import os
import sys
import typing
import atexit
import signal

# from functools import lru_cache as cached

import yaml

import pypigeonhole_config.ioc_conf as ioc_conf
import pypigeonhole_config.ioc_container as ioc_container
import pypigeonhole_simple_utils.extra.simple_yaml as simple_yaml


# @cached(maxsize=None, typed=False)
def get_sys_args_map(list_of_parameters: list):
    ret = {}
    for arg in list_of_parameters:
        if arg.startswith('-E'):
            param_str = arg[2:]
            idx = param_str.find('=')
            if idx > 0:
                key = param_str[0:idx]
                value = param_str[idx+1:]
                ret[key] = value
    return ret


# @cached(maxsize=None, typed=False)
# def get_ap_args_map(args):
#     ret = {}
#     for arg in vars(args):
#         value = getattr(args, arg)
#         ret[arg] = value
#
#     return ret


# a decorator to collect all factories
class IocRegister:
    factory_list = []

    def __call__(self, *args, **kwargs):
        factory = args[0]
        self.factory_list.append(factory)


ioc_register = IocRegister


T = typing.TypeVar('T')


class IocContext:
    def __init__(self, name, crypto=None, sys_args: dict = None, file_sep='-', file_suffix='.yaml'):
        self.name = name  # can be used in many places, such as configuration file, log file, etc
        if sys_args is None:
            self._cmd_args = get_sys_args_map(sys.argv)
        else:
            self._cmd_args = sys_args
        self._ioc_settings = ioc_conf.TreePathSecretDict(crypto)
        self._ioc_container = ioc_container.IocContainer()

        self._file_sep = file_sep
        self._file_suffix = file_suffix
        atexit.register(self.close)
        signal.signal(signal.SIGINT, self.close)

    def load_conf_file(self, conf_folder: str, env=''):
        file_name = self.name + self._file_sep + env + self._file_suffix if env else self.name + self._file_suffix
        conf_file = os.path.join(conf_folder, file_name)
        conf_data = simple_yaml.load_file(conf_file, self._cmd_args)

        self._ioc_settings.add_dict(conf_data)
        self._ioc_settings.add_dict(self._cmd_args)

        # now override with environment variables. Don't do this, use ${} to assign values
        # for k, v in self._ioc_settings.to_dict().items():  # get full tree path of each setting
        #     res = os.environ.get(k)
        #     if res:
        #         self._ioc_settings[k] = res

        ioc_conf.set_settings(self._ioc_settings)  # point to singleton. If you don't need, it's fine.

    def add_settings(self, extra_settings: dict):  # use to add command line overrides
        self._ioc_settings.add_dict(extra_settings)

    def load_conf_from_yaml_str(self, yaml_str: str):  # mainly for testing purpose
        conf_data = yaml.safe_load(yaml_str)
        self._ioc_settings.add_dict(conf_data)
        ioc_conf.set_settings(self._ioc_settings)

    def init(self):
        factories = IocRegister.factory_list
        for f in factories:
            f(self._ioc_container)

        self._ioc_container.init()

    def close(self):
        self._ioc_container.destroy()

    def get_obj(self, oid, cls: type(T)) -> T:
        obj = self._ioc_container.get(oid, cls)
        return typing.cast(cls, obj)

    def get_conf(self, key):
        return self._ioc_settings.get(key)


app_context = None


def set_app_context(context: IocContext):
    global app_context
    app_context = context
