"""Search indexes for the netbox_loadbalancer plugin.

Registers each model with NetBox's global search system so that load balancer objects
are discoverable via the search bar at the top of every NetBox page.

Each ``SearchIndex`` subclass defines a ``fields`` tuple of ``(field_name, weight)``
pairs. The weight is a positive integer that controls search result ranking — lower
numbers indicate higher priority. For example, a weight of 100 on the ``name`` field
means name matches are ranked higher than description matches (weight 500).

The ``@register_search`` decorator adds the index to NetBox's search registry at
import time, so the plugin's objects appear in global search results automatically.
"""

from netbox.search import SearchIndex, register_search

from .models import LoadBalancer, VirtualServer, Pool, PoolMember


@register_search
class LoadBalancerIndex(SearchIndex):
    """Indexes load balancer name (weight 100) and description (weight 500) for global search.

    A search for "prod" would match a load balancer named "Production-LB-01" with
    high priority, or one with "production environment" in its description with lower
    priority.
    """
    model = LoadBalancer
    fields = (
        ('name', 100),
        ('description', 500),
    )


@register_search
class PoolIndex(SearchIndex):
    """Indexes pool name (weight 100) and description (weight 500) for global search."""
    model = Pool
    fields = (
        ('name', 100),
        ('description', 500),
    )


@register_search
class VirtualServerIndex(SearchIndex):
    """Indexes virtual server name (weight 100) and description (weight 500) for global search."""
    model = VirtualServer
    fields = (
        ('name', 100),
        ('description', 500),
    )


@register_search
class PoolMemberIndex(SearchIndex):
    """Indexes pool member name (weight 100) and description (weight 500) for global search."""
    model = PoolMember
    fields = (
        ('name', 100),
        ('description', 500),
    )
