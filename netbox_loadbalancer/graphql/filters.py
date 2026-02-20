"""Strawberry-django filter types for GraphQL query filtering.

Each filter type maps to one of the plugin's models and defines which fields can
be filtered in GraphQL queries. The ``lookups=True`` argument on the decorator
enables standard lookup expressions (exact, contains, starts_with, etc.) for each
field.

These filters are referenced by the corresponding GraphQL types in ``types.py``
via the ``filters=`` parameter on the ``@strawberry_django.type`` decorator.
"""

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup

from netbox.graphql.filters import NetBoxModelFilter

from netbox_loadbalancer import models

__all__ = (
    'LoadBalancerFilter',
    'PoolFilter',
    'VirtualServerFilter',
    'PoolMemberFilter',
)


@strawberry_django.filter_type(models.LoadBalancer, lookups=True)
class LoadBalancerFilter(NetBoxModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    platform: FilterLookup[str] | None = strawberry_django.filter_field()
    status: FilterLookup[str] | None = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()
    site_id: ID | None = strawberry_django.filter_field()
    tenant_id: ID | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(models.Pool, lookups=True)
class PoolFilter(NetBoxModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    loadbalancer_id: ID | None = strawberry_django.filter_field()
    method: FilterLookup[str] | None = strawberry_django.filter_field()
    protocol: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(models.VirtualServer, lookups=True)
class VirtualServerFilter(NetBoxModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    loadbalancer_id: ID | None = strawberry_django.filter_field()
    ip_address_id: ID | None = strawberry_django.filter_field()
    port: FilterLookup[int] | None = strawberry_django.filter_field()
    protocol: FilterLookup[str] | None = strawberry_django.filter_field()
    status: FilterLookup[str] | None = strawberry_django.filter_field()
    pool_id: ID | None = strawberry_django.filter_field()
    tenant_id: ID | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter_type(models.PoolMember, lookups=True)
class PoolMemberFilter(NetBoxModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    pool_id: ID | None = strawberry_django.filter_field()
    ip_address_id: ID | None = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()
    port: FilterLookup[int] | None = strawberry_django.filter_field()
    weight: FilterLookup[int] | None = strawberry_django.filter_field()
    priority: FilterLookup[int] | None = strawberry_django.filter_field()
    status: FilterLookup[str] | None = strawberry_django.filter_field()
    description: FilterLookup[str] | None = strawberry_django.filter_field()
