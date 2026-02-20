"""Table definitions for rendering load balancer objects in list views."""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns

from .models import LoadBalancer, VirtualServer, Pool, PoolMember


class LoadBalancerTable(NetBoxTable):
    """Table for displaying load balancers with linkified name, device, site, and tenant columns."""

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
    """Table for displaying pools with a linked member count column."""

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
    """Table for displaying virtual servers with linkified name, load balancer, VIP, and pool columns."""

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
    """Table for displaying pool members with linkified name, pool, IP, and device columns."""

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
