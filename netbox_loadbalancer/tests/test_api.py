"""
Tests for the ``netbox_loadbalancer`` plugin's REST API endpoints.

This module validates the full CRUD lifecycle (GET single, GET list, POST
create, PATCH/PUT update, DELETE) for every model exposed through the plugin's
API: ``LoadBalancer``, ``Pool``, ``VirtualServer``, and ``PoolMember``.

Like the view tests, these classes leverage NetBox's built-in test
infrastructure — in this case, the ``APIViewTestCases`` mixin classes from
``utilities.testing``.  Each mixin provides a complete set of tests for a
particular API operation (e.g. ``GetObjectViewTestCase`` tests ``GET
/api/.../{{id}}/``, ``CreateObjectViewTestCase`` tests ``POST /api/.../``).
The test class only needs to provide:

* ``model`` – the Django model under test.
* ``view_namespace`` – the DRF router namespace, e.g.
  ``'plugins-api:netbox_loadbalancer'``.
* ``brief_fields`` – the list of fields returned in "brief" serialisation mode
  (used by ``?brief=true`` queries).
* ``setUpTestData()`` – creates three existing objects (for GET / DELETE tests)
  plus ``create_data`` (a list of dicts for POST tests) and
  ``bulk_update_data`` (a dict for PATCH bulk-update tests).

**Testing framework:** NetBox's ``APIViewTestCases`` mixins extend Django REST
Framework's ``APITestCase``, handling token authentication, content-type
negotiation, permission checks, and response status-code assertions
automatically.

**Running these tests:**

.. code-block:: bash

   docker compose exec netbox python /opt/netbox/netbox/manage.py test \\
       netbox_loadbalancer.tests.test_api --verbosity=2
"""

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
    """
    API tests for the ``LoadBalancer`` model.

    Inherits five ``APIViewTestCases`` mixins that collectively test GET
    (single + list), POST (create), PATCH/PUT (update), and DELETE operations
    against the ``/api/plugins/loadbalancer/loadbalancers/`` endpoint.
    """

    model = LoadBalancer
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        """
        Create three ``LoadBalancer`` instances for read / delete tests, plus
        ``create_data`` for POST tests and ``bulk_update_data`` for PATCH tests.
        """
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
    """
    API tests for the ``Pool`` model.

    Inherits the same five ``APIViewTestCases`` mixins to test CRUD operations
    against the ``/api/plugins/loadbalancer/pools/`` endpoint.
    """

    model = Pool
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        """
        Create a parent ``LoadBalancer``, three ``Pool`` instances, and the
        ``create_data`` / ``bulk_update_data`` used by the API test mixins.
        """
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
    """
    API tests for the ``VirtualServer`` model.

    Inherits the same five ``APIViewTestCases`` mixins to test CRUD operations
    against the ``/api/plugins/loadbalancer/virtual-servers/`` endpoint.
    """

    model = VirtualServer
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        """
        Create a parent ``LoadBalancer``, three ``VirtualServer`` instances, and
        the ``create_data`` / ``bulk_update_data`` used by the API test mixins.
        """
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
    """
    API tests for the ``PoolMember`` model.

    Inherits the same five ``APIViewTestCases`` mixins to test CRUD operations
    against the ``/api/plugins/loadbalancer/pool-members/`` endpoint.
    """

    model = PoolMember
    view_namespace = 'plugins-api:netbox_loadbalancer'
    brief_fields = ['display', 'id', 'name', 'url']

    @classmethod
    def setUpTestData(cls):
        """
        Create a ``LoadBalancer`` → ``Pool`` hierarchy, three ``PoolMember``
        instances, and the ``create_data`` / ``bulk_update_data`` used by the
        API test mixins.
        """
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
