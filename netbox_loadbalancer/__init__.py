"""NetBox plugin for managing load balancers, virtual servers, pools, and pool members."""

from netbox.plugins import PluginConfig


class NetBoxLoadBalancerConfig(PluginConfig):
    """Plugin configuration for netbox_loadbalancer."""
    name = 'netbox_loadbalancer'
    verbose_name = 'Load Balancer'
    description = 'Manage load balancers, virtual servers, pools, and pool members'
    version = '0.1.0'
    author = 'David Johnnes'
    author_email = 'david.johnnes@gmail.com'
    base_url = 'loadbalancer'
    min_version = '4.0.0'


config = NetBoxLoadBalancerConfig
