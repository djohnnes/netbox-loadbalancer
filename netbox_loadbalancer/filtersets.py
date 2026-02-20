"""Filter sets for querying and filtering load balancer objects.

Each FilterSet class defines the fields that can be used to filter a model's queryset
in both the web UI list views and the REST API. They extend NetBox's
``NetBoxModelFilterSet``, which provides built-in support for tags, custom fields,
and the ``q`` search parameter.

Filter types used:
- ``MultipleChoiceFilter``: allows filtering by one or more choice values
  (e.g. ``?status=active&status=planned``).
- ``ModelMultipleChoiceFilter``: allows filtering by one or more related object IDs
  (e.g. ``?loadbalancer_id=1&loadbalancer_id=2``).

The ``search()`` method on each FilterSet handles the ``q`` parameter from the search
box on list views. It defines which model fields are searched when a user types a
free-text query.
"""

import django_filters
from netbox.filtersets import NetBoxModelFilterSet

from .models import LoadBalancer, VirtualServer, Pool, PoolMember
from .choices import (
    LoadBalancerPlatformChoices,
    LoadBalancerStatusChoices,
    VirtualServerStatusChoices,
    VirtualServerProtocolChoices,
    PoolMethodChoices,
    PoolProtocolChoices,
    PoolMemberStatusChoices,
)


class LoadBalancerFilterSet(NetBoxModelFilterSet):
    """Filters load balancers by platform, status, device, site, and tenant.

    The Meta.fields tuple lists all fields that can be filtered via URL query
    parameters. Fields like ``device_id``, ``site_id``, and ``tenant_id`` are
    automatically handled by NetBoxModelFilterSet because they are standard
    ForeignKey fields on the model.
    """

    platform = django_filters.MultipleChoiceFilter(choices=LoadBalancerPlatformChoices)
    status = django_filters.MultipleChoiceFilter(choices=LoadBalancerStatusChoices)

    class Meta:
        model = LoadBalancer
        fields = ('id', 'name', 'platform', 'status', 'device_id', 'site_id', 'tenant_id')

    def search(self, queryset, name, value):
        """Handle the ``q`` search parameter from the list view search box.

        Performs a case-insensitive substring match on the load balancer's name field.
        For example, searching for "prod" would match "Production-LB-01".
        """
        return queryset.filter(name__icontains=value)


class PoolFilterSet(NetBoxModelFilterSet):
    """Filters pools by load balancer, method, and protocol.

    The ``loadbalancer_id`` filter uses ``ModelMultipleChoiceFilter`` which accepts
    one or more load balancer IDs and returns only pools belonging to those load
    balancers.
    """

    loadbalancer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=LoadBalancer.objects.all(),
    )
    method = django_filters.MultipleChoiceFilter(choices=PoolMethodChoices)
    protocol = django_filters.MultipleChoiceFilter(choices=PoolProtocolChoices)

    class Meta:
        model = Pool
        fields = ('id', 'name', 'loadbalancer_id', 'method', 'protocol')

    def search(self, queryset, name, value):
        """Handle the ``q`` search parameter by matching against the pool name."""
        return queryset.filter(name__icontains=value)


class VirtualServerFilterSet(NetBoxModelFilterSet):
    """Filters virtual servers by load balancer, status, protocol, port, pool, and tenant.

    This is the most feature-rich FilterSet in the plugin, reflecting the number of
    filterable attributes on the VirtualServer model. The ``pool_id`` filter allows
    finding all virtual servers that point to a specific pool.
    """

    loadbalancer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=LoadBalancer.objects.all(),
    )
    status = django_filters.MultipleChoiceFilter(choices=VirtualServerStatusChoices)
    protocol = django_filters.MultipleChoiceFilter(choices=VirtualServerProtocolChoices)
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
    )

    class Meta:
        model = VirtualServer
        fields = ('id', 'name', 'loadbalancer_id', 'status', 'protocol', 'port', 'pool_id', 'tenant_id')

    def search(self, queryset, name, value):
        """Handle the ``q`` search parameter by matching against the virtual server name."""
        return queryset.filter(name__icontains=value)


class PoolMemberFilterSet(NetBoxModelFilterSet):
    """Filters pool members by pool, status, device, IP address, port, weight, and priority.

    This FilterSet exposes the widest range of filterable fields, allowing operators
    to find members by their parent pool, operational status, associated device or
    IP, specific port numbers, or weight/priority values.
    """

    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
    )
    status = django_filters.MultipleChoiceFilter(choices=PoolMemberStatusChoices)

    class Meta:
        model = PoolMember
        fields = ('id', 'name', 'pool_id', 'ip_address_id', 'device_id', 'port', 'weight', 'priority', 'status')

    def search(self, queryset, name, value):
        """Handle the ``q`` search parameter by matching against the pool member name."""
        return queryset.filter(name__icontains=value)
