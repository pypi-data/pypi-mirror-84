# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/45_collab.ipynb (unless otherwise specified).

__all__ = ['TabularCollab', 'CollabDataLoaders', 'EmbeddingDotBias', 'EmbeddingNN', 'collab_learner']

# Cell
from .tabular.all import *

# Cell
class TabularCollab(TabularPandas):
    "Instance of `TabularPandas` suitable for collaborative filtering (with no continuous variable)"
    with_cont=False

# Cell
class CollabDataLoaders(DataLoaders):
    "Base `DataLoaders` for collaborative filtering."
    @delegates(DataLoaders.from_dblock)
    @classmethod
    def from_df(cls, ratings, valid_pct=0.2, user_name=None, item_name=None, rating_name=None, seed=None, path='.', **kwargs):
        "Create a `DataLoaders` suitable for collaborative filtering from `ratings`."
        user_name   = ifnone(user_name,   ratings.columns[0])
        item_name   = ifnone(item_name,   ratings.columns[1])
        rating_name = ifnone(rating_name, ratings.columns[2])
        cat_names = [user_name,item_name]
        splits = RandomSplitter(valid_pct=valid_pct, seed=seed)(range_of(ratings))
        to = TabularCollab(ratings, [Categorify], cat_names, y_names=[rating_name], y_block=TransformBlock(), splits=splits)
        return to.dataloaders(path=path, **kwargs)

    @classmethod
    def from_csv(cls, csv, **kwargs):
        "Create a `DataLoaders` suitable for collaborative filtering from `csv`."
        return cls.from_df(pd.read_csv(csv), **kwargs)

CollabDataLoaders.from_csv = delegates(to=CollabDataLoaders.from_df)(CollabDataLoaders.from_csv)

# Cell
class EmbeddingDotBias(Module):
    "Base dot model for collaborative filtering."
    def __init__(self, n_factors, n_users, n_items, y_range=None):
        self.y_range = y_range
        (self.u_weight, self.i_weight, self.u_bias, self.i_bias) = [Embedding(*o) for o in [
            (n_users, n_factors), (n_items, n_factors), (n_users,1), (n_items,1)
        ]]

    def forward(self, x):
        users,items = x[:,0],x[:,1]
        dot = self.u_weight(users)* self.i_weight(items)
        res = dot.sum(1) + self.u_bias(users).squeeze() + self.i_bias(items).squeeze()
        if self.y_range is None: return res
        return torch.sigmoid(res) * (self.y_range[1]-self.y_range[0]) + self.y_range[0]

    @classmethod
    def from_classes(cls, n_factors, classes, user=None, item=None, y_range=None):
        "Build a model with `n_factors` by inferring `n_users` and  `n_items` from `classes`"
        if user is None: user = list(classes.keys())[0]
        if item is None: item = list(classes.keys())[1]
        res = cls(n_factors, len(classes[user]), len(classes[item]), y_range=y_range)
        res.classes,res.user,res.item = classes,user,item
        return res

    def _get_idx(self, arr, is_item=True):
        "Fetch item or user (based on `is_item`) for all in `arr`"
        assert hasattr(self, 'classes'), "Build your model with `EmbeddingDotBias.from_classes` to use this functionality."
        classes = self.classes[self.item] if is_item else self.classes[self.user]
        c2i = {v:k for k,v in enumerate(classes)}
        try: return tensor([c2i[o] for o in arr])
        except Exception as e:
            print(f"""You're trying to access {'an item' if is_item else 'a user'} that isn't in the training data.
                  If it was in your original data, it may have been split such that it's only in the validation set now.""")

    def bias(self, arr, is_item=True):
        "Bias for item or user (based on `is_item`) for all in `arr`"
        idx = self._get_idx(arr, is_item)
        layer = (self.i_bias if is_item else self.u_bias).eval().cpu()
        return to_detach(layer(idx).squeeze(),gather=False)

    def weight(self, arr, is_item=True):
        "Weight for item or user (based on `is_item`) for all in `arr`"
        idx = self._get_idx(arr, is_item)
        layer = (self.i_weight if is_item else self.u_weight).eval().cpu()
        return to_detach(layer(idx),gather=False)

# Cell
class EmbeddingNN(TabularModel):
    "Subclass `TabularModel` to create a NN suitable for collaborative filtering."
    @delegates(TabularModel.__init__)
    def __init__(self, emb_szs, layers, **kwargs):
        super().__init__(emb_szs=emb_szs, n_cont=0, out_sz=1, layers=layers, **kwargs)

# Cell
@log_args(to_return=True, but_as=Learner.__init__)
@delegates(Learner.__init__)
def collab_learner(dls, n_factors=50, use_nn=False, emb_szs=None, layers=None, config=None, y_range=None, loss_func=None, **kwargs):
    "Create a Learner for collaborative filtering on `dls`."
    emb_szs = get_emb_sz(dls, ifnone(emb_szs, {}))
    if loss_func is None: loss_func = MSELossFlat()
    if config is None: config = tabular_config()
    if y_range is not None: config['y_range'] = y_range
    if layers is None: layers = [n_factors]
    if use_nn: model = EmbeddingNN(emb_szs=emb_szs, layers=layers, **config)
    else:      model = EmbeddingDotBias.from_classes(n_factors, dls.classes, y_range=y_range)
    return Learner(dls, model, loss_func=loss_func, **kwargs)