"""GraphQL schema definition for the netbox_loadbalancer plugin.

Defines the top-level Query class that exposes singular and list query fields for
each model. NetBox's plugin framework auto-discovers this module at ``graphql.schema``
and merges the ``schema`` list into the root GraphQL Query type.

Each model gets two fields:
- A singular field (e.g. ``load_balancer``) for fetching a single object by ID.
- A list field (e.g. ``load_balancer_list``) for fetching filtered, paginated lists.
"""

from typing import List

import strawberry
import strawberry_django

from .types import *

__all__ = (
    'schema',
)


@strawberry.type(name='Query')
class LoadBalancerQuery:
    load_balancer: LoadBalancerType = strawberry_django.field()
    load_balancer_list: List[LoadBalancerType] = strawberry_django.field()

    pool: PoolType = strawberry_django.field()
    pool_list: List[PoolType] = strawberry_django.field()

    virtual_server: VirtualServerType = strawberry_django.field()
    virtual_server_list: List[VirtualServerType] = strawberry_django.field()

    pool_member: PoolMemberType = strawberry_django.field()
    pool_member_list: List[PoolMemberType] = strawberry_django.field()


schema = [LoadBalancerQuery]
