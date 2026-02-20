"""Navigation menu configuration for the netbox_loadbalancer plugin.

Defines the sidebar menu structure that appears under the "Load Balancer" section
in NetBox's navigation bar. The ``menu`` module-level variable is automatically
discovered by NetBox because the plugin's PluginConfig class inherits the default
``menu`` attribute name.

The menu is organised into groups. Each ``PluginMenuItem`` specifies a ``link``
(a Django URL name that resolves to the list view) and ``link_text`` (the label
displayed in the menu). The URL names follow the pattern
``plugins:<plugin_name>:<model_name>_list``.
"""

from netbox.plugins import PluginMenu, PluginMenuItem


menu = PluginMenu(
    label='Load Balancer',
    groups=(
        (
            'Load Balancing',
            (
                PluginMenuItem(
                    link='plugins:netbox_loadbalancer:loadbalancer_list',
                    link_text='Load Balancers',
                ),
                PluginMenuItem(
                    link='plugins:netbox_loadbalancer:virtualserver_list',
                    link_text='Virtual Servers',
                ),
                PluginMenuItem(
                    link='plugins:netbox_loadbalancer:pool_list',
                    link_text='Pools',
                ),
                PluginMenuItem(
                    link='plugins:netbox_loadbalancer:poolmember_list',
                    link_text='Pool Members',
                ),
            ),
        ),
    ),
)
