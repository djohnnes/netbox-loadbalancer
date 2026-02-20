"""Filter sets for querying and filtering load balancer objects in list views and the API."""

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
    """Filters load balancers by platform, status, device, site, and tenant."""

    platform = django_filters.MultipleChoiceFilter(choices=LoadBalancerPlatformChoices)
    status = django_filters.MultipleChoiceFilter(choices=LoadBalancerStatusChoices)

    class Meta:
        model = LoadBalancer
        fields = ('id', 'name', 'platform', 'status', 'device_id', 'site_id', 'tenant_id')

    def search(self, queryset, name, value):
        """Filter by name using case-insensitive containment."""
        return queryset.filter(name__icontains=value)


class PoolFilterSet(NetBoxModelFilterSet):
    """Filters pools by load balancer, method, and protocol."""

    loadbalancer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=LoadBalancer.objects.all(),
    )
    method = django_filters.MultipleChoiceFilter(choices=PoolMethodChoices)
    protocol = django_filters.MultipleChoiceFilter(choices=PoolProtocolChoices)

    class Meta:
        model = Pool
        fields = ('id', 'name', 'loadbalancer_id', 'method', 'protocol')

    def search(self, queryset, name, value):
        """Filter by name using case-insensitive containment."""
        return queryset.filter(name__icontains=value)


class VirtualServerFilterSet(NetBoxModelFilterSet):
    """Filters virtual servers by load balancer, status, protocol, pool, and tenant."""

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
        """Filter by name using case-insensitive containment."""
        return queryset.filter(name__icontains=value)


class PoolMemberFilterSet(NetBoxModelFilterSet):
    """Filters pool members by pool, status, device, IP address, port, weight, and priority."""

    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Pool.objects.all(),
    )
    status = django_filters.MultipleChoiceFilter(choices=PoolMemberStatusChoices)

    class Meta:
        model = PoolMember
        fields = ('id', 'name', 'pool_id', 'ip_address_id', 'device_id', 'port', 'weight', 'priority', 'status')

    def search(self, queryset, name, value):
        """Filter by name using case-insensitive containment."""
        return queryset.filter(name__icontains=value)
