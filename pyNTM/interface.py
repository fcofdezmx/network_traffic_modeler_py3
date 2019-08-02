"""An object representing a Node interface"""

from .exceptions import ModelException
from .rsvp import RSVP_LSP

class Interface(object):
    """An object representing a Node interface"""

    def __init__(self, name, cost, capacity, node_object, remote_node_object,
                 address=0):
        self.name = name
        self.cost = cost
        self.capacity = capacity
        self.node_object = node_object
        self.remote_node_object = remote_node_object
        self.address = address
        self.traffic = 0.0
        self._failed = False
        self.reserved_bandwidth = 0

        # Validate cost and capacity values
        if not (isinstance(cost, (int, float))):
            raise ValueError('Cost must be positive integer or float')
        if not (isinstance(capacity, (int, float))):
            raise ValueError('Capacity must be positive integer or float')

    @property
    def _key(self):
        """Unique ID for interface object"""
        return (self.name, self.node_object.name)

    # Modify the __hash__ and __eq__ methods to make comparisons easier
    def __eq__(self, other_object):
        if not isinstance(other_object, Interface):
            return NotImplemented

        return [self.node_object, self.remote_node_object, self.name,
                self.capacity, self.address] == [other_object.node_object,
                                                 other_object.remote_node_object, other_object.name,
                                                 other_object.capacity, other_object.address]
        # return self.__dict__ == other_object.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return '%s(name = %r, cost = %s, capacity = %s, node_object = %r, \
remote_node_object = %r, address = %r)' % (self.__class__.__name__,
                                           self.name,
                                           self.cost,
                                           self.capacity,
                                           self.node_object,
                                           self.remote_node_object,
                                           self.address)

    @property
    def reservable_bandwidth(self):
        """Amount of bandwidth available for rsvp lsp reservation"""
        return self.capacity - self.reserved_bandwidth

    # @property
    # def reserved_bandwidth(self):
    #     """
    #     Amount of bandwidth reserved by RSVP LSPs
    #     :return: reserved bandwidth
    #     """
    #     return self._reserved_bandwidth
    #
    # @reserved_bandwidth.setter
    # def reserved_bandwidth(self):
    #     """
    #     Setter for reserved_bandwidth property
    #     :return:
    #     """

    @property
    def failed(self):
        """
        Is Interface failed
        :return: True|False
        """
        return self._failed

    @failed.setter
    def failed(self, status):
        """
        Puts logical guardrails on conditions of interface failure status
        :param status: boolean; input by user
        :return: self._failed; boolean
        """
        if not (isinstance(status, bool)):
            raise ModelException('must be boolean value')

        if not status:

            # Check to see if both nodes are failed = False
            if self.node_object.failed == False and \
                    self.remote_node_object.failed == False:
                self._failed = False

            else:
                self._failed = True
                self.reserved_bandwidth = 0

        else:
            self._failed = True
            self.reserved_bandwidth = 0

    # Put some guardrails on cost
    # def get_cost(self):
    #     return self._cost
    #
    # def set_cost(self, cost):
    #     if cost < 1:
    #         raise ModelException("Interface cost cannot be less than 1")
    #     self._cost = cost
    #
    # cost = property(get_cost, set_cost)
    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost):
        if cost < 1:
            raise ModelException("Interface cost cannot be less than 1")
        self._cost = cost

    # Put some guardrails on capacity
    # def get_capacity(self):
    #     return self._capacity
    #
    # def set_capacity(self, capacity):
    #     if not(capacity > 0):
    #         raise ModelException("Interface capacity must be greater than 0")
    #     self._capacity = capacity
    #
    # capacity = property(get_capacity, set_capacity)
    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        if not(capacity > 0):
            raise ModelException("Interface capacity must be greater than 0")
        self._capacity = capacity

    def fail_interface(self, model):
        """Returns an updated model with the specified
        interface and the remote interface with failed==True
        """

        # find the remote interface
        remote_interface = Interface.get_remote_interface(self, model)

        # set the 2 interfaces to failed = True
        self.failed = True
        remote_interface.failed = True

    def unfail_interface(self, model):
        """Returns an updated network_interfaces table with the specified
        interface and the remote interface in the 'failed': False state
        """

        # find the remote interface
        remote_interface = Interface.get_remote_interface(self, model)

        # check to see if the local and remote node are failed
        if self.node_object.failed == False and \
                self.remote_node_object.failed == False:

            # set the 2 interfaces to failed = False
            self.failed = False
            remote_interface.failed = False
        else:
            message = ("Local and/or remote node are failed; cannot have "
                       "unfailed interface on failed node")
            raise ModelException(message)

    def get_remote_interface(self, model):
        """Searches the model and returns the remote interface"""

        for interface in (interface for interface in model.interface_objects):
            if interface.node_object.name == self.remote_node_object.name and \
                    interface.address == self.address:
                remote_interface = interface
                break

        # sanity check
        if remote_interface.remote_node_object.interfaces(model) == \
                self.node_object.interfaces(model):
            return remote_interface
        else:
            message = 'Internal Validation Error', remote_interface, \
                      'and', self, 'fail validation checks'
            raise ModelException(message)

    def get_circuit_object(self, model):
        """Returns the circuit object from the model that an
        interface is associated with."""

        ckt = model.get_circuit_object_from_interface(self.name,
                                                      self.node_object.name)

        return ckt

    def demands(self, model):
        """Returns list of demands that egress the interface"""
        dmd_set = set()
        demands = (demand for demand in model.demand_objects)
        for demand in demands:

            # Counter for total number of paths for each demand
            # num_paths = 0
            if demand.path != 'Unrouted':
                for dmd_path in demand.path:
                    # If dmd_path is an RSVP LSP and self is in dmd_path.path['interfaces'] ,
                    # look at the LSP path and get demands on the LSP and add them to dmd_set
                    if isinstance(dmd_path, RSVP_LSP):
                        if self in dmd_path.path['interfaces']:
                            dmd_set.add(demand)

                    # If path is not an LSP, then it's a list of Interface
                    # objects; look for self in dmd_path

                    elif self in dmd_path:
                        # num_paths += 1
                        dmd_set.add(demand)

        dmd_list = list(dmd_set)

        # TODO - add % of each demand that is on the interface next to the demand

        return dmd_list

    def lsps(self, model):
        """
        Returns a list of RSVP LSPs that egress the interface
        :param model: Model object
        :return: list of RSVP LSPs that egress the interface
        """

        lsp_set = set()

        for lsp in (lsp for lsp in model.rsvp_lsp_objects if 'Unrouted' not in lsp.path):
            if self in lsp.path['interfaces']:
                lsp_set.add(lsp)

        lsp_list = list(lsp_set)
        return lsp_list

    @property
    def utilization(self):
        """Returns utilization = (self.traffic/self.capacity)*100% """
        if self.traffic == 'Down':
            return 'Int is down'
        else:
            return self.traffic / self.capacity