"""Search indexes for the netbox_loadbalancer plugin.

Registers each model with the global search system so that load balancer objects
are discoverable via the NetBox search bar.
"""

from netbox.search import SearchIndex, register_search

from .models import LoadBalancer, VirtualServer, Pool, PoolMember


@register_search
class LoadBalancerIndex(SearchIndex):
    """Indexes load balancer name and description for global search."""
    model = LoadBalancer
    fields = (
        ('name', 100),
        ('description', 500),
    )


@register_search
class PoolIndex(SearchIndex):
    """Indexes pool name and description for global search."""
    model = Pool
    fields = (
        ('name', 100),
        ('description', 500),
    )


@register_search
class VirtualServerIndex(SearchIndex):
    """Indexes virtual server name and description for global search."""
    model = VirtualServer
    fields = (
        ('name', 100),
        ('description', 500),
    )


@register_search
class PoolMemberIndex(SearchIndex):
    """Indexes pool member name and description for global search."""
    model = PoolMember
    fields = (
        ('name', 100),
        ('description', 500),
    )
