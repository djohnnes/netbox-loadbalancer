"""
Tests for the ``netbox_loadbalancer`` plugin's filter sets.

This module validates every filter exposed by the plugin's ``FilterSet``
classes: ``LoadBalancerFilterSet``, ``PoolFilterSet``,
``VirtualServerFilterSet``, and ``PoolMemberFilterSet``.  Filter sets power
the list-view search and filter sidebar in the NetBox UI, as well as the
``?field=value`` query-string filtering on REST API list endpoints.

Each test class follows the same pattern:

1. **Class attributes** – ``queryset`` and ``filterset`` are set at the class
   level so that every test method can call
   ``self.filterset(params, self.queryset).qs`` without boilerplate.
2. **``setUpTestData``** – creates three fixture objects with deliberately
   different field values so that each filter test can assert the correct
   subset is returned (typically count == 1 or count == 2).
3. **``test_<field>``** – applies a single filter parameter and asserts the
   count of matching objects.
4. **``test_search``** – exercises the ``q`` (search) filter, which maps to
   the ``SearchFilter`` defined in the filter set's ``search_fields``.

**Testing framework:** Django's ``TestCase`` with ``setUpTestData`` for
one-time fixture creation.

**Running these tests:**

.. code-block:: bash

   docker compose exec netbox python /opt/netbox/netbox/manage.py test \\
       netbox_loadbalancer.tests.test_filtersets --verbosity=2
"""

from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant

from netbox_loadbalancer.models import LoadBalancer, Pool, VirtualServer, PoolMember
from netbox_loadbalancer.filtersets import (
    LoadBalancerFilterSet, PoolFilterSet, VirtualServerFilterSet, PoolMemberFilterSet,
)


class LoadBalancerFilterSetTest(TestCase):
    """
    Tests for ``LoadBalancerFilterSet``.

    Verifies that ``LoadBalancer`` instances can be filtered by ``name``,
    ``platform``, ``status``, ``site``, ``tenant``, and the free-text
    ``search`` (``q``) parameter.  Three load balancers with varying field
    values are created in ``setUpTestData`` so that each filter can be tested
    in isolation.
    """

    queryset = LoadBalancer.objects.all()
    filterset = LoadBalancerFilterSet

    @classmethod
    def setUpTestData(cls):
        """Create three ``LoadBalancer`` instances across two sites and two tenants."""
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
        """Filter by exact ``name`` should return a single matching load balancer."""
        params = {'name': ['LB-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_platform(self):
        """Filter by ``platform`` should support single and multi-value lookups."""
        params = {'platform': ['f5']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'platform': ['f5', 'haproxy']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_status(self):
        """Filter by ``status`` should support single and multi-value lookups."""
        params = {'status': ['active']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'status': ['active', 'planned']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_site(self):
        """Filter by ``site_id`` should return all load balancers at the given site."""
        site = Site.objects.get(slug='fs-site-1')
        params = {'site_id': site.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        """Filter by ``tenant_id`` should return load balancers assigned to that tenant."""
        tenant = Tenant.objects.get(slug='fs-tenant-1')
        params = {'tenant_id': tenant.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        """The ``q`` search parameter should match against the load balancer name."""
        params = {'q': 'LB-FS-1'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class PoolFilterSetTest(TestCase):
    """
    Tests for ``PoolFilterSet``.

    Verifies that ``Pool`` instances can be filtered by ``name``,
    ``loadbalancer``, ``method``, ``protocol``, and the free-text ``search``
    (``q``) parameter.  Three pools with different methods and protocols are
    distributed across two load balancers.
    """

    queryset = Pool.objects.all()
    filterset = PoolFilterSet

    @classmethod
    def setUpTestData(cls):
        """Create two ``LoadBalancer`` instances and three ``Pool`` instances with varying fields."""
        lb1 = LoadBalancer.objects.create(name='LB-PFS-1', platform='f5')
        lb2 = LoadBalancer.objects.create(name='LB-PFS-2', platform='haproxy')

        Pool.objects.create(name='Pool-FS-1', loadbalancer=lb1, method='round-robin', protocol='http')
        Pool.objects.create(name='Pool-FS-2', loadbalancer=lb1, method='least-connections', protocol='https')
        Pool.objects.create(name='Pool-FS-3', loadbalancer=lb2, method='ip-hash', protocol='tcp')

    def test_name(self):
        """Filter by exact ``name`` should return a single matching pool."""
        params = {'name': ['Pool-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_loadbalancer(self):
        """Filter by ``loadbalancer_id`` should return all pools belonging to that load balancer."""
        lb = LoadBalancer.objects.get(name='LB-PFS-1')
        params = {'loadbalancer_id': [lb.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_method(self):
        """Filter by ``method`` should support single and multi-value lookups."""
        params = {'method': ['round-robin']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'method': ['round-robin', 'ip-hash']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        """Filter by ``protocol`` should return pools using that protocol."""
        params = {'protocol': ['http']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        """The ``q`` search parameter should match against the pool name."""
        params = {'q': 'Pool-FS-2'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class VirtualServerFilterSetTest(TestCase):
    """
    Tests for ``VirtualServerFilterSet``.

    Verifies that ``VirtualServer`` instances can be filtered by ``name``,
    ``status``, ``protocol``, ``port``, ``pool``, ``tenant``, and the
    free-text ``search`` (``q``) parameter.  Three virtual servers with
    different ports, protocols, and statuses are created under a single load
    balancer.
    """

    queryset = VirtualServer.objects.all()
    filterset = VirtualServerFilterSet

    @classmethod
    def setUpTestData(cls):
        """Create a ``LoadBalancer``, ``Pool``, ``Tenant``, and three ``VirtualServer`` instances."""
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
        """Filter by exact ``name`` should return a single matching virtual server."""
        params = {'name': ['VS-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_status(self):
        """Filter by ``status`` should support single and multi-value lookups."""
        params = {'status': ['active']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'status': ['active', 'planned']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        """Filter by ``protocol`` should return virtual servers using that protocol."""
        params = {'protocol': ['https']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_port(self):
        """Filter by ``port`` should return the virtual server listening on that port."""
        params = {'port': [80]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pool(self):
        """Filter by ``pool_id`` should return virtual servers assigned to that pool."""
        pool = Pool.objects.get(name='Pool-VSFS')
        params = {'pool_id': [pool.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tenant(self):
        """Filter by ``tenant_id`` should return virtual servers assigned to that tenant."""
        tenant = Tenant.objects.get(slug='fs-vs-tenant')
        params = {'tenant_id': tenant.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        """The ``q`` search parameter should match against the virtual-server name."""
        params = {'q': 'VS-FS-3'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class PoolMemberFilterSetTest(TestCase):
    """
    Tests for ``PoolMemberFilterSet``.

    Verifies that ``PoolMember`` instances can be filtered by ``name``,
    ``pool``, ``status``, ``port``, ``weight``, ``priority``, ``device``, and
    the free-text ``search`` (``q``) parameter.  Three members with different
    attribute values are spread across two pools and one device.
    """

    queryset = PoolMember.objects.all()
    filterset = PoolMemberFilterSet

    @classmethod
    def setUpTestData(cls):
        """Create two pools, a device, and three ``PoolMember`` instances with varying fields."""
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
        """Filter by exact ``name`` should return a single matching pool member."""
        params = {'name': ['PM-FS-1']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_pool(self):
        """Filter by ``pool_id`` should return all members belonging to that pool."""
        pool = Pool.objects.get(name='Pool-PMFS-1')
        params = {'pool_id': [pool.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_status(self):
        """Filter by ``status`` should support single and multi-value lookups."""
        params = {'status': ['active']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'status': ['active', 'drain']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_port(self):
        """Filter by ``port`` should return the member listening on that port."""
        params = {'port': [8080]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_weight(self):
        """Filter by ``weight`` should return members with that exact weight value."""
        params = {'weight': [5]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_priority(self):
        """Filter by ``priority`` should return members with that exact priority value."""
        params = {'priority': [1]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_device(self):
        """Filter by ``device_id`` should return members associated with that device."""
        device = Device.objects.get(name='PMFS Device')
        params = {'device_id': device.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search(self):
        """The ``q`` search parameter should match against the pool-member name."""
        params = {'q': 'PM-FS-2'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
