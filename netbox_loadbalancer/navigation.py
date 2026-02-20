"""Navigation menu configuration for the netbox_loadbalancer plugin.

Defines the sidebar menu structure with links to list views for all four models.
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
