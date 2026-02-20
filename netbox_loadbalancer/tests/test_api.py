from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant
from utilities.testing import APIViewTestCases

from netbox_loadbalancer.models import LoadBalancer, Pool, VirtualServer, PoolMember


class LoadBalancerAPITest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = LoadBalancer
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name='API Site', slug='api-site')

        loadbalancers = (
            LoadBalancer(name='LB-API-1', platform='f5', status='active', site=site),
            LoadBalancer(name='LB-API-2', platform='haproxy', status='active', site=site),
            LoadBalancer(name='LB-API-3', platform='nginx', status='planned', site=site),
        )
        LoadBalancer.objects.bulk_create(loadbalancers)

        cls.create_data = [
            {'name': 'LB-API-4', 'platform': 'f5', 'status': 'active'},
            {'name': 'LB-API-5', 'platform': 'haproxy', 'status': 'active'},
            {'name': 'LB-API-6', 'platform': 'citrix', 'status': 'planned'},
        ]
        cls.bulk_update_data = {
            'description': 'Updated via API',
        }


class PoolAPITest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = Pool
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-PoolAPI', platform='f5')

        pools = (
            Pool(name='Pool-API-1', loadbalancer=lb, method='round-robin', protocol='http'),
            Pool(name='Pool-API-2', loadbalancer=lb, method='least-connections', protocol='https'),
            Pool(name='Pool-API-3', loadbalancer=lb, method='ip-hash', protocol='tcp'),
        )
        Pool.objects.bulk_create(pools)

        cls.create_data = [
            {'name': 'Pool-API-4', 'loadbalancer': lb.pk, 'method': 'round-robin', 'protocol': 'http'},
            {'name': 'Pool-API-5', 'loadbalancer': lb.pk, 'method': 'weighted', 'protocol': 'udp'},
            {'name': 'Pool-API-6', 'loadbalancer': lb.pk, 'method': 'other', 'protocol': 'other'},
        ]
        cls.bulk_update_data = {
            'description': 'Updated via API',
        }


class VirtualServerAPITest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = VirtualServer
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-VSAPI', platform='f5')

        virtual_servers = (
            VirtualServer(name='VS-API-1', loadbalancer=lb, port=80, protocol='http', status='active'),
            VirtualServer(name='VS-API-2', loadbalancer=lb, port=443, protocol='https', status='active'),
            VirtualServer(name='VS-API-3', loadbalancer=lb, port=8080, protocol='tcp', status='planned'),
        )
        VirtualServer.objects.bulk_create(virtual_servers)

        cls.create_data = [
            {'name': 'VS-API-4', 'loadbalancer': lb.pk, 'port': 9090, 'protocol': 'http', 'status': 'active'},
            {'name': 'VS-API-5', 'loadbalancer': lb.pk, 'port': 9091, 'protocol': 'https', 'status': 'active'},
            {'name': 'VS-API-6', 'loadbalancer': lb.pk, 'port': 9092, 'protocol': 'tcp', 'status': 'planned'},
        ]
        cls.bulk_update_data = {
            'description': 'Updated via API',
        }


class PoolMemberAPITest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = PoolMember
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-PMAPI', platform='f5')
        pool = Pool.objects.create(name='Pool-PMAPI', loadbalancer=lb)

        members = (
            PoolMember(name='PM-API-1', pool=pool, port=8080, weight=1, priority=0, status='active'),
            PoolMember(name='PM-API-2', pool=pool, port=8081, weight=2, priority=1, status='active'),
            PoolMember(name='PM-API-3', pool=pool, port=8082, weight=3, priority=2, status='drain'),
        )
        PoolMember.objects.bulk_create(members)

        cls.create_data = [
            {'name': 'PM-API-4', 'pool': pool.pk, 'port': 9080, 'weight': 1, 'priority': 0, 'status': 'active'},
            {'name': 'PM-API-5', 'pool': pool.pk, 'port': 9081, 'weight': 2, 'priority': 1, 'status': 'active'},
            {'name': 'PM-API-6', 'pool': pool.pk, 'port': 9082, 'weight': 3, 'priority': 2, 'status': 'drain'},
        ]
        cls.bulk_update_data = {
            'description': 'Updated via API',
        }
