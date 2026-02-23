"""
Tests for the ``netbox_loadbalancer`` plugin's UI views.

This module exercises the standard NetBox web-UI views (list, detail, create,
edit, delete, bulk-import, bulk-edit, bulk-delete, and changelog) for every
model in the plugin: ``LoadBalancer``, ``Pool``, ``VirtualServer``, and
``PoolMember``.

Rather than writing individual view tests from scratch, the plugin leverages
NetBox's built-in ``ViewTestCases`` mixin classes from
``utilities.testing``.  Each mixin provides a complete set of tests for a
particular view type (e.g. ``GetObjectViewTestCase`` tests the detail view,
``CreateObjectViewTestCase`` tests the create form, etc.).  The test class
only needs to provide:

* ``model`` – the Django model under test.
* ``_get_base_url()`` – returns the URL namespace pattern used by the plugin's
  ``urlpatterns``, e.g. ``'plugins:netbox_loadbalancer:loadbalancer_{}'``.
* ``setUpTestData()`` – creates three existing objects (for list/detail/delete
  tests) plus ``form_data`` (for create/edit), ``csv_data`` and
  ``csv_update_data`` (for bulk-import), and ``bulk_edit_data`` (for
  bulk-edit).

**Testing framework:** NetBox's ``ViewTestCases`` mixins extend Django's
``TestCase`` and handle authentication, CSRF, permission checks, and response
status-code assertions automatically.

**Running these tests:**

.. code-block:: bash

   docker compose exec netbox python /opt/netbox/netbox/manage.py test \\
       netbox_loadbalancer.tests.test_views --verbosity=2
"""

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant
from utilities.testing import ViewTestCases

from netbox_loadbalancer.models import LoadBalancer, Pool, VirtualServer, PoolMember


class LoadBalancerViewTest(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """
    View tests for the ``LoadBalancer`` model.

    Inherits nine ``ViewTestCases`` mixins that collectively test every
    standard NetBox UI operation (GET detail, GET list, POST create, POST edit,
    POST delete, bulk import via CSV, bulk edit, bulk delete, and changelog).
    """

    model = LoadBalancer

    def _get_base_url(self):
        """Return the URL namespace pattern for ``LoadBalancer`` views."""
        return 'plugins:netbox_loadbalancer:loadbalancer_{}'

    @classmethod
    def setUpTestData(cls):
        """
        Create three ``LoadBalancer`` instances plus form, CSV, and bulk-edit
        data used by the ``ViewTestCases`` mixins.
        """
        site = Site.objects.create(name='VT Site', slug='vt-site')

        LoadBalancer.objects.create(name='LB-VT-1', platform='f5', status='active', site=site)
        LoadBalancer.objects.create(name='LB-VT-2', platform='haproxy', status='active', site=site)
        LoadBalancer.objects.create(name='LB-VT-3', platform='nginx', status='planned', site=site)

        cls.form_data = {
            'name': 'LB-VT-4',
            'platform': 'f5',
            'status': 'active',
            'site': site.pk,
            'description': '',
            'tags': [],
        }

        cls.csv_data = (
            'name,platform,status,description',
            'LB-CSV-1,f5,active,Test LB 1',
            'LB-CSV-2,haproxy,planned,Test LB 2',
            'LB-CSV-3,nginx,active,Test LB 3',
        )

        cls.csv_update_data = (
            'id,description',
        )

        cls.bulk_edit_data = {
            'description': 'Bulk updated',
        }


class PoolViewTest(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """
    View tests for the ``Pool`` model.

    Inherits the same nine ``ViewTestCases`` mixins as ``LoadBalancerViewTest``
    to cover all standard CRUD and bulk operations for pools.
    """

    model = Pool

    def _get_base_url(self):
        """Return the URL namespace pattern for ``Pool`` views."""
        return 'plugins:netbox_loadbalancer:pool_{}'

    @classmethod
    def setUpTestData(cls):
        """
        Create a parent ``LoadBalancer``, three ``Pool`` instances, and the
        form / CSV / bulk-edit data consumed by the ``ViewTestCases`` mixins.
        """
        lb = LoadBalancer.objects.create(name='LB-PoolVT', platform='f5')

        Pool.objects.create(name='Pool-VT-1', loadbalancer=lb, method='round-robin', protocol='http')
        Pool.objects.create(name='Pool-VT-2', loadbalancer=lb, method='least-connections', protocol='https')
        Pool.objects.create(name='Pool-VT-3', loadbalancer=lb, method='ip-hash', protocol='tcp')

        cls.form_data = {
            'name': 'Pool-VT-4',
            'loadbalancer': lb.pk,
            'method': 'round-robin',
            'protocol': 'http',
            'description': '',
            'tags': [],
        }

        cls.csv_data = (
            'name,loadbalancer,method,protocol,description',
            'Pool-CSV-1,LB-PoolVT,round-robin,http,Test Pool 1',
            'Pool-CSV-2,LB-PoolVT,least-connections,https,Test Pool 2',
            'Pool-CSV-3,LB-PoolVT,ip-hash,tcp,Test Pool 3',
        )

        cls.csv_update_data = (
            'id,description',
        )

        cls.bulk_edit_data = {
            'description': 'Bulk updated',
        }


class VirtualServerViewTest(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """
    View tests for the ``VirtualServer`` model.

    Inherits the same nine ``ViewTestCases`` mixins to cover all standard CRUD
    and bulk operations for virtual servers.
    """

    model = VirtualServer

    def _get_base_url(self):
        """Return the URL namespace pattern for ``VirtualServer`` views."""
        return 'plugins:netbox_loadbalancer:virtualserver_{}'

    @classmethod
    def setUpTestData(cls):
        """
        Create a parent ``LoadBalancer``, three ``VirtualServer`` instances, and
        the form / CSV / bulk-edit data consumed by the ``ViewTestCases`` mixins.
        """
        lb = LoadBalancer.objects.create(name='LB-VSVT', platform='f5')

        VirtualServer.objects.create(
            name='VS-VT-1', loadbalancer=lb, port=80, protocol='http', status='active',
        )
        VirtualServer.objects.create(
            name='VS-VT-2', loadbalancer=lb, port=443, protocol='https', status='active',
        )
        VirtualServer.objects.create(
            name='VS-VT-3', loadbalancer=lb, port=8080, protocol='tcp', status='planned',
        )

        cls.form_data = {
            'name': 'VS-VT-4',
            'loadbalancer': lb.pk,
            'port': 9090,
            'protocol': 'http',
            'status': 'active',
            'description': '',
            'tags': [],
        }

        cls.csv_data = (
            'name,loadbalancer,port,protocol,status,description',
            'VS-CSV-1,LB-VSVT,8001,http,active,Test VS 1',
            'VS-CSV-2,LB-VSVT,8002,https,active,Test VS 2',
            'VS-CSV-3,LB-VSVT,8003,tcp,planned,Test VS 3',
        )

        cls.csv_update_data = (
            'id,description',
        )

        cls.bulk_edit_data = {
            'description': 'Bulk updated',
        }


class PoolMemberViewTest(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """
    View tests for the ``PoolMember`` model.

    Inherits the same nine ``ViewTestCases`` mixins to cover all standard CRUD
    and bulk operations for pool members.
    """

    model = PoolMember

    def _get_base_url(self):
        """Return the URL namespace pattern for ``PoolMember`` views."""
        return 'plugins:netbox_loadbalancer:poolmember_{}'

    @classmethod
    def setUpTestData(cls):
        """
        Create a ``LoadBalancer`` → ``Pool`` hierarchy, three ``PoolMember``
        instances, and the form / CSV / bulk-edit data consumed by the
        ``ViewTestCases`` mixins.
        """
        lb = LoadBalancer.objects.create(name='LB-PMVT', platform='f5')
        pool = Pool.objects.create(name='Pool-PMVT', loadbalancer=lb)

        PoolMember.objects.create(
            name='PM-VT-1', pool=pool, port=8080, weight=1, priority=0, status='active',
        )
        PoolMember.objects.create(
            name='PM-VT-2', pool=pool, port=8081, weight=2, priority=1, status='active',
        )
        PoolMember.objects.create(
            name='PM-VT-3', pool=pool, port=8082, weight=3, priority=2, status='drain',
        )

        cls.form_data = {
            'name': 'PM-VT-4',
            'pool': pool.pk,
            'port': 9080,
            'weight': 1,
            'priority': 0,
            'status': 'active',
            'description': '',
            'tags': [],
        }

        cls.csv_data = (
            'name,pool,port,weight,priority,status,description',
            'PM-CSV-1,Pool-PMVT,9001,1,0,active,Test PM 1',
            'PM-CSV-2,Pool-PMVT,9002,2,1,active,Test PM 2',
            'PM-CSV-3,Pool-PMVT,9003,3,2,drain,Test PM 3',
        )

        cls.csv_update_data = (
            'id,description',
        )

        cls.bulk_edit_data = {
            'description': 'Bulk updated',
        }
