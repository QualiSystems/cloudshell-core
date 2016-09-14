class ConnectionParams(object):
    def __init__(self, type='', vlanId='', mode='', vlan_service_attributes=[]):
        self.type = type
        self.vlanId = vlanId
        self.mode = mode
        self.vlanServiceAttributes= vlan_service_attributes
        self.type='setVlanParameter'