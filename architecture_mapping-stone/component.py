import json

class Component:
    def __init__(self, id = None, parent = None) -> None:
        self._id = id
        self._parent = parent
        self._type = self.__class__.__name__
        self._children = {}
        self._attr = {}

    def id(self, id = None):
        if id: self._id = id
        return self._id

    def parent(self, parent = None):
        if parent: self._parent = parent
        return self._parent

    def type(self):
        return self._type

    def getAttr(self):
        return self._attr

    def getAttrName(self):
        return self._attr.keys()

    def addChildren(self, nameStr, obj):
        # assert isinstance(nameStr, str), f'nameStr: {nameStr} is {type(nameStr)}'
        assert isinstance(obj, Component), f'obj: {obj} is {type(obj)}'
        # self._children[nameStr] = obj
        self._children.update({nameStr: obj})

    def removeChildren(self, nameStr):
        if nameStr in self._children.keys():
            del self._children[nameStr]
        else: 
            print("There is no such key in children")

    def getChildren(self):
        return self._children

    def getChildrenStr(self):
        return self._children.keys()

    def numOfChildren(self):
        return len(self._children)

    def __str__(self) -> str:
        s = f'Type: {self.type()}; ID: {self.id()};'
        if self.parent():
            s = s + f' Parent: {self.parent().id()}'
        else: s = s + ' Parent: None'
        return s


class Architecture(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)


class Account(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)


class Cluster(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)
        self._attr = {
            'cluster_failed_node_count': None,
            'cluster_node_count': None
        }


class Namespace(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)
        self._attr = {
            'namespace_number_of_running_pods': None
        }
    

class Node(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)
        self._attr = {
            'node_cpu_usage_total': None,
            'node_cpu_utilization': None,
            'node_network_total_bytes': None,
            'node_number_of_running_containers': None,
            'node_number_of_running_pods': None,
            'node_memory_usage': None,
            'node_memory_swap': None
        }


class Pod(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)
        self._attr = {
            'pod_cpu_utilization': None,
            'pod_memory_utilization': None,
            'pod_number_of_container_restarts': None,
            'pod_network_rx_bytes': None,
            'pod_network_tx_bytes': None,
            'pod_cpu_usage_total': None,
            'pod_memory_usage': None,
            'pod_memory_swap': None,
            'pod_memory_max_usage': None
        }


class Container(Component):
    def __init__(self, id=None, parent=None) -> None:
        super().__init__(id, parent)
        self._attr = {
            'container_cpu_utilization': None,
            'container_memory_utilization': None,
            'container_memory_failcnt': None,
            'number_of_container_restarts': None,
            'container_cpu_usage_total': None,
            'container_memory_usage': None,
            'container_memory_swap': None,
            'container_memory_max_usage': None
        }