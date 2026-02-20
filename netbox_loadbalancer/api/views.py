"""REST API viewsets for the netbox_loadbalancer plugin.

Each viewset extends ``NetBoxModelViewSet``, which is a DRF (Django REST Framework)
ModelViewSet pre-configured with NetBox's authentication, permission checking,
pagination, and nested serializer support. A single viewset provides all standard
REST actions: list, retrieve, create, update, partial_update, and destroy.

The three class attributes on each viewset control its behaviour:
- ``queryset``: the base database query (can include annotations like Count).
- ``serializer_class``: the serializer used to convert model instances to/from JSON.
- ``filterset_class``: the FilterSet that enables URL query parameter filtering
  (e.g. ``GET /api/plugins/loadbalancer/pools/?method=round-robin``).

These viewsets are registered with the ``NetBoxRouter`` in ``api/urls.py``, which
generates the standard REST URL patterns (list, detail, etc.) automatically.
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
    """API endpoint for managing load balancers.

    Supports ``GET /``, ``POST /``, ``GET /<id>/``, ``PUT /<id>/``, ``PATCH /<id>/``,
    and ``DELETE /<id>/`` under the ``/api/plugins/loadbalancer/loadbalancers/`` path.
    """
    queryset = LoadBalancer.objects.all()
    serializer_class = LoadBalancerSerializer
    filterset_class = LoadBalancerFilterSet


class PoolViewSet(NetBoxModelViewSet):
    """API endpoint for managing pools.

    The queryset includes ``.annotate(member_count=Count('members'))`` so that the
    pool member count is available in the serialized response without requiring a
    separate database query for each pool.
    """
    queryset = Pool.objects.annotate(member_count=Count('members'))
    serializer_class = PoolSerializer
    filterset_class = PoolFilterSet


class VirtualServerViewSet(NetBoxModelViewSet):
    """API endpoint for managing virtual servers.

    Supports full CRUD and filtering by load balancer, status, protocol, pool, and
    tenant via the ``VirtualServerFilterSet``.
    """
    queryset = VirtualServer.objects.all()
    serializer_class = VirtualServerSerializer
    filterset_class = VirtualServerFilterSet


class PoolMemberViewSet(NetBoxModelViewSet):
    """API endpoint for managing pool members.

    Supports full CRUD and filtering by pool, status, device, IP address, port,
    weight, and priority via the ``PoolMemberFilterSet``.
    """
    queryset = PoolMember.objects.all()
    serializer_class = PoolMemberSerializer
    filterset_class = PoolMemberFilterSet
