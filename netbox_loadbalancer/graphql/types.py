"""Strawberry-django GraphQL types for each plugin model.

Each type class maps a Django model to a GraphQL object type. The ``fields='__all__'``
argument exposes all model fields automatically, including foreign key relationships.
Choice fields (platform, status, method, protocol) are explicitly annotated with
``strawberry.auto`` to let Strawberry-django resolve them as string types from the
underlying Django CharField.

The ``filters=`` parameter links the type to its corresponding filter class from
``filters.py``, enabling field-level filtering in GraphQL queries. The ``pagination=True``
parameter adds cursor-based pagination support to list queries.
"""

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType

from netbox_loadbalancer import models
from .filters import *

__all__ = (
    'LoadBalancerType',
    'PoolType',
    'VirtualServerType',
    'PoolMemberType',
)


@strawberry_django.type(
    models.LoadBalancer,
    fields='__all__',
    filters=LoadBalancerFilter,
    pagination=True,
)
class LoadBalancerType(NetBoxObjectType):
    platform: strawberry.auto
    status: strawberry.auto


@strawberry_django.type(
    models.Pool,
    fields='__all__',
    filters=PoolFilter,
    pagination=True,
)
class PoolType(NetBoxObjectType):
    method: strawberry.auto
    protocol: strawberry.auto


@strawberry_django.type(
    models.VirtualServer,
    fields='__all__',
    filters=VirtualServerFilter,
    pagination=True,
)
class VirtualServerType(NetBoxObjectType):
    protocol: strawberry.auto
    status: strawberry.auto


@strawberry_django.type(
    models.PoolMember,
    fields='__all__',
    filters=PoolMemberFilter,
    pagination=True,
)
class PoolMemberType(NetBoxObjectType):
    status: strawberry.auto
