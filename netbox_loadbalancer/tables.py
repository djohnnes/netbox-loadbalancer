"""Table definitions for rendering load balancer objects in list views.

Each table class extends ``NetBoxTable`` and defines how a model's data is displayed
in the list view as an HTML table. Key concepts:

- ``linkify=True`` on a Column makes the cell value a clickable link to that object's
  detail view. This is used for the primary name column and for related objects.
- ``ChoiceFieldColumn`` renders choice fields as coloured badges (e.g. a green
  "Active" badge for status fields) instead of plain text.
- ``LinkedCountColumn`` displays an integer count as a hyperlink that navigates to
  a filtered list view showing the related objects.
- ``Meta.fields`` lists all available columns, while ``Meta.default_columns`` controls
  which columns are visible by default (users can customise this in the UI).
"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns

from .models import LoadBalancer, VirtualServer, Pool, PoolMember


class LoadBalancerTable(NetBoxTable):
    """List view table for load balancers.

    The name, device, site, tenant, and management_ip columns are linkified so users
    can click through to the related object's detail page. Platform and status use
    ChoiceFieldColumn to render as coloured badges. Default columns show name, platform,
    status, site, and tenant — additional columns can be toggled by the user.
    """

    name = tables.Column(linkify=True)
    platform = columns.ChoiceFieldColumn()
    status = columns.ChoiceFieldColumn()
    device = tables.Column(linkify=True)
    site = tables.Column(linkify=True)
    tenant = tables.Column(linkify=True)
    management_ip = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = LoadBalancer
        fields = (
            'pk', 'id', 'name', 'platform', 'status', 'device', 'site',
            'tenant', 'management_ip', 'description', 'tags',
        )
        default_columns = ('name', 'platform', 'status', 'site', 'tenant')


class PoolTable(NetBoxTable):
    """List view table for pools.

    Includes a ``member_count`` column using LinkedCountColumn, which displays the
    number of pool members as a clickable link. Clicking the count navigates to the
    pool member list view pre-filtered to show only members belonging to that pool.
    The count is provided by a ``Count('members')`` annotation on the queryset in the
    view (see ``PoolListView``).
    """

    name = tables.Column(linkify=True)
    loadbalancer = tables.Column(linkify=True)
    method = columns.ChoiceFieldColumn()
    protocol = columns.ChoiceFieldColumn()
    member_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_loadbalancer:poolmember_list',
        url_params={'pool_id': 'pk'},
        verbose_name='Members',
    )

    class Meta(NetBoxTable.Meta):
        model = Pool
        fields = (
            'pk', 'id', 'name', 'loadbalancer', 'method', 'protocol',
            'member_count', 'description', 'tags',
        )
        default_columns = ('name', 'loadbalancer', 'method', 'protocol', 'member_count')


class VirtualServerTable(NetBoxTable):
    """List view table for virtual servers.

    Displays the most fields of any table in the plugin, reflecting the virtual
    server's role as the central object connecting load balancers, VIPs, and pools.
    The name, load balancer, IP address, pool, and tenant columns are all linkified.
    Default columns show the most commonly needed fields; port and protocol are
    included to quickly identify the listener configuration.
    """

    name = tables.Column(linkify=True)
    loadbalancer = tables.Column(linkify=True)
    ip_address = tables.Column(linkify=True)
    port = tables.Column()
    protocol = columns.ChoiceFieldColumn()
    status = columns.ChoiceFieldColumn()
    pool = tables.Column(linkify=True)
    tenant = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = VirtualServer
        fields = (
            'pk', 'id', 'name', 'loadbalancer', 'ip_address', 'port',
            'protocol', 'status', 'pool', 'tenant', 'description', 'tags',
        )
        default_columns = ('name', 'loadbalancer', 'ip_address', 'port', 'protocol', 'status', 'pool')


class PoolMemberTable(NetBoxTable):
    """List view table for pool members.

    Shows each member's name, parent pool, IP address, device, port, weight, priority,
    and status. The name, pool, IP, and device columns are linkified. Default columns
    focus on the operational essentials: name, pool, IP, port, weight, and status.
    """

    name = tables.Column(linkify=True)
    pool = tables.Column(linkify=True)
    ip_address = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    port = tables.Column()
    weight = tables.Column()
    priority = tables.Column()
    status = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = PoolMember
        fields = (
            'pk', 'id', 'name', 'pool', 'ip_address', 'device', 'port',
            'weight', 'priority', 'status', 'description', 'tags',
        )
        default_columns = ('name', 'pool', 'ip_address', 'port', 'weight', 'status')
