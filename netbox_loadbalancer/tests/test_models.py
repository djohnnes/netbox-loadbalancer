from django.core.exceptions import ValidationError
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


class PoolMemberCleanTest(TestCase):
    """Tests for PoolMember.clean() duplicate detection logic."""

    @classmethod
    def setUpTestData(cls):
        lb = LoadBalancer.objects.create(name='LB-Clean-Test', platform='f5')
        cls.pool = Pool.objects.create(name='Pool-Clean-Test', loadbalancer=lb)
        cls.ip = IPAddress.objects.create(address='10.1.0.1/24')
        cls.ip2 = IPAddress.objects.create(address='10.1.0.2/24')

    def test_duplicate_ip_port_rejected(self):
        """Two members with the same pool, IP, and port should fail validation."""
        PoolMember.objects.create(
            name='PM-Dup-1', pool=self.pool, ip_address=self.ip, port=8080,
        )
        pm2 = PoolMember(
            name='PM-Dup-2', pool=self.pool, ip_address=self.ip, port=8080,
        )
        with self.assertRaises(ValidationError):
            pm2.full_clean()

    def test_same_ip_different_port_allowed(self):
        """Same IP but different port should be allowed."""
        PoolMember.objects.create(
            name='PM-DiffPort-1', pool=self.pool, ip_address=self.ip2, port=8080,
        )
        pm2 = PoolMember(
            name='PM-DiffPort-2', pool=self.pool, ip_address=self.ip2, port=8081,
        )
        pm2.full_clean()  # Should not raise

    def test_null_ip_allows_duplicates(self):
        """Members with null IP address bypass the unique-together check."""
        PoolMember.objects.create(
            name='PM-NullIP-1', pool=self.pool, ip_address=None, port=8080,
        )
        pm2 = PoolMember(
            name='PM-NullIP-2', pool=self.pool, ip_address=None, port=8080,
        )
        pm2.full_clean()  # Should not raise because ip_address is NULL

    def test_update_existing_member_passes_clean(self):
        """Editing an existing member should not flag itself as a duplicate."""
        pm = PoolMember.objects.create(
            name='PM-Update', pool=self.pool, ip_address=self.ip, port=9999,
        )
        pm.name = 'PM-Update-Renamed'
        pm.full_clean()  # Should not raise

    def test_weight_min_value_rejected(self):
        """Weight of 0 should fail validation (minimum is 1)."""
        pm = PoolMember(
            name='PM-Weight0', pool=self.pool, port=7777, weight=0,
        )
        with self.assertRaises(ValidationError):
            pm.full_clean()

    def test_weight_valid(self):
        """Weight of 1 (minimum) should pass validation."""
        pm = PoolMember(
            name='PM-Weight1', pool=self.pool, port=7778, weight=1,
        )
        pm.full_clean()  # Should not raise

    def test_port_min_value_rejected(self):
        """Port of 0 should fail validation (minimum is 1)."""
        pm = PoolMember(
            name='PM-Port0', pool=self.pool, port=0,
        )
        with self.assertRaises(ValidationError):
            pm.full_clean()

    def test_port_max_value_rejected(self):
        """Port above 65535 should fail validation."""
        pm = PoolMember(
            name='PM-PortHigh', pool=self.pool, port=65536,
        )
        with self.assertRaises(ValidationError):
            pm.full_clean()


class CloneFieldsTest(TestCase):
    """Tests that clone_fields are defined and clone() returns expected data."""

    @classmethod
    def setUpTestData(cls):
        cls.lb = LoadBalancer.objects.create(
            name='LB-Clone', platform='f5', status='active',
        )
        cls.pool = Pool.objects.create(
            name='Pool-Clone', loadbalancer=cls.lb, method='round-robin', protocol='http',
        )

    def test_loadbalancer_clone(self):
        attrs = self.lb.clone()
        self.assertEqual(attrs['platform'], 'f5')
        self.assertEqual(attrs['status'], 'active')

    def test_pool_clone(self):
        attrs = self.pool.clone()
        self.assertEqual(attrs['loadbalancer'], self.lb.pk)
        self.assertEqual(attrs['method'], 'round-robin')
        self.assertEqual(attrs['protocol'], 'http')

    def test_virtualserver_clone(self):
        vs = VirtualServer.objects.create(
            name='VS-Clone', loadbalancer=self.lb, port=443, protocol='https', status='active',
        )
        attrs = vs.clone()
        self.assertEqual(attrs['loadbalancer'], self.lb.pk)
        self.assertEqual(attrs['protocol'], 'https')
        self.assertEqual(attrs['status'], 'active')

    def test_poolmember_clone(self):
        pm = PoolMember.objects.create(
            name='PM-Clone', pool=self.pool, port=8080, weight=5, priority=2, status='drain',
        )
        attrs = pm.clone()
        self.assertEqual(attrs['pool'], self.pool.pk)
        self.assertEqual(attrs['weight'], 5)
        self.assertEqual(attrs['priority'], 2)
        self.assertEqual(attrs['status'], 'drain')
