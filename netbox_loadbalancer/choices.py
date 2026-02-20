"""Choice sets for the netbox_loadbalancer plugin.

Each ChoiceSet defines the valid options for a particular model field, such as
platform type, operational status, protocol, or load balancing method.
"""

from utilities.choices import ChoiceSet


class LoadBalancerPlatformChoices(ChoiceSet):
    """Available load balancer platform types (e.g. F5, HAProxy, NGINX)."""
    key = 'LoadBalancer.platform'

    PLATFORM_F5 = 'f5'
    PLATFORM_HAPROXY = 'haproxy'
    PLATFORM_CITRIX = 'citrix'
    PLATFORM_NGINX = 'nginx'
    PLATFORM_AWS = 'aws'
    PLATFORM_AZURE = 'azure'
    PLATFORM_OTHER = 'other'

    CHOICES = [
        (PLATFORM_F5, 'F5 BIG-IP'),
        (PLATFORM_HAPROXY, 'HAProxy'),
        (PLATFORM_CITRIX, 'Citrix ADC'),
        (PLATFORM_NGINX, 'NGINX'),
        (PLATFORM_AWS, 'AWS ELB/ALB'),
        (PLATFORM_AZURE, 'Azure LB'),
        (PLATFORM_OTHER, 'Other'),
    ]


class LoadBalancerStatusChoices(ChoiceSet):
    """Operational status choices for load balancers."""
    key = 'LoadBalancer.status'

    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_DECOMMISSIONED = 'decommissioned'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_MAINTENANCE, 'Maintenance', 'yellow'),
        (STATUS_DECOMMISSIONED, 'Decommissioned', 'gray'),
    ]


class VirtualServerStatusChoices(ChoiceSet):
    """Operational status choices for virtual servers."""
    key = 'VirtualServer.status'

    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_DISABLED = 'disabled'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_DISABLED, 'Disabled', 'red'),
    ]


class VirtualServerProtocolChoices(ChoiceSet):
    """Protocol choices for virtual server listeners."""
    key = 'VirtualServer.protocol'

    PROTOCOL_TCP = 'tcp'
    PROTOCOL_UDP = 'udp'
    PROTOCOL_HTTP = 'http'
    PROTOCOL_HTTPS = 'https'
    PROTOCOL_OTHER = 'other'

    CHOICES = [
        (PROTOCOL_TCP, 'TCP'),
        (PROTOCOL_UDP, 'UDP'),
        (PROTOCOL_HTTP, 'HTTP'),
        (PROTOCOL_HTTPS, 'HTTPS'),
        (PROTOCOL_OTHER, 'Other'),
    ]


class PoolMethodChoices(ChoiceSet):
    """Load balancing algorithm choices for pools."""
    key = 'Pool.method'

    METHOD_ROUND_ROBIN = 'round-robin'
    METHOD_LEAST_CONNECTIONS = 'least-connections'
    METHOD_IP_HASH = 'ip-hash'
    METHOD_WEIGHTED = 'weighted'
    METHOD_OTHER = 'other'

    CHOICES = [
        (METHOD_ROUND_ROBIN, 'Round Robin'),
        (METHOD_LEAST_CONNECTIONS, 'Least Connections'),
        (METHOD_IP_HASH, 'IP Hash'),
        (METHOD_WEIGHTED, 'Weighted'),
        (METHOD_OTHER, 'Other'),
    ]


class PoolProtocolChoices(ChoiceSet):
    """Protocol choices for pool backend traffic."""
    key = 'Pool.protocol'

    PROTOCOL_TCP = 'tcp'
    PROTOCOL_UDP = 'udp'
    PROTOCOL_HTTP = 'http'
    PROTOCOL_HTTPS = 'https'
    PROTOCOL_OTHER = 'other'

    CHOICES = [
        (PROTOCOL_TCP, 'TCP'),
        (PROTOCOL_UDP, 'UDP'),
        (PROTOCOL_HTTP, 'HTTP'),
        (PROTOCOL_HTTPS, 'HTTPS'),
        (PROTOCOL_OTHER, 'Other'),
    ]


class PoolMemberStatusChoices(ChoiceSet):
    """Operational status choices for pool members."""
    key = 'PoolMember.status'

    STATUS_ACTIVE = 'active'
    STATUS_DRAIN = 'drain'
    STATUS_DISABLED = 'disabled'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DRAIN, 'Drain', 'yellow'),
        (STATUS_DISABLED, 'Disabled', 'red'),
    ]
