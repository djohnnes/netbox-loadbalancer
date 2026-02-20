"""REST API serializers for the netbox_loadbalancer plugin.

Each serializer extends ``NetBoxModelSerializer``, which is a DRF ModelSerializer
pre-configured with NetBox's conventions for nested object representation, tag
handling, and custom field support.

Key concepts:
- ``Meta.fields``: the complete list of fields included in the full (detail) API
  response. This includes computed fields like ``url`` and ``display`` (provided
  by NetBoxModelSerializer), standard model fields, and audit fields (``created``,
  ``last_updated``).
- ``Meta.brief_fields``: the subset of fields returned when the ``?brief=true``
  query parameter is used on the API. Brief mode returns a minimal representation
  (typically just id, url, display, and name) and is used when the object appears
  as a nested related object inside another serializer's response, to avoid deeply
  nested JSON.
"""

from netbox.api.serializers import NetBoxModelSerializer

from ..models import LoadBalancer, VirtualServer, Pool, PoolMember


class LoadBalancerSerializer(NetBoxModelSerializer):
    """Serializer for load balancer API responses.

    Related objects (device, site, tenant, management_ip) are automatically serialized
    as nested objects in full mode, or as brief references when this serializer is
    used as a nested serializer inside another response.
    """
    class Meta:
        model = LoadBalancer
        fields = (
            'id', 'url', 'display', 'name', 'platform', 'status',
            'device', 'site', 'tenant', 'management_ip', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class PoolSerializer(NetBoxModelSerializer):
    """Serializer for pool API responses.

    The loadbalancer field is serialized as a nested object in full mode, showing
    the parent load balancer's details inline within the pool response.
    """
    class Meta:
        model = Pool
        fields = (
            'id', 'url', 'display', 'name', 'loadbalancer', 'method',
            'protocol', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class VirtualServerSerializer(NetBoxModelSerializer):
    """Serializer for virtual server API responses.

    Includes nested representations for loadbalancer, ip_address, pool, and tenant.
    The port and protocol fields are serialized as simple values.
    """
    class Meta:
        model = VirtualServer
        fields = (
            'id', 'url', 'display', 'name', 'loadbalancer', 'ip_address',
            'port', 'protocol', 'status', 'pool', 'tenant', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class PoolMemberSerializer(NetBoxModelSerializer):
    """Serializer for pool member API responses.

    Includes nested representations for pool, ip_address, and device. Numeric fields
    (port, weight, priority) are serialized as plain integers.
    """
    class Meta:
        model = PoolMember
        fields = (
            'id', 'url', 'display', 'name', 'pool', 'ip_address', 'device',
            'port', 'weight', 'priority', 'status', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')
