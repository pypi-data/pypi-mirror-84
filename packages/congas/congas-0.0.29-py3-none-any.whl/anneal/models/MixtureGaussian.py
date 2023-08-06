import pyro
import pyro.distributions as dist
import torch
from congas.models.Model import Model
from pyro.ops.indexing import Vindex
from pyro import poutine
from pyro.infer.autoguide import AutoDelta
from torch.distributions import constraints






class MixtureGaussian(Model):

    """

    A simple mixture model for CNV inference, it assumes independence among the different segments, needs to be used after
    calling CNV regions with bulk DNA or RNA. CNVs events are modelled as LogNormal distributions.


    Model parameters:
        K = number of clusters (default = 2)
        cnv_var = var of the LogNorm prior (default = 0.6)
        theta_scale = scale for the normalization factor variable (default = 3)
        theta_rate = rate for the normalization factor variable (default = 1)
        batch_size = batch size (default = None)
        mixture = prior for the mixture weights (default = 1/torch.ones(K))
        gamma_multiplier = multiplier Gamma(rate * gamma_multiplier, shape  * gamma_multiplier) when we also want to
        infer the shape and rate parameter (i.e. when MAP = FALSE) (default = 4)





    TODO:
        add support for joint inference with bulk counts (or allelic frequencies)


    """

    params = {'K': 2, 'cnv_sd': 0.6, 'theta_scale': 3, 'theta_rate': 1, 'batch_size': None,
              'mixture':  None}
    data_name = set(['data', 'mu', 'pld'])

    def __init__(self, data_dict):

        self._params = self.params.copy()
        self._data = None
        super().__init__(data_dict, self.data_name)

    def model(self,*args, **kwargs):
        I, N = self._data['data'].shape
        batch = N if self._params['batch_size'] else self._params['batch_size']
        weights = pyro.sample('mixture_weights', dist.Dirichlet(torch.ones(self._params['K'])))

        with pyro.plate('segments', I):
            with pyro.plate('components', self._params['K']):
                cc = pyro.sample('cnv_probs', dist.LogNormal(torch.log(self._data['pld']), self._params['cnv_sd']))

        with pyro.plate("data2", N, batch):
            theta = pyro.sample('norm_factor', dist.Gamma(self._params['theta_scale'], self._params['theta_rate']))

        with pyro.plate('data', N, batch):

            assignment = pyro.sample('assignment', dist.Categorical(weights), infer={"enumerate": "parallel"})


            for i in pyro.plate('segments2', I):
                pyro.sample('obs_{}'.format(i), dist.Poisson((Vindex(cc)[assignment,i] * theta * self._data['mu'][i])
                                                             + 1e-8), obs=self._data['data'][i, :])

    def guide(self,MAP = False,*args, **kwargs):
        if(MAP):
            return AutoDelta(poutine.block(self.model, expose=['mixture_weights', 'norm_factor', 'cnv_probs']),
                             init_loc_fn=self.init_fn())
        else:
            def guide_ret(*args, **kwargs):
                I, N = self._data['data'].shape
                batch = N if self._params['batch_size'] else self._params['batch_size']

                param_weights = pyro.param("param_mixture_weights", lambda: torch.ones(self._params['K']) / self._params['K'],
                                           constraint=constraints.simplex)
                cnv_mean = pyro.param("param_cnv_probs", lambda: self.create_gaussian_init_values(),
                                         constraint=constraints.positive)
                cnv_var = pyro.param("param_cnv_var", lambda: torch.ones(1) * self._params['cnv_sd'],
                                      constraint=constraints.positive)
                gamma_scale = pyro.param("param_norm_factor", lambda: torch.mean(self._data['data'] / (2 * self._data['mu'].reshape(self._data['data'].shape[0],1)), axis=0),
                                   constraint=constraints.positive)

                pyro.sample('mixture_weights', dist.Dirichlet(param_weights))

                with pyro.plate('segments', I):
                    with pyro.plate('components', self._params['K']):
                        pyro.sample('cnv_probs', dist.LogNormal(torch.log(cnv_mean), cnv_var))

                with pyro.plate("data2", N, batch):
                    pyro.sample('norm_factor', dist.Delta(gamma_scale))


            return guide_ret


    def create_gaussian_init_values(self):
        init = torch.zeros(self._params['K'], self._data['data'].shape[0])
        for i in range(len(self._data['pld'])):
            for k in range(self._params['K']):
                if k == 0:
                    init[k, i] = torch.ceil(self._data['pld'][i])
                else:
                    init[k, i] = torch.floor(self._data['pld'][i])
        return init

    def full_guide(self, MAP = False , *args, **kwargs):
        def full_guide_ret(*args, **kargs):
            I, N = self._data['data'].shape
            batch = N if self._params['batch_size'] else self._params['batch_size']

            with poutine.block(hide_types=["param"]):  # Keep our learned values of global parameters.
                self.guide(MAP)()
            with pyro.plate('data', N, batch):
                assignment_probs = pyro.param('assignment_probs', torch.ones(N, self._params['K']) / self._params['K'],
                                              constraint=constraints.simplex)
                pyro.sample('assignment', dist.Categorical(assignment_probs), infer={"enumerate": "parallel"})

        return full_guide_ret



    def init_fn(self):
        def init_function(site):
            if site["name"] == "cnv_probs":
                return self.create_gaussian_init_values()
            if site["name"] == "mixture_weights":
                return self._params['mixture']
            if site["name"] == "norm_factor":
                return torch.mean(self._data['data'] / (2 * self._data['mu'].reshape(self._data['data'].shape[0],1)), axis=0)
            raise ValueError(site["name"])
        return init_function



