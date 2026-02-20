from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant

from netbox_loadbalancer.models import LoadBalancer, Pool, VirtualServer, PoolMember


class LoadBalancerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name='Test Site', slug='test-site')
        manufacturer = Manufacturer.objects.create(name='Test Mfg', slug='test-mfg')
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model='Test Model', slug='test-model',
        )
        role = DeviceRole.objects.create(name='Test Role', slug='test-role')
        cls.device = Device.objects.create(
            name='Test Device', site=site, device_type=device_type, role=role,
        )
        cls.site = site
        cls.tenant = Tenant.objects.create(name='Test Tenant', slug='test-tenant')
        cls.ip = IPAddress.objects.create(address='10.0.0.1/24')

    def test_create_loadbalancer(self):
        lb = LoadBalancer.objects.create(
            name='LB-01',
            platform='f5',
            status='active',
            device=self.device,
            site=self.site,
            tenant=self.tenant,
            management_ip=self.ip,
        )
        self.assertEqual(lb.name, 'LB-01')
        self.assertEqual(lb.platform, 'f5')
        self.assertEqual(lb.status, 'active')
        self.assertEqual(lb.device, self.device)
        self.assertEqual(lb.site, self.site)
        self.assertEqual(lb.tenant, self.tenant)
        self.assertEqual(lb.management_ip, self.ip)

    def test_str(self):
        lb = LoadBalancer.objects.create(name='LB-02', platform='f5')
        self.assertEqual(str(lb), 'LB-02')

    def test_get_absolute_url(self):
        lb = LoadBalancer.objects.create(name='LB-03', platform='f5')
        url = lb.get_absolute_url()
        self.assertIn('/loadbalancer/loadbalancers/', url)
        self.assertIn(str(lb.pk), url)


class PoolModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.lb = LoadBalancer.objects.create(name='LB-Pool-Test', platform='f5')

    def test_create_pool(self):
        pool = Pool.objects.create(
            name='Pool-01',
            loadbalancer=self.lb,
            method='round-robin',
            protocol='http',
        )
        self.assertEqual(pool.name, 'Pool-01')
        self.assertEqual(pool.loadbalancer, self.lb)
        self.assertEqual(pool.method, 'round-robin')
        self.assertEqual(pool.protocol, 'http')

    def test_str(self):
        pool = Pool.objects.create(name='Pool-02', loadbalancer=self.lb)
        self.assertEqual(str(pool), 'Pool-02')

    def test_get_absolute_url(self):
        pool = Pool.objects.create(name='Pool-03', loadbalancer=self.lb)
        url = pool.get_absolute_url()
        self.assertIn('/loadbalancer/pools/', url)
        self.assertIn(str(pool.pk), url)


class VirtualServerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.lb = LoadBalancer.objects.create(name='LB-VS-Test', platform='f5')

    def test_create_virtual_server(self):
        vs = VirtualServer.objects.create(
            name='VS-01',
            loadbalancer=self.lb,
            port=80,
            protocol='http',
            status='active',
        )
        self.assertEqual(vs.name, 'VS-01')
        self.assertEqual(vs.port, 80)
        self.assertEqual(vs.protocol, 'http')
        self.assertEqual(vs.status, 'active')

    def test_str(self):
        vs = VirtualServer.objects.create(
            name='VS-02',
            loadbalancer=self.lb,
            port=443,
            protocol='https',
        )
        self.assertEqual(str(vs), 'VS-02 (HTTPS/443)')

    def test_get_absolute_url(self):
        vs = VirtualServer.objects.create(
            name='VS-03',
            loadbalancer=self.lb,
            port=8080,
        )
        url = vs.get_absolute_url()
        self.assertIn('/loadbalancer/virtual-servers/', url)
        self.assertIn(str(vs.pk), url)


class PoolMemberModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-PM-Test', platform='f5')
        cls.pool = Pool.objects.create(name='Pool-PM-Test', loadbalancer=lb)

    def test_create_pool_member(self):
        pm = PoolMember.objects.create(
            name='Member-01',
            pool=self.pool,
            port=8080,
            weight=5,
            priority=1,
            status='active',
        )
        self.assertEqual(pm.name, 'Member-01')
        self.assertEqual(pm.pool, self.pool)
        self.assertEqual(pm.port, 8080)
        self.assertEqual(pm.weight, 5)
        self.assertEqual(pm.priority, 1)

    def test_str(self):
        pm = PoolMember.objects.create(
            name='Member-02',
            pool=self.pool,
            port=9090,
        )
        self.assertEqual(str(pm), 'Member-02:9090')

    def test_get_absolute_url(self):
        pm = PoolMember.objects.create(
            name='Member-03',
            pool=self.pool,
            port=7070,
        )
        url = pm.get_absolute_url()
        self.assertIn('/loadbalancer/pool-members/', url)
        self.assertIn(str(pm.pk), url)
