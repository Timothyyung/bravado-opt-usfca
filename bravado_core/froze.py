from six import iteritems
from frozendict import frozendict

def to_frozen(raw_spec):
    if isinstance(raw_spec, dict):
        pre_frozen_spec = {}
        for k,v in iteritems(raw_spec):
            if isinstance(v, list):
                temp = []
                for item in v:
                    item = to_frozen(item)
                    temp.append(item)
                temp = tuple(temp)
                pre_frozen_spec[k] = temp
            elif isinstance(v, dict):
                temp = {}
                for key,item in iteritems(v):
                    item = to_frozen(item)
                    temp[key] = item
                temp = frozendict(temp)
                pre_frozen_spec[k] = temp
            else:
                pre_frozen_spec[k] = v
        return frozendict(pre_frozen_spec)
    elif isinstance(raw_spec, list):
        pre_frozen_spec = []
        for v in raw_spec:
            if isinstance(v, list):
                temp = []
                for item in v:
                    item = to_frozen(item)
                    temp.append(item)
                temp = tuple(temp)
                pre_frozen_spec.append(temp)
            elif isinstance(v, dict):
                temp = {}
                for key,item in iteritems(v):
                    item = to_frozen(item)
                    temp[key] = item
                temp = frozendict(temp)
                pre_frozen_spec.append(temp)
            else:
                pre_frozen_spec.append(v)
        return tuple(pre_frozen_spec)
    else:
        return raw_spec

def test():
    dict = frozendict({'small':'small'})
    dict_super = frozendict({'big':'big'})
    # dict_super = dict_super.copy(key=dict)
    # dict_super['small'].append('small')
    print(hash(dict_super))
