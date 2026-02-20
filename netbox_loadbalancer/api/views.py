"""REST API viewsets for the netbox_loadbalancer plugin.

Each viewset provides full CRUD operations and filtering for its respective model.
"""

from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet

from ..models import LoadBalancer, VirtualServer, Pool, PoolMember
from ..filtersets import (
    LoadBalancerFilterSet, VirtualServerFilterSet, PoolFilterSet, PoolMemberFilterSet,
)
from .serializers import (
    LoadBalancerSerializer, VirtualServerSerializer, PoolSerializer, PoolMemberSerializer,
)


class LoadBalancerViewSet(NetBoxModelViewSet):
    """API endpoint for managing load balancers."""
    queryset = LoadBalancer.objects.all()
    serializer_class = LoadBalancerSerializer
    filterset_class = LoadBalancerFilterSet


class PoolViewSet(NetBoxModelViewSet):
    """API endpoint for managing pools. The queryset includes an annotated member count."""
    queryset = Pool.objects.annotate(member_count=Count('members'))
    serializer_class = PoolSerializer
    filterset_class = PoolFilterSet


class VirtualServerViewSet(NetBoxModelViewSet):
    """API endpoint for managing virtual servers."""
    queryset = VirtualServer.objects.all()
    serializer_class = VirtualServerSerializer
    filterset_class = VirtualServerFilterSet


class PoolMemberViewSet(NetBoxModelViewSet):
    """API endpoint for managing pool members."""
    queryset = PoolMember.objects.all()
    serializer_class = PoolMemberSerializer
    filterset_class = PoolMemberFilterSet
