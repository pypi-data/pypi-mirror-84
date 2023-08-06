import os

import pypigeonhole_simple_utils.simple.simple_log as slog

logger = slog.get_logger('__name__')


def _chain_with(sep='.', *args):
    if args[0] == '':
        return sep.join((args[1:]))
    else:
        return sep.join(args)


###############################################################################
# Tree structured key value pair store. Value are stored at leaf nodes only.
# Intermediate nodes are for paths only.
###############################################################################
class TreePathSecretDict:
    # we include crypto because we don't want to show secrets in print or log.
    def __init__(self, crypto=None, tree_path_sep='.', secret_prefix='secret='):
        self._tree_path_sep = tree_path_sep
        self._secret_prefix = secret_prefix
        self._crypto = crypto
        self._data_dict = {}

    def get(self, key, default=None):
        nodes = key.split(self._tree_path_sep)

        data = self._data_dict
        for node in nodes:  # walk down tree path nodes
            data = data.get(node, None)  # do not return default here.
            if not data:
                ret = os.environ.get(key)  # if dict does not have it, check env
                if ret:
                    return ret

                return default  # return default only at the end.

        if type(data) is str and data.startswith(self._secret_prefix) and self._crypto:
            value = data[len(self._secret_prefix):]
            return self._crypto.decrypt_secret(value)
        else:
            return data

    def set(self, key, value):
        nodes = key.split(self._tree_path_sep)
        last = len(nodes) - 1
        data = self._data_dict
        for idx, node in enumerate(nodes):
            if idx == last:
                data[node] = value
            else:  # build tree_path down
                next_data = data.get(node, None)
                if not next_data:
                    next_data = self._new_empty_copy()
                    data[node] = next_data

                data = next_data._data_dict

    # dict syntax [], no bomb out with default None
    def __getitem__(self, key):
        return self.get(key, None)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __len__(self):
        tree_path_dict = self.to_dict()
        return len(tree_path_dict)

    def __repr__(self):
        return 'TreePathSecretDict={{sep={}, secret_prefix={}, crypto={}, key_value_pairs={}}}'.format(
            self._tree_path_sep, self._secret_prefix, self._crypto, repr(self._data_dict)
        )

    def merge(self, tree_path_secret_dict: 'TreePathSecretDict'):
        TreePathSecretDict._merge_dicts(self._data_dict, tree_path_secret_dict._data_dict)
        return self

    def add_dict(self, data_dict: dict):
        # assume dict is flattened data, treepath -> value
        self._add_dict('', data_dict)

        return self

    def _add_dict(self, key, data_dict: dict):
        for k, v in data_dict.items():
            kk = _chain_with(self._tree_path_sep, key, k)
            if isinstance(v, dict):
                self._add_dict(kk, v)
            else:
                self.set(kk, v)

    def to_dict(self) -> dict:
        # flatten tree to treepath -> value
        return TreePathSecretDict._to_dict_with_segs('', self._data_dict, self._tree_path_sep)

    def _new_empty_copy(self) -> 'TreePathSecretDict':
        return TreePathSecretDict(self._crypto, self._tree_path_sep, self._secret_prefix)

    # these methods reference internal data dict, so they stay in this class.
    @staticmethod
    def _merge_dicts(dict1: dict, dict2: dict):
        for k, v in dict2.items():
            if k in dict1:
                u = dict1[k]
                if isinstance(u, TreePathSecretDict) and isinstance(v, TreePathSecretDict):
                    TreePathSecretDict._merge_dicts(u._data_dict, v._data_dict)
                else:
                    if isinstance(u, TreePathSecretDict) and not isinstance(v, TreePathSecretDict):
                        raise Exception('not allowed to override path: {} with value {}'.format(u, v))
                    elif not isinstance(u, TreePathSecretDict) and isinstance(v, TreePathSecretDict):
                        raise Exception('not allowed to override value: {} with path: {}'.format(u, v))
                    else:
                        dict1[k] = v  # override dict1's value
            else:
                dict1[k] = v  # shallow copy

    @staticmethod
    def _to_dict_with_segs(seg_prefix: str, data_dict: dict, seg_sep) -> dict:
        # this is mind twisting, recursion. This is deep copying until values.
        # do not deep-copy values, that's not the concern here. Do it elsewhere.
        ret = {}
        for k, v in data_dict.items():
            if isinstance(v, TreePathSecretDict):
                deep_dict = TreePathSecretDict._to_dict_with_segs(_chain_with(seg_sep, seg_prefix, k),
                                                                  v._data_dict, seg_sep)
                for kk, vv in deep_dict.items():
                    ret[_chain_with(seg_sep, seg_prefix, kk)] = vv
            else:
                ret[_chain_with(seg_sep, seg_prefix, k)] = v

        return ret


# This is the optional single entry point, similar to singleton. This is used
# mainly by the framework. Callers in general do not need this. They should use
# top level IoC context to access this.
ioc_setting = None  # syntax sugar, set by below


def set_settings(setting_store: TreePathSecretDict):
    global ioc_setting
    ioc_setting = setting_store
