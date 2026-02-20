"""NetBox plugin for managing load balancers, virtual servers, pools, and pool members.

This is the plugin entry point. NetBox discovers plugins by looking for a module-level
``config`` variable that points to a PluginConfig subclass. The PluginConfig class
declares metadata (name, version, author) and settings (base_url, min_version) that
NetBox uses when loading the plugin.

When NetBox starts, it imports this module, reads the ``config`` variable, and uses it
to register the plugin's models, views, API endpoints, navigation menu, and search
indexes — all of which are defined in sibling modules within this package.
"""

from netbox.plugins import PluginConfig


class NetBoxLoadBalancerConfig(PluginConfig):
    """Declares plugin metadata and compatibility requirements.

    NetBox reads these attributes at startup to register the plugin. The ``name``
    must match the Python package name (``netbox_loadbalancer``). The ``base_url``
    determines the URL prefix for all plugin views (e.g. ``/plugins/loadbalancer/``).
    The ``min_version`` prevents the plugin from loading on incompatible NetBox releases.
    """
    name = 'netbox_loadbalancer'
    verbose_name = 'Load Balancer'
    description = 'Manage load balancers, virtual servers, pools, and pool members'
    version = '0.1.0'
    author = 'David Johnnes'
    author_email = 'david.johnnes@gmail.com'
    base_url = 'loadbalancer'
    min_version = '4.0.0'


config = NetBoxLoadBalancerConfig
