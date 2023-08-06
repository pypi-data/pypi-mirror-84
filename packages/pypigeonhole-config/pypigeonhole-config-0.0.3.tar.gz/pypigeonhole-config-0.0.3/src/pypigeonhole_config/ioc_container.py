import typing

import pypigeonhole_config.ioc_conf as ioc_conf


class Params:  # syntax sugar so that code is similar to direct constructor call
    def __init__(self, **kwargs):
        self.param_dict = kwargs  # standard dictionary maintains insert order

    def __repr__(self):
        return repr(self.param_dict)


class Registry:
    def __init__(self, oid: str, cls, constr_params: Params, prop_params: Params,
                 initialize, destroy, singleton=True, lazy=False):
        self.oid = oid
        self.cls = cls
        self.constr_params = constr_params
        self.prop_params = prop_params
        self.initialize = initialize
        self.destroy = destroy
        self.singleton = singleton
        self.lazy = lazy

    def __repr__(self):
        ret = "Registry{{oid={}, cls={}, constr_params={}, prop_params={}, " +\
              "initialize={}, destroy={}, singleton={}, lazy= {}}}"
        return ret.format(self.oid, self.cls, self.constr_params, self.prop_params,
                          self.initialize, self.destroy, self.singleton, self.lazy)


# These 2 classes are to distinguish them from literal values / constants
class ObjRef:
    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return 'ObjRef{{key={}}}'.format(self.key)


class ConfRef:
    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return 'ConfRef{{key={}}}'.format(self.key)


T = typing.TypeVar('T')


class IocContainer:
    def __init__(self):
        self._id_registry = {}
        self._id_object = {}

    def register(self, oid: str, cls, constr_params=Params(), prop_params=Params(),
                 initialize=None, destroy=None, singleton=True, lazy=False):
        self._id_registry[oid] = Registry(oid, cls, constr_params, prop_params,
                                          initialize, destroy, singleton, lazy)

    def get(self, oid, cls: type(T)) -> T:
        obj = self._id_object.get(oid, None)
        if obj is None:
            registry = self._id_registry[oid]
            obj = self._get_or_create(registry, False)
            self._set_obj_props(obj, registry)
            if registry.initialize:
                registry.initialize(obj)

        return typing.cast(cls, obj)

    def init(self):
        self._create_objects()
        self._set_props()
        self._init_objects()

    def destroy(self):
        for oid, registry in self._id_registry.items():
            if registry.singleton and registry.destroy:
                obj = self._id_object[oid]
                registry.destroy(obj)

    def _build_dep_trees(self, id_reg_dict: dict):
        # obj -> dependencies, 1 to many
        # dependency used by many objects, 1 to many
        obj_2_parent = {}
        obj_2_child = {}
        for oid, registry in id_reg_dict.items():
            if oid in self._id_object:
                continue

            if registry.lazy or not registry.singleton:
                continue  # we don't pre-create these objects

            dep_list = []  # collect all object references (not literals or settings)
            for k, v in registry.constr_params.param_dict.items():
                if isinstance(v, ObjRef) and v.key not in self._id_object:
                    dep_list.append(v.key)

            obj_2_child[oid] = dep_list

            for dep_oid in dep_list:
                parent_list = obj_2_parent.get(dep_oid, None)
                if not parent_list:
                    parent_list = []
                    obj_2_parent[dep_oid] = parent_list

                parent_list.append(oid)

        return obj_2_child, obj_2_parent

    def _create_objects(self):
        # worst case is linear dependency, like a -> b -> c -> d
        obj_2_child, obj_2_parent = self._build_dep_trees(self._id_registry)
        for oid, registry in self._id_registry.items():
            if oid in self._id_object:
                continue

            if registry.singleton:
                parents = obj_2_parent.get(oid, None)
                if registry.lazy and parents and len(parents) > 0:  # non top level lazy needs to create
                    self._get_or_create(registry, True)
                elif not registry.lazy:
                    self._get_or_create(registry, True)

    def _get_or_create(self, registry: Registry, prebuild: bool, hist=None):
        if hist is None:  # to track dependency path as we walk, prevent cyclic dependency
            hist = set()

        if registry.oid in self._id_object:
            return self._id_object[registry.oid]

        cps = {}
        for k, v in registry.constr_params.param_dict.items():
            if isinstance(v, ObjRef):
                if v.key in hist:
                    raise Exception('cyclic dependency for object {} in path {}'.format(v.key, hist))
                hist1 = hist.copy()
                hist1.add(v.key)
                reg = self._id_registry[v.key]
                if prebuild and reg.singleton:
                    cps[k] = self._get_or_create(reg, prebuild, hist1)  # recursive call
                else:
                    cps[k] = self.get(reg.oid, reg.cls)
            elif isinstance(v, ConfRef):
                cps[k] = ioc_conf.ioc_setting[v.key]
            else:
                cps[k] = v

        res = registry.cls(**cps)  # call constructor

        if registry.singleton:
            self._id_object[registry.oid] = res

        return res

    def _set_props(self):  # set objects without call set_props and init
        for oid, registry in self._id_registry.items():
            obj = self._id_object.get(oid)
            if obj is None:
                continue  # this happens when lazy=true or singleton=false (prototype)
            for k, v in registry.prop_params.param_dict.items():
                if isinstance(v, ObjRef):
                    dereference = self._id_object.get(v.key, None)
                    if not dereference:  # when prototype or lazy
                        dereference = self.get(v.key, self._id_registry[v.key].cls)
                    setattr(obj, k, dereference)
                elif isinstance(v, ConfRef):
                    dereference = ioc_conf.ioc_setting[v.key]
                    setattr(obj, k, dereference)
                else:
                    setattr(obj, k, v)

    def _set_obj_props(self, obj, registry):
        for k, v in registry.prop_params.param_dict.items():
            if isinstance(v, ObjRef):
                dereference = self.get(v.key, registry.cls)
                setattr(obj, k, dereference)
            elif isinstance(v, ConfRef):
                dereference = ioc_conf.ioc_setting[v.key]
                setattr(obj, k, dereference)
            else:
                setattr(obj, k, v)

    def _init_objects(self):
        for oid, registry in self._id_registry.items():
            if registry.initialize:
                obj = self._id_object.get(oid)
                if obj:
                    registry.initialize(obj)


obj_container = None


def set_ioc_container(container: IocContainer):
    global obj_container
    obj_container = container
