from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant

from netbox_loadbalancer.models import LoadBalancer, Pool, VirtualServer, PoolMember
from netbox_loadbalancer.filtersets import (
    LoadBalancerFilterSet, PoolFilterSet, VirtualServerFilterSet, PoolMemberFilterSet,
)


class LoadBalancerFilterSetTest(TestCase):
    queryset = LoadBalancer.objects.all()
    filterset = LoadBalancerFilterSet

    @classmethod
    def setUpTestData(cls):
        sites = (
            Site(name='FS Site 1', slug='fs-site-1'),
            Site(name='FS Site 2', slug='fs-site-2'),
        )
        Site.objects.bulk_create(sites)

        tenants = (
            Tenant(name='FS Tenant 1', slug='fs-tenant-1'),
            Tenant(name='FS Tenant 2', slug='fs-tenant-2'),
        )
        Tenant.objects.bulk_create(tenants)

        LoadBalancer.objects.create(
            name='LB-FS-1', platform='f5', status='active',
            site=sites[0], tenant=tenants[0],
        )
        LoadBalancer.objects.create(
            name='LB-FS-2', platform='haproxy', status='planned',
            site=sites[1], tenant=tenants[1],
        )
        LoadBalancer.objects.create(
            name='LB-FS-3', platform='nginx', status='maintenance',
            site=sites[0],
        )

    def test_name(self):
        params = {'name': ['LB-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_platform(self):
        params = {'platform': ['f5']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'platform': ['f5', 'haproxy']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_status(self):
        params = {'status': ['active']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'status': ['active', 'planned']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_site(self):
        site = Site.objects.get(slug='fs-site-1')
        params = {'site_id': site.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        tenant = Tenant.objects.get(slug='fs-tenant-1')
        params = {'tenant_id': tenant.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        params = {'q': 'LB-FS-1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class PoolFilterSetTest(TestCase):
    queryset = Pool.objects.all()
    filterset = PoolFilterSet

    @classmethod
    def setUpTestData(cls):
        lb1 = LoadBalancer.objects.create(name='LB-PFS-1', platform='f5')
        lb2 = LoadBalancer.objects.create(name='LB-PFS-2', platform='haproxy')

        Pool.objects.create(name='Pool-FS-1', loadbalancer=lb1, method='round-robin', protocol='http')
        Pool.objects.create(name='Pool-FS-2', loadbalancer=lb1, method='least-connections', protocol='https')
        Pool.objects.create(name='Pool-FS-3', loadbalancer=lb2, method='ip-hash', protocol='tcp')

    def test_name(self):
        params = {'name': ['Pool-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_loadbalancer(self):
        lb = LoadBalancer.objects.get(name='LB-PFS-1')
        params = {'loadbalancer_id': [lb.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_method(self):
        params = {'method': ['round-robin']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'method': ['round-robin', 'ip-hash']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        params = {'protocol': ['http']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        params = {'q': 'Pool-FS-2'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class VirtualServerFilterSetTest(TestCase):
    queryset = VirtualServer.objects.all()
    filterset = VirtualServerFilterSet

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-VSFS', platform='f5')
        pool = Pool.objects.create(name='Pool-VSFS', loadbalancer=lb)
        tenant = Tenant.objects.create(name='FS VS Tenant', slug='fs-vs-tenant')

        VirtualServer.objects.create(
            name='VS-FS-1', loadbalancer=lb, port=80, protocol='http',
            status='active', pool=pool, tenant=tenant,
        )
        VirtualServer.objects.create(
            name='VS-FS-2', loadbalancer=lb, port=443, protocol='https',
            status='planned',
        )
        VirtualServer.objects.create(
            name='VS-FS-3', loadbalancer=lb, port=8080, protocol='tcp',
            status='disabled',
        )

    def test_name(self):
        params = {'name': ['VS-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_status(self):
        params = {'status': ['active']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'status': ['active', 'planned']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        params = {'protocol': ['https']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_port(self):
        params = {'port': [80]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pool(self):
        pool = Pool.objects.get(name='Pool-VSFS')
        params = {'pool_id': [pool.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tenant(self):
        tenant = Tenant.objects.get(slug='fs-vs-tenant')
        params = {'tenant_id': tenant.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        params = {'q': 'VS-FS-3'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class PoolMemberFilterSetTest(TestCase):
    queryset = PoolMember.objects.all()
    filterset = PoolMemberFilterSet

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-PMFS', platform='f5')
        pool1 = Pool.objects.create(name='Pool-PMFS-1', loadbalancer=lb)
        pool2 = Pool.objects.create(name='Pool-PMFS-2', loadbalancer=lb)

        manufacturer = Manufacturer.objects.create(name='PMFS Mfg', slug='pmfs-mfg')
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model='PMFS Model', slug='pmfs-model',
        )
        site = Site.objects.create(name='PMFS Site', slug='pmfs-site')
        role = DeviceRole.objects.create(name='PMFS Role', slug='pmfs-role')
        device = Device.objects.create(
            name='PMFS Device', site=site, device_type=device_type, role=role,
        )

        PoolMember.objects.create(
            name='PM-FS-1', pool=pool1, port=8080, weight=1,
            priority=0, status='active', device=device,
        )
        PoolMember.objects.create(
            name='PM-FS-2', pool=pool1, port=8081, weight=5,
            priority=1, status='drain',
        )
        PoolMember.objects.create(
            name='PM-FS-3', pool=pool2, port=8082, weight=10,
            priority=2, status='disabled',
        )

    def test_name(self):
        params = {'name': ['PM-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pool(self):
        pool = Pool.objects.get(name='Pool-PMFS-1')
        params = {'pool_id': [pool.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_status(self):
        params = {'status': ['active']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'status': ['active', 'drain']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_port(self):
        params = {'port': [8080]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_weight(self):
        params = {'weight': [5]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_priority(self):
        params = {'priority': [1]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_device(self):
        device = Device.objects.get(name='PMFS Device')
        params = {'device_id': device.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        params = {'q': 'PM-FS-2'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
