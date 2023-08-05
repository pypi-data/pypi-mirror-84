# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/12_optimizer.ipynb (unless otherwise specified).

__all__ = ['Optimizer', 'sgd_step', 'weight_decay', 'l2_reg', 'average_grad', 'average_sqr_grad', 'momentum_step',
           'SGD', 'rms_prop_step', 'RMSProp', 'step_stat', 'debias', 'adam_step', 'Adam', 'radam_step', 'RAdam',
           'qhadam_step', 'QHAdam', 'larc_layer_lr', 'larc_step', 'Larc', 'lamb_step', 'Lamb', 'Lookahead', 'ranger',
           'detuplify_pg', 'set_item_pg', 'pytorch_hp_map', 'OptimWrapper']

# Cell
from .torch_basics import *

# Cell
class _BaseOptimizer():
    "Common functionality between `Optimizer` and `OptimWrapper`"
    def all_params(self, n=slice(None), with_grad=False):
        res = L((p,pg,self.state[p],hyper) for pg,hyper in zip(self.param_lists[n],self.hypers[n]) for p in pg)
        return L(o for o in res if hasattr(o[0], 'grad') and o[0].grad is not None) if with_grad else res

    def _set_require_grad(self, rg, p,pg,state,h): p.requires_grad_(rg or state.get('force_train', False))
    def freeze_to(self, n):
        self.frozen_idx = n if n >= 0 else len(self.param_lists) + n
        if self.frozen_idx >= len(self.param_lists):
            warn(f"Freezing {self.frozen_idx} groups; model has {len(self.param_lists)}; whole model is frozen.")
        for o in self.all_params(slice(n, None)): self._set_require_grad(True,  *o)
        for o in self.all_params(slice(None, n)): self._set_require_grad(False, *o)

    def freeze(self):
        assert(len(self.param_lists)>1)
        self.freeze_to(-1)

    def set_freeze(self, n, rg, ignore_force_train=False):
        for p in self.param_lists[n]: p.requires_grad_(rg or (state.get('force_train', False) and not ignore_force_train))

    def unfreeze(self): self.freeze_to(0)
    def set_hypers(self, **kwargs): L(kwargs.items()).starmap(self.set_hyper)
    def _set_hyper(self, k, v):
        for v_,h in zip(v, self.hypers): h[k] = v_

    def set_hyper(self, k, v):
        if isinstance(v, slice):
            if v.start: v = even_mults(v.start, v.stop, len(self.param_lists))
            else: v = [v.stop/10]*(len(self.param_lists)-1) + [v.stop]
        v = L(v, use_list=None)
        if len(v)==1: v = v*len(self.param_lists)
        assert len(v) == len(self.hypers), f"Trying to set {len(v)} values for {k} but there are {len(self.param_lists)} parameter groups."
        self._set_hyper(k, v)

    @property
    def param_groups(self): return [{**{'params': pg}, **hp} for pg,hp in zip(self.param_lists, self.hypers)]
    @param_groups.setter
    def param_groups(self, v):
        for pg,v_ in zip(self.param_lists,v): pg = v_['params']
        for hyper,v_ in zip(self.hypers,v):
            for k,t in v_.items():
                if k != 'params': hyper[k] = t

# Cell
def _update(state, new=None):
    if new is None: return state
    if isinstance(new, dict): state.update(new)
    return state

# Cell
@log_args(but='params,cbs,defaults')
class Optimizer(_BaseOptimizer):
    "Base optimizer class for the fastai library, updating `params` with `cbs`"
    _keep_on_clear = ['force_train', 'do_wd']
    def __init__(self, params, cbs, train_bn=True, **defaults):
        params = L(params)
        self.cbs,self.state,self.train_bn = L(cbs),defaultdict(dict),train_bn
        defaults = merge(*self.cbs.attrgot('defaults'), defaults)
        self.param_lists = L(L(p) for p in params) if isinstance(params[0], (L,list)) else L([params])
        self.hypers = L({} for _ in range_of(self.param_lists))
        self.set_hypers(**defaults)
        self.frozen_idx = 0

    def zero_grad(self):
        for p,*_ in self.all_params(with_grad=True):
            p.grad.detach_()
            p.grad.zero_()

    def step(self):
        for p,pg,state,hyper in self.all_params(with_grad=True):
            for cb in self.cbs: state = _update(state, cb(p, **{**state, **hyper}))
            self.state[p] = state

    def clear_state(self):
        for p,pg,state,hyper in self.all_params():
            self.state[p] = {k: state[k] for k in self._keep_on_clear if k in state}

    def state_dict(self):
        state = [self.state[p] for p,*_ in self.all_params()]
        return {'state': state, 'hypers': self.hypers}

    def load_state_dict(self, sd):
        assert len(sd["hypers"]) == len(self.param_lists)
        assert len(sd["state"])  == sum([len(pg) for pg in self.param_lists])
        self.hypers = sd['hypers']
        self.state = {p: s for p,s in zip(self.all_params().itemgot(0), sd['state'])}

# Cell
def sgd_step(p, lr, **kwargs):
    p.data.add_(p.grad.data, alpha=-lr)

# Cell
def weight_decay(p, lr, wd, do_wd=True, **kwargs):
    "Weight decay as decaying `p` with `lr*wd`"
    if do_wd and wd!=0: p.data.mul_(1 - lr*wd)

weight_decay.defaults = dict(wd=0.)

# Cell
def l2_reg(p, lr, wd, do_wd=True, **kwargs):
    "L2 regularization as adding `wd*p` to `p.grad`"
    if do_wd and wd!=0: p.grad.data.add_(p.data, alpha=wd)

l2_reg.defaults = dict(wd=0.)

# Cell
def average_grad(p, mom, dampening=False, grad_avg=None, **kwargs):
    "Keeps track of the avg grads of `p` in `state` with `mom`."
    if grad_avg is None: grad_avg = torch.zeros_like(p.grad.data)
    damp = 1-mom if dampening else 1.
    grad_avg.mul_(mom).add_(p.grad.data, alpha=damp)
    return {'grad_avg': grad_avg}

average_grad.defaults = dict(mom=0.9)

# Cell
def average_sqr_grad(p, sqr_mom, dampening=True, sqr_avg=None, **kwargs):
    if sqr_avg is None: sqr_avg = torch.zeros_like(p.grad.data)
    damp = 1-sqr_mom if dampening else 1.
    sqr_avg.mul_(sqr_mom).addcmul_(p.grad.data, p.grad.data, value=damp)
    return {'sqr_avg': sqr_avg}

average_sqr_grad.defaults = dict(sqr_mom=0.99)

# Cell
def momentum_step(p, lr, grad_avg, **kwargs):
    "Step for SGD with momentum with `lr`"
    p.data.add_(grad_avg, alpha=-lr)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def SGD(params, lr, mom=0., wd=0., decouple_wd=True):
    "A `Optimizer` for SGD with `lr` and `mom` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    if mom != 0: cbs.append(average_grad)
    cbs.append(sgd_step if mom==0 else momentum_step)
    return Optimizer(params, cbs, lr=lr, mom=mom, wd=wd)

# Cell
def rms_prop_step(p, lr, sqr_avg, eps, grad_avg=None, **kwargs):
    "Step for SGD with momentum with `lr`"
    denom = sqr_avg.sqrt().add_(eps)
    p.data.addcdiv_((grad_avg if grad_avg is not None else p.grad), denom, value=-lr)

rms_prop_step.defaults = dict(eps=1e-8)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def RMSProp(params, lr, sqr_mom=0.99, mom=0., wd=0., decouple_wd=True):
    "A `Optimizer` for RMSProp with `lr`, `sqr_mom`, `mom` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += ([average_sqr_grad] if mom==0. else [average_grad, average_sqr_grad])
    cbs.append(rms_prop_step)
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, wd=wd)

# Cell
def step_stat(p, step=0, **kwargs):
    "Register the number of steps done in `state` for `p`"
    step += 1
    return {'step' : step}

# Cell
def debias(mom, damp, step): return damp * (1 - mom**step) / (1-mom)

# Cell
def adam_step(p, lr, mom, step, sqr_mom, grad_avg, sqr_avg, eps, **kwargs):
    "Step for Adam with `lr` on `p`"
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    p.data.addcdiv_(grad_avg, (sqr_avg/debias2).sqrt() + eps, value = -lr / debias1)
    return p

adam_step._defaults = dict(eps=1e-5)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def Adam(params, lr, mom=0.9, sqr_mom=0.99, eps=1e-5, wd=0.01, decouple_wd=True):
    "A `Optimizer` for Adam with `lr`, `mom`, `sqr_mom`, `eps` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), average_sqr_grad, step_stat, adam_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd)

# Cell
def radam_step(p, lr, mom, step, sqr_mom, grad_avg, sqr_avg, eps, beta, **kwargs):
    "Step for RAdam with `lr` on `p`"
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    r_inf = 2/(1-sqr_mom) - 1
    r = r_inf - 2*step*sqr_mom**step/(1-sqr_mom**step)
    if r > 5:
        v = math.sqrt(((r-4) * (r-2) * r_inf)/((r_inf-4)*(r_inf-2)*r))
        denom = (sqr_avg/debias2).sqrt()
        if eps: denom += eps
        if beta: denom = F.softplus(denom, beta)
        p.data.addcdiv_(grad_avg, denom, value = -lr*v / debias1)
    else: p.data.add_(grad_avg, alpha=-lr / debias1)
    return p

radam_step._defaults = dict(eps=1e-5)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def RAdam(params, lr, mom=0.9, sqr_mom=0.99, eps=1e-5, wd=0., beta=0., decouple_wd=True):
    "A `Optimizer` for Adam with `lr`, `mom`, `sqr_mom`, `eps` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), average_sqr_grad, step_stat, radam_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd, beta=beta)

# Cell
def qhadam_step(p, lr, mom, sqr_mom, sqr_avg, nu_1, nu_2, step, grad_avg, eps, **kwargs):
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    p.data.addcdiv_(((1-nu_1) * p.grad.data) + (nu_1 * (grad_avg / debias1)),
                    (((1 - nu_2) * (p.grad.data)**2) + (nu_2 * (sqr_avg / debias2))).sqrt() + eps,
                    value = -lr)
    return p

qhadam_step._defaults = dict(eps=1e-8)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def QHAdam(params, lr, mom=0.999, sqr_mom=0.999, nu_1=0.7, nu_2 = 1.0, eps=1e-8, wd=0., decouple_wd=True):
    "An `Optimizer` for Adam with `lr`, `mom`, `sqr_mom`, `nus`, eps` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), partial(average_sqr_grad, dampening=True), step_stat, qhadam_step]
    return Optimizer(params, cbs, lr=lr, nu_1=nu_1, nu_2=nu_2 ,
                     mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd)

# Cell
def larc_layer_lr(p, lr, trust_coeff, wd, eps, clip=True, **kwargs):
    "Computes the local lr before weight decay is applied"
    p_norm,g_norm = torch.norm(p.data),torch.norm(p.grad.data)
    local_lr = lr*trust_coeff * (p_norm) / (g_norm + p_norm * wd + eps)
    return {'local_lr': min(lr, local_lr) if clip else local_lr}

larc_layer_lr.defaults = dict(trust_coeff=0.02, wd=0., eps=1e-8)

# Cell
def larc_step(p, local_lr, grad_avg=None, **kwargs):
    "Step for LARC `local_lr` on `p`"
    p.data.add_(p.grad.data if grad_avg is None else grad_avg, alpha = -local_lr)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def Larc(params, lr, mom=0.9, clip=True, trust_coeff=0.02, eps=1e-8, wd=0., decouple_wd=True):
    "A `Optimizer` for Adam with `lr`, `mom`, `sqr_mom`, `eps` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    if mom!=0.: cbs.append(average_grad)
    cbs += [partial(larc_layer_lr, clip=clip), larc_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, trust_coeff=trust_coeff, eps=eps, wd=wd)

# Cell
def lamb_step(p, lr, mom, step, sqr_mom, grad_avg, sqr_avg, eps, **kwargs):
    "Step for LAMB with `lr` on `p`"
    debias1 = debias(mom,     1-mom,     step)
    debias2 = debias(sqr_mom, 1-sqr_mom, step)
    r1 = p.data.pow(2).mean().sqrt()
    step = (grad_avg/debias1) / ((sqr_avg/debias2).sqrt()+eps)
    r2 = step.pow(2).mean().sqrt()
    q = 1 if r1 == 0 or r2 == 0 else min(r1/r2,10)
    p.data.add_(step, alpha = -lr * q)

lamb_step._defaults = dict(eps=1e-6, wd=0.)

# Cell
@log_args(to_return=True, but_as=Optimizer.__init__)
def Lamb(params, lr, mom=0.9, sqr_mom=0.99, eps=1e-5, wd=0., decouple_wd=True):
    "A `Optimizer` for Adam with `lr`, `mom`, `sqr_mom`, `eps` and `params`"
    cbs = [weight_decay] if decouple_wd else [l2_reg]
    cbs += [partial(average_grad, dampening=True), average_sqr_grad, step_stat, lamb_step]
    return Optimizer(params, cbs, lr=lr, mom=mom, sqr_mom=sqr_mom, eps=eps, wd=wd)

# Cell
@log_args(but='opt')
class Lookahead(Optimizer, GetAttr):
    "Wrap `opt` in a lookahead optimizer"
    _default='opt'
    def __init__(self, opt, k=6, alpha=0.5):
        store_attr('opt,k,alpha')
        self._init_state()

    def step(self):
        if self.slow_weights is None: self._copy_weights()
        self.opt.step()
        self.count += 1
        if self.count%self.k != 0: return
        for slow_pg,fast_pg in zip(self.slow_weights,self.param_lists):
            for slow_p,fast_p in zip(slow_pg,fast_pg):
                slow_p.data.add_(fast_p.data-slow_p.data, alpha=self.alpha)
                fast_p.data.copy_(slow_p.data)

    def clear_state(self):
        self.opt.clear_state()
        self._init_state()

    def state_dict(self):
        state = self.opt.state_dict()
        state.update({'count': self.count, 'slow_weights': self.slow_weights})
        return state

    def load_state_dict(self, sd):
        self.count = sd.pop('count')
        self.slow_weights = sd.pop('slow_weights')
        self.opt.load_state_dict(sd)

    def _init_state(self): self.count,self.slow_weights = 0,None
    def _copy_weights(self): self.slow_weights = L(L(p.clone().detach() for p in pg) for pg in self.param_lists)

    @property
    def param_lists(self): return self.opt.param_lists
    @param_lists.setter
    def param_lists(self, v): self.opt.param_lists = v

# Cell
@delegates(RAdam)
def ranger(p, lr, mom=0.95, wd=0.01, eps=1e-6, **kwargs):
    "Convenience method for `Lookahead` with `RAdam`"
    return Lookahead(RAdam(p, lr=lr, mom=mom, wd=wd, eps=eps, **kwargs))

# Cell
def detuplify_pg(d):
    res = {}
    for k,v in d.items():
        if k == 'params': continue
        if is_listy(v): res.update(**{f'{k}__{i}': v_ for i,v_ in enumerate(v)})
        else: res[k] = v
    return res

# Cell
def set_item_pg(pg, k, v):
    if '__' not in k: pg[k] = v
    else:
        name,idx = k.split('__')
        pg[name] = tuple(v if i==int(idx) else pg[name][i] for i in range_of(pg[name]))
    return pg

# Cell
pytorch_hp_map = {'momentum': 'mom', 'weight_decay': 'wd', 'alpha': 'sqr_mom', 'betas__0': 'mom', 'betas__1': 'sqr_mom'}

# Cell
class OptimWrapper(_BaseOptimizer, GetAttr):
    _xtra=['zero_grad', 'step', 'state_dict', 'load_state_dict']
    _default='opt'
    def __init__(self, opt, hp_map=None):
        self.opt = opt
        if hp_map is None: hp_map = pytorch_hp_map
        self.fwd_map = {k: hp_map[k] if k in hp_map else k for k in detuplify_pg(opt.param_groups[0]).keys()}
        self.bwd_map = {v:k for k,v in self.fwd_map.items()}
        self.state = defaultdict(dict, {})
        self.frozen_idx = 0

    @property
    def hypers(self):
        return [{self.fwd_map[k]:v for k,v in detuplify_pg(pg).items() if k != 'params'} for pg in self.opt.param_groups]

    def _set_hyper(self, k, v):
        for pg,v_ in zip(self.opt.param_groups,v): pg = set_item_pg(pg, self.bwd_map[k], v_)

    def clear_state(self): self.opt.state = defaultdict(dict, {})

    @property
    def param_lists(self): return [pg['params'] for pg in self.opt.param_groups]
    @param_lists.setter
    def param_lists(self, v):
        for pg,v_ in zip(self.opt.param_groups,v): pg['params'] = v_