# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = ['TEST_IMAGE', 'zip_safe', 'create']

# Cell
from fastai.basics import *
from fastai.vision.all import *

# Cell
TEST_IMAGE = 'images/puppy.jpg'

# Cell
def zip_safe(*args, **kwargs):
  'Raises ValueError is len of items are different. Does not work for generators'
  if len(set([len(o) for o in args])) != 1: raise ValueError('All items should have same length')
  return zip(*args, **kwargs)

# Cell
def _wmean(t:Tensor, w=None, dim=None):
  'Weighted mean'
  if w is None: return t.mean(dim=dim)
  w = tensor(w, device=t.device)
  assert w.sum(dim).mean() == 1., 'weights must sum to 1'
  if dim is not None:
    set_trace()
    assert len(w) == t.shape[dim], 'weights must have the same number of items as chosen dimension'
    sz = torch.ones(len(t.shape), dtype=int)
    sz[dim] = t.shape[dim]
  else:
    assert len(w) == torch.prod(tensor(t.shape))
    sz = t.shape
  w = w.reshape(*sz)
  if dim is not None:  return (w*t).sum(dim=dim) #TODO: dim=None gives error
  else:                return (w*t).sum()

# Cell
@patch
@delegates(_wmean)
def wmean(self:Tensor, w, **kwargs): return _wmean(self, w, **kwargs)

# Cell
@patch_to(TensorImage)
def create(fn) -> TensorImage:
  pipe = Pipeline([PILImage.create, ToTensor(), IntToFloatTensor()])
  return pipe(fn).to(default_device())