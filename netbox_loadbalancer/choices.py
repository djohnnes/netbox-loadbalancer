"""Choice sets for the netbox_loadbalancer plugin.

Each class in this module extends NetBox's ``ChoiceSet`` base class to define the
valid options for a CharField on one of the plugin's models. A ChoiceSet works like
a Django choices tuple but adds colour-coded badges in the UI (the optional third
element in each CHOICES entry).

The ``key`` attribute (e.g. ``'LoadBalancer.platform'``) allows NetBox administrators
to override or extend the default choices at runtime through the FIELD_CHOICES
configuration setting, without modifying the plugin source code.

Convention: class constants (e.g. ``STATUS_ACTIVE = 'active'``) are used throughout
the codebase to reference choices by name instead of hardcoding string values.
"""

from utilities.choices import ChoiceSet


class LoadBalancerPlatformChoices(ChoiceSet):
    """Platform types for load balancer appliances.

    Identifies the vendor or technology stack running the load balancer. This is a
    required field on the LoadBalancer model. Common platforms include hardware
    appliances (F5 BIG-IP, Citrix ADC), software-based solutions (HAProxy, NGINX),
    and cloud-native services (AWS ELB/ALB, Azure LB). Use 'Other' for platforms
    not listed here.
    """
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
    """Operational lifecycle status for load balancers.

    Tracks where a load balancer is in its lifecycle: planned (not yet deployed),
    active (in production), maintenance (temporarily offline for work), or
    decommissioned (retired). Each status has an associated colour that is displayed
    as a badge in the NetBox UI.
    """
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
    """Operational status for virtual servers.

    Indicates whether a virtual server is actively accepting traffic (active),
    not yet deployed (planned), or intentionally taken offline (disabled).
    """
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
    """Network protocol that a virtual server listener accepts.

    Determines what kind of traffic the virtual server handles. TCP and UDP are
    layer-4 protocols, while HTTP and HTTPS are layer-7 (application-level).
    The choice of protocol affects how the load balancer inspects and routes traffic.
    """
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
    """Load balancing algorithm used to distribute traffic among pool members.

    - Round Robin: requests are sent to each member in turn, cycling through the list.
    - Least Connections: the member with the fewest active connections gets the next
      request, which is useful when request processing times vary.
    - IP Hash: the client's source IP determines which member receives the request,
      providing session persistence (sticky sessions).
    - Weighted: traffic is distributed proportionally based on each member's weight
      value, allowing more powerful servers to handle more traffic.
    """
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
    """Network protocol used for communication between the load balancer and pool members.

    This may differ from the virtual server's protocol. For example, a virtual server
    might accept HTTPS traffic from clients while the pool communicates with backend
    members over plain HTTP (SSL offloading).
    """
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
    """Operational status for individual pool members.

    - Active: the member is healthy and receiving new traffic.
    - Drain: the member stops accepting new connections but finishes processing
      existing ones. This is used for graceful removal during maintenance.
    - Disabled: the member is completely offline and receives no traffic at all.
    """
    key = 'PoolMember.status'

    STATUS_ACTIVE = 'active'
    STATUS_DRAIN = 'drain'
    STATUS_DISABLED = 'disabled'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_DRAIN, 'Drain', 'yellow'),
        (STATUS_DISABLED, 'Disabled', 'red'),
    ]
