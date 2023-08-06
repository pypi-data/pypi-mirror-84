import numpy as np
from .hmc_utils.step_size import DualAverageAdaptation
from .hmc_utils.metrics import QuadMetric, QuadMetricDiag, QuadMetricFull
from .hmc_utils.metrics import QuadMetricDiagAdapt, QuadMetricFullAdapt
from .hmc_utils.stats import HStepStats, NStepStats, THStepStats, TNStepStats
from .hmc_utils.stats import HStats, NStats, THStats, TNStats
from ..utils.random import get_generator, spawn_generator
from ..core import Density, DensityLite
from copy import deepcopy
import warnings

__all__ = ['SampleTrace', '_HTrace', 'NTrace', 'HTrace', 'TNTrace', 'THTrace',
           'ETrace', 'TraceTuple', '_get_step_size', '_get_metric']

# TODO: StatsTuple?


class SampleTrace:
    """Utilities shared by all different types of SampleTrace classes."""
    def __init__(self, n_chain=4, n_iter=1500, n_warmup=500, x_0=None,
                 random_generator=None):
        self._chain_initialized = False
        self.n_chain = n_chain
        self.n_iter = n_iter
        self.n_warmup = n_warmup
        self.x_0 = x_0
        self.random_generator = random_generator
        self._x_0_transformed = False

    @property
    def chain_initialized(self):
        return self._chain_initialized

    @property
    def n_chain(self):
        return self._n_chain

    @n_chain.setter
    def n_chain(self, n):
        if self._chain_initialized:
            raise RuntimeError('you should not change n_chain once the chain '
                               'is initialized.')
        try:
            n = int(n)
            assert n > 0
        except Exception:
            raise ValueError('n_chain should be a positive int, instead of '
                             '{}.'.format(n))
        self._n_chain = n

    @property
    def n_iter(self):
        try:
            return self._n_iter
        except Exception:
            return 0

    @n_iter.setter
    def n_iter(self, n):
        try:
            n = int(n)
            assert n > 0
        except Exception:
            raise ValueError('n_iter should be a positive int, instead of '
                             '{}.'.format(n))
        if n < self.i_iter:
            raise ValueError(
                'you have already run {} iterations, so n_iter should not be '
                'smaller than this number.'.format(self.i_iter))
        if n < self.n_warmup:
            raise ValueError('n_warmup is {}, so n_iter should not be smaller '
                             'than this number.'.format(self.n_warmup))
        self._n_iter = n

    @property
    def i_iter(self):
        raise NotImplementedError('Abstract property.')

    @property
    def n_warmup(self):
        try:
            return self._n_warmup
        except Exception:
            return 0

    @n_warmup.setter
    def n_warmup(self, n):
        try:
            n = int(n)
            assert n > 0
        except Exception:
            raise ValueError('n_warmup should be a positive int, instead of '
                             '{}.'.format(n))
        self._warmup_check(n)
        if n >= self.n_iter:
            raise ValueError('n_iter is {}, so n_warmup should be smaller than '
                             'this number.'.format(self.n_iter))
        self._n_warmup = n

    def _warmup_check(self, n):
        pass

    def add_iter(self, n):
        self.n_iter = self.n_iter + n

    def add_warmup(self, n):
        self.n_warmup = self.n_warmup + n

    @property
    def x_0(self):
        return self._x_0

    @x_0.setter
    def x_0(self, x):
        if self._chain_initialized:
            raise RuntimeError('you should not change x_0 once the chain '
                               'is initialized.')
        if x is None:
            self._x_0 = None
        else:
            try:
                self._x_0 = np.atleast_1d(x).copy()
            except Exception:
                raise ValueError('invalid value for x_0.')

    # TODO: maybe we can have a better name for this?
    @property
    def x_0_transformed(self):
        return self._x_0_transformed

    @property
    def samples(self):
        raise NotImplementedError('Abstract property.')

    @property
    def input_size(self):
        try:
            return self.x_0.shape[-1]
        except Exception:
            return None

    @property
    def random_generator(self):
        if self._random_generator is None:
            return get_generator()
        else:
            return self._random_generator

    @random_generator.setter
    def random_generator(self, generator):
        if generator is None:
            self._random_generator = None
        else:
            self._random_generator = np.random.default_rng(generator)


class _HTrace(SampleTrace):
    """Utilities shared by HTrace and NTrace."""
    def __init__(self, n_chain=4, n_iter=1500, n_warmup=500, x_0=None,
                 random_generator=None, step_size=None, adapt_step_size=True,
                 metric='diag', adapt_metric=True, max_change=1000.,
                 target_accept=0.8, gamma=0.05, k=0.75, t_0=10.,
                 initial_mean=None, initial_weight=10., adapt_window=60,
                 update_window=1, doubling=True):
        super().__init__(n_chain, n_iter, n_warmup, x_0, random_generator)
        self._samples = []
        self._chain_id = None
        self.max_change = max_change
        self._set_step_size(step_size, adapt_step_size, target_accept, gamma, k,
                            t_0)
        self._set_metric(metric, adapt_metric, initial_mean, initial_weight,
                         adapt_window, update_window, doubling)

    @property
    def chain_id(self):
        return self._chain_id

    def _init_chain(self, i):
        if self._x_0 is None:
            raise RuntimeError('no valid x_0 is given.')
        if self._chain_id is not None:
            warnings.warn('chain_id is supposed to be set only once, but now '
                          'you are trying to modify it.', RuntimeWarning)
        try:
            i = int(i)
            assert i >= 0
            assert i < self.n_chain
        except Exception:
            raise ValueError(
                'i should satisfy 0 <= i < n_chain, but you give {}.'.format(i))
        self._chain_id = i
        self.random_generator = spawn_generator(
            self.random_generator, self.n_chain)[i]
        self._x_0 = self._x_0.reshape((-1, self._x_0.shape[-1]))
        if self._x_0.shape[0] == self._n_chain:
            self._x_0 = self._x_0[i]
        else:
            self._x_0 = self._x_0[
                self.random_generator.integers(0, self._x_0.shape[0])]
        self._set_step_size_2()
        self._set_metric_2()
        self._chain_initialized = True

    @property
    def step_size(self):
        return self._step_size

    @property
    def metric(self):
        return self._metric

    @property
    def max_change(self):
        return self._max_change

    @max_change.setter
    def max_change(self, max_change):
        try:
            max_change = float(max_change)
            assert max_change > 0
        except Exception:
            raise ValueError('max_change should be a positive float, instead '
                             'of {}.'.format(max_change))
        self._max_change = max_change

    @property
    def samples(self):
        return np.asarray(self._samples)

    @property
    def samples_original(self):
        return np.asarray(self._samples_original)

    @property
    def i_iter(self):
        try:
            return len(self._samples)
        except Exception:
            return 0

    @property
    def finished(self):
        if self.i_iter < self.n_iter:
            return False
        elif self.i_iter == self.n_iter:
            return True
        else:
            raise RuntimeError('unexpected behavior: i_iter seems larger than '
                               'n_iter.')

    @property
    def logp(self):
        return np.asarray(self.stats._logp)

    @property
    def logp_original(self):
        return np.asarray(self._logp_original)

    @property
    def stats(self):
        try:
            return self._stats
        except Exception:
            raise NotImplementedError('stats is not defined for this '
                                      'SampleTrace.')

    @property
    def n_call(self):
        raise NotImplementedError('abstract property.')

    def update(self, point, stats):
        self._samples.append(point)
        self._stats.update(stats)

    _all_return = ['samples', 'logp']

    def get(self, since_iter=None, include_warmup=False, original_space=True,
            return_type='samples', flatten=True):
        if return_type == 'all':
            return [self.get(since_iter, include_warmup, original_space, _,
                    flatten) for _ in self._all_return]
        if flatten is not True:
            warnings.warn('the argument flatten is not used here.',
                          RuntimeWarning)
        if since_iter is None:
            since_iter = 0 if include_warmup else self.n_warmup
        else:
            try:
                since_iter = int(since_iter)
            except Exception:
                raise ValueError('invalid value for since_iter.')
        if since_iter >= self.i_iter - 1:
            raise ValueError('since_iter is too large. Nothing to return.')
        if return_type == 'samples':
            samples = self.samples_original if original_space else self.samples
            samples = samples[since_iter:]
            return samples
        elif return_type == 'logp':
            logp = self.logp_original if original_space else self.logp
            logp = logp[since_iter:]
            return logp
        else:
            return self._get(since_iter, original_space, return_type)

    def _get(self, since_iter, original_space, return_type):
        raise ValueError('invalid value for return_type.')

    __call__ = get

    def _warmup_check(self, n):
        if self.i_iter > 0:
            _adapt_metric = isinstance(self.metric, (QuadMetricDiagAdapt,
                                                     QuadMetricFullAdapt))
            _adapt_step_size = self._step_size._adapt
            if _adapt_metric or _adapt_step_size:
                if self.n_warmup < self.i_iter or n < self.i_iter:
                    warnings.warn(
                        'please be cautious to modify n_warmup for the adaptive'
                        ' HMC/NUTS sampler, when i_iter is larger than '
                        'n_warmup(old) and/or n_warmup(new).', RuntimeWarning)

    def _set_step_size(self, step_size, adapt_step_size, target_accept, gamma,
                       k, t_0):
        if isinstance(step_size, DualAverageAdaptation):
            self._step_size = step_size
        else:
            if step_size is None:
                pass
            else:
                try:
                    step_size = float(step_size)
                    assert step_size > 0
                except Exception:
                    raise ValueError('invalid value for step_size.')
            self._step_size = step_size
            self._adapt_step_size = bool(adapt_step_size)

            try:
                target_accept = float(target_accept)
                assert 0 < target_accept < 1
            except Exception:
                raise ValueError('invalid value for target_accept.')
            self._target_accept = target_accept

            try:
                gamma = float(gamma)
                assert gamma != 0
            except Exception:
                raise ValueError('invalid value for gamma.')
            self._gamma = gamma

            try:
                k = float(k)
            except Exception:
                raise ValueError('invalid value for k.')
            self._k = k

            try:
                t_0 = float(t_0)
                assert t_0 >= 0
            except Exception:
                raise ValueError('invalid value for t_0.')
            self._t_0 = t_0

    def _set_step_size_2(self):
        if isinstance(self.step_size, DualAverageAdaptation):
            pass
        else:
            if self._step_size is None:
                self._step_size = 1.
            self._step_size = DualAverageAdaptation(
                self._step_size / self.input_size**0.25, self._target_accept,
                self._gamma, self._k, self._t_0, self._adapt_step_size)

    def _set_metric(self, metric, adapt_metric, initial_mean, initial_weight,
                    adapt_window, update_window, doubling):
        if isinstance(metric, QuadMetric):
            self._metric = metric
        else:
            if metric == 'diag' or metric == 'full':
                pass
            else:
                try:
                    metric = np.asarray(metric)
                    n = metric.shape[0]
                    assert metric.shape == (n,) or metric.shape == (n, n)
                except Exception:
                    raise ValueError('invalid value for metric.')
            self._metric = metric
            self._adapt_metric = bool(adapt_metric)

            if initial_mean is None:
                pass
            else:
                try:
                    initial_mean = np.atleast_1d(initial_mean)
                    assert initial_mean.ndim == 1
                except Exception:
                    raise ValueError('invalid value for initial_mean.')
            self._initial_mean = initial_mean

            try:
                initial_weight = float(initial_weight)
                assert initial_weight > 0
            except Exception:
                raise ValueError('invalid value for initial_weight.')
            self._initial_weight = initial_weight

            try:
                adapt_window = int(adapt_window)
                assert adapt_window > 0
            except Exception:
                raise ValueError('invalid value for adapt_window.')
            self._adapt_window = adapt_window

            try:
                update_window = int(update_window)
                assert update_window > 0
            except Exception:
                raise ValueError('invalid value for update_window.')
            self._update_window = update_window
            self._doubling = bool(doubling)

    def _set_metric_2(self):
        if isinstance(self.metric, QuadMetric):
            pass
        else:
            if isinstance(self._metric, str) and self._metric == 'diag':
                self._metric = np.ones(self.input_size)
            elif isinstance(self._metric, str) and self._metric == 'full':
                self._metric = np.eye(self.input_size)
            elif isinstance(self._metric, np.ndarray):
                pass
            else:
                raise RuntimeError('unexpected value for self._metric.')

            if self._initial_mean is None:
                self._initial_mean = self.x_0.copy()

            if self._metric.ndim == 1 and self._adapt_metric:
                self._metric = QuadMetricDiagAdapt(
                    self.input_size, self._initial_mean, self._metric,
                    self._initial_weight, self._adapt_window,
                    self._update_window, self._doubling)
            elif self._metric.ndim == 2 and self._adapt_metric:
                self._metric = QuadMetricFullAdapt(
                    self.input_size, self._initial_mean, self._metric,
                    self._initial_weight, self._adapt_window,
                    self._update_window, self._doubling)
            elif self._metric.ndim == 1 and not self._adapt_metric:
                self._metric = QuadMetricDiag(self._metric)
            elif self._metric.ndim == 2 and not self._adapt_metric:
                self._metric = QuadMetricFull(self._metric)
            else:
                raise RuntimeError('unexpected value for self._metric.')


class HTrace(_HTrace):
    """Trace class for the (vanilla) HMC sampler."""
    def __init__(self, n_chain=4, n_iter=1500, n_warmup=500, n_int_step=32,
                 x_0=None, random_generator=None, step_size=1.,
                 adapt_step_size=True, metric='diag', adapt_metric=True,
                 max_change=1000., target_accept=0.8, gamma=0.05, k=0.75,
                 t_0=10., initial_mean=None, initial_weight=10.,
                 adapt_window=60, update_window=1, doubling=True):
        super().__init__(n_chain, n_iter, n_warmup, x_0, random_generator,
                         step_size, adapt_step_size, metric, adapt_metric,
                         max_change, target_accept, gamma, k, t_0, initial_mean,
                         initial_weight, adapt_window, update_window, doubling)
        self.n_int_step = n_int_step
        self._stats = HStats()

    @property
    def n_int_step(self):
        return self._n_int_step

    @n_int_step.setter
    def n_int_step(self, nis):
        try:
            nis = int(nis)
            assert nis > 0
        except Exception:
            raise ValueError('n_int_step should be a positive int, instead '
                             'of {}.'.format(nis))
        self._n_int_step = nis

    @property
    def n_call(self):
        return self.n_iter * (self.n_int_step + 1) + 1
        """
        Here we add n_iter because at the beginning of each iteration, 
        We recompute logp_and_grad at the starting point.
        In principle this can be avoided by reusing the old values,
        But the current implementation doesn't do it in this way.
        We add another 1 for the test during initialization.
        """


class NTrace(_HTrace):
    """Trace class for the NUTS sampler."""
    def __init__(self, n_chain=4, n_iter=1500, n_warmup=500, x_0=None,
                 random_generator=None, step_size=1., adapt_step_size=True,
                 metric='diag', adapt_metric=True, max_change=1000.,
                 max_treedepth=10, target_accept=0.8, gamma=0.05, k=0.75,
                 t_0=10., initial_mean=None, initial_weight=10.,
                 adapt_window=60, update_window=1, doubling=True):
        super().__init__(n_chain, n_iter, n_warmup, x_0, random_generator,
                         step_size, adapt_step_size, metric, adapt_metric,
                         max_change, target_accept, gamma, k, t_0, initial_mean,
                         initial_weight, adapt_window, update_window, doubling)
        self.max_treedepth = max_treedepth
        self._stats = NStats()

    @property
    def max_treedepth(self):
        return self._max_treedepth

    @max_treedepth.setter
    def max_treedepth(self, mt):
        try:
            mt = int(mt)
            assert mt > 0
        except Exception:
            raise ValueError('max_treedepth should be a postive int, instead '
                             'of {}.'.format(mt))
        self._max_treedepth = mt

    @property
    def n_call(self):
        return sum(self._stats._tree_size[1:]) + self.n_iter + 1
        """
        Here we add n_iter because at the beginning of each iteration, 
        We recompute logp_and_grad at the starting point.
        In principle this can be avoided by reusing the old values,
        But the current implementation doesn't do it in this way.
        We add another 1 for the test during initialization.
        """


class _TTrace:
    """Utilities shared by THTrace and TNTrace."""
    def __init__(self, density_base, logxi=0.):
        self.density_base = density_base
        self.logxi = logxi

    @property
    def density_base(self):
        return self._density_base

    @density_base.setter
    def density_base(self, db):
        try:
            assert isinstance(db, (Density, DensityLite))
        except Exception:
            raise ValueError('invalid value for density_base.')
        self._density_base = db

    @property
    def logxi(self):
        return self._logxi

    @logxi.setter
    def logxi(self, lxi):
        try:
            self._logxi = float(lxi)
        except Exception:
            raise ValueError('invalid value for logxi.')

    @property
    def u(self):
        return np.array(self.stats._u)

    @property
    def weights(self):
        return np.array(self.stats._weights)

    _all_return = ['samples', 'u', 'weights', 'logp']

    def _get(self, since_iter, original_space, return_type):
        if return_type == 'u':
            u = self.u[since_iter:]
            return u
        elif return_type == 'weights':
            weights = self.weights[since_iter:]
            return weights
        else:
            raise ValueError('invalid value for return_type.')


class THTrace(_TTrace, HTrace):
    """Trace class for the THMC sampler."""
    def __init__(self, density_base, logxi=0., n_chain=4, n_iter=1500,
                 n_warmup=500, n_int_step=32, x_0=None, random_generator=None,
                 step_size=1., adapt_step_size=True, metric='diag',
                 adapt_metric=True, max_change=1000., target_accept=0.8,
                 gamma=0.05, k=0.75, t_0=10., initial_mean=None,
                 initial_weight=10., adapt_window=60, update_window=1,
                 doubling=True):
        _TTrace.__init__(self, density_base, logxi)
        HTrace.__init__(n_chain, n_iter, n_warmup, n_int_step, x_0,
                        random_generator, step_size, adapt_step_size, metric,
                        adapt_metric, max_change, target_accept, gamma, k, t_0,
                        initial_mean, initial_weight, adapt_window,
                        update_window, doubling)


class TNTrace(_TTrace, NTrace):
    """Trace class for the TNUTS sampler."""
    def __init__(self, density_base, logxi=0., n_chain=4, n_iter=1500,
                 n_warmup=500, x_0=None, random_generator=None, step_size=1.,
                 adapt_step_size=True, metric='diag', adapt_metric=True,
                 max_change=1000., max_treedepth=10, target_accept=0.8,
                 gamma=0.05, k=0.75, t_0=10., initial_mean=None,
                 initial_weight=10., adapt_window=60, update_window=1,
                 doubling=True):
        _TTrace.__init__(self, density_base, logxi)
        NTrace.__init__(self, n_chain, n_iter, n_warmup, x_0, random_generator,
                        step_size, adapt_step_size, metric, adapt_metric,
                        max_change, max_treedepth, target_accept, gamma, k, t_0,
                        initial_mean, initial_weight, adapt_window,
                        update_window, doubling)
        self._stats = TNStats()


class ETrace(SampleTrace):
    """Trace class for the ensemble sampler from emcee."""
    def __init__(*args, **kwargs):
        raise NotImplementedError


class TraceTuple:
    """Collection of multiple NTrace/HTrace from different chains."""
    def __init__(self, sample_traces):
        try:
            sample_traces = tuple(sample_traces)
            if isinstance(sample_traces[0], TNTrace):
                self._sampler = 'TNUTS'
            elif isinstance(sample_traces[0], THTrace):
                self._sampler = 'THMC'
            elif isinstance(sample_traces[0], NTrace):
                self._sampler = 'NUTS'
            elif isinstance(sample_traces[0], HTrace):
                self._sampler = 'HMC'
            else:
                raise ValueError('invalid value for sample_traces')
            _type = type(sample_traces[0])
            for i, t in enumerate(sample_traces):
                assert type(t) == _type
                assert t.chain_id == i
            self._sample_traces = sample_traces
        except Exception:
            raise ValueError('invalid value for sample_traces.')

    @property
    def sample_traces(self):
        return self._sample_traces

    @property
    def sampler(self):
        return self._sampler

    @property
    def n_chain(self):
        return self.sample_traces[0].n_chain

    @property
    def n_iter(self):
        return self.sample_traces[0].n_iter

    @n_iter.setter
    def n_iter(self, n):
        tmp = self.n_iter
        try:
            for t in self.sample_traces:
                t.n_iter = n
        except Exception:
            for t in self.sample_traces:
                t._n_iter = tmp
            raise

    @property
    def i_iter(self):
        return self.sample_traces[0].i_iter

    @property
    def n_warmup(self):
        return self.sample_traces[0].n_warmup

    @n_warmup.setter
    def n_warmup(self, n):
        tmp = self.n_warmup
        try:
            for t in self.sample_traces:
                t.n_warmup = n
        except Exception:
            for t in self.sample_traces:
                t._n_warmup = tmp
            raise

    @property
    def n_call(self):
        return sum([t.n_call for t in self.sample_traces])

    @property
    def samples(self):
        s = np.array([t.samples for t in self.sample_traces])
        if s.dtype.kind != 'f':
            warnings.warn('the array of samples does not has dtype of float, '
                          'presumably because different chains have run for '
                          'different lengths.', RuntimeWarning)
        return s

    @property
    def samples_original(self):
        s = np.array([t.samples_original for t in self.sample_traces])
        if s.dtype.kind != 'f':
            warnings.warn('the array of samples_original does not has dtype of '
                          'float, presumably because different chains have run '
                          'for different lengths.', RuntimeWarning)
        return s

    @property
    def logp(self):
        l = np.array([t.logp for t in self.sample_traces])
        if l.dtype.kind != 'f':
            warnings.warn('the array of logp does not has dtype of float, '
                          'presumably because different chains have run for '
                          'different lengths.', RuntimeWarning)
        return l

    @property
    def logp_original(self):
        l = np.array([t.logp_original for t in self.sample_traces])
        if l.dtype.kind != 'f':
            warnings.warn('the array of logp_original does not has dtype of '
                          'float, presumably because different chains have run '
                          'for different lengths.', RuntimeWarning)
        return l

    @property
    def input_size(self):
        return self.samples.shape[-1]

    @property
    def finished(self):
        return self.sample_traces[0].finished

    @property
    def stats(self):
        return [t.stats for t in self.sample_traces] # add StatsTuple?

    @property
    def _all_return(self):
        if self.sampler == 'NUTS' or self.sampler == 'HMC':
            return _HTrace._all_return
        elif self.sampler == 'TNUTS' or self.sampler == 'THMC':
            return _TTrace._all_return
        else:
            raise RuntimeError('unexpected value for self.sampler.')

    # TODO: the default value for flatten?
    def get(self, since_iter=None, include_warmup=False, original_space=True,
            return_type='samples', flatten=True):
        if return_type == 'all':
            return [self.get(since_iter, include_warmup, original_space, _,
                    flatten) for _ in self._all_return]
        tget = [t.get(since_iter, include_warmup, original_space, return_type)
                for t in self.sample_traces]
        if return_type == 'samples':
            samples = np.asarray(tget)
            if flatten:
                samples = samples.reshape((-1, self.input_size))
            return samples
        elif return_type == 'logp':
            logp = np.asarray(tget)
            if flatten:
                logp = logp.flatten()
            return logp
        elif return_type == 'u' or return_type == 'weights':
            if not (self.sampler == 'TNUTS' or self.sampler == 'THMC'):
                raise RuntimeError('invalid value for return_type.')
            res = np.asarray(tget)
            if flatten:
                res = res.flatten()
            return res
        else:
            raise ValueError('invalid value for return_type.')

    __call__ = get

    def __getitem__(self, key):
        return self._sample_traces.__getitem__(key)

    def __len__(self):
        return self._sample_traces.__len__()

    def __iter__(self):
        return self._sample_traces.__iter__()

    def __next__(self):
        return self._sample_traces.__next__()


def _get_step_size(sample_trace):
    if isinstance(sample_trace, _HTrace):
        step_size = sample_trace.step_size
        dim = sample_trace.input_size
        if not isinstance(step_size, DualAverageAdaptation):
            raise RuntimeError('sample_trace.step_size should be a '
                               'DualAverageAdaptation.')
        if not isinstance(dim, int):
            raise RuntimeError('sample_trace.input_size is not defined.')
        return step_size.current(False) * dim**0.25
    elif isinstance(sample_trace, TraceTuple):
        return np.mean([_get_step_size(sti) for sti in sample_trace])
    else:
        raise ValueError('invalid value for sample_trace.')


def _get_metric(sample_trace, target, from_samples=True):
    if from_samples:
        if isinstance(sample_trace, (_HTrace, TraceTuple)):
            samples = sample_trace.get(original_space=False, flatten=True)
            cov = np.cov(samples, rowvar=False)
        else:
            raise ValueError('invalid value for sample_trace.')
    else:
        if isinstance(sample_trace, _HTrace):
            metric = sample_trace.metric
            if isinstance(metric, QuadMetricDiag):
                cov = np.diag(metric._var)
            elif isinstance(metric, QuadMetricFull):
                cov = np.copy(metric._cov)
            else:
                raise RuntimeError('sample_trace.metric is not a QuadMetric.')
        elif isinstance(sample_trace, TraceTuple):
            return np.mean([_get_metric(sti, target, from_samples) for sti in
                            sample_trace], axis=0)
        else:
            raise ValueError('invalid value for sample_trace.')

    if target == 'diag':
        return np.diag(cov)
    elif target == 'full':
        return cov
    else:
        raise ValueError('unexpected value for target.')
