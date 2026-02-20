"""REST API serializers for the netbox_loadbalancer plugin.

Each serializer handles the conversion between model instances and their JSON
API representation, including nested related objects.
"""

from netbox.api.serializers import NetBoxModelSerializer

from ..models import LoadBalancer, VirtualServer, Pool, PoolMember


class LoadBalancerSerializer(NetBoxModelSerializer):
    """Serializer for load balancer objects."""
    class Meta:
        model = LoadBalancer
        fields = (
            'id', 'url', 'display', 'name', 'platform', 'status',
            'device', 'site', 'tenant', 'management_ip', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class PoolSerializer(NetBoxModelSerializer):
    """Serializer for pool objects."""
    class Meta:
        model = Pool
        fields = (
            'id', 'url', 'display', 'name', 'loadbalancer', 'method',
            'protocol', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class VirtualServerSerializer(NetBoxModelSerializer):
    """Serializer for virtual server objects."""
    class Meta:
        model = VirtualServer
        fields = (
            'id', 'url', 'display', 'name', 'loadbalancer', 'ip_address',
            'port', 'protocol', 'status', 'pool', 'tenant', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')


class PoolMemberSerializer(NetBoxModelSerializer):
    """Serializer for pool member objects."""
    class Meta:
        model = PoolMember
        fields = (
            'id', 'url', 'display', 'name', 'pool', 'ip_address', 'device',
            'port', 'weight', 'priority', 'status', 'description',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name')
