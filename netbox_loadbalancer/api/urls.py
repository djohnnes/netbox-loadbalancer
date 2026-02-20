"""API URL routing for the netbox_loadbalancer plugin.

Uses ``NetBoxRouter`` (a subclass of DRF's DefaultRouter) to automatically generate
REST API URL patterns for all four model viewsets. The router creates standard
endpoints like ``/api/plugins/loadbalancer/loadbalancers/`` and
``/api/plugins/loadbalancer/loadbalancers/<id>/``.

NetBox discovers this module automatically because the plugin package contains an
``api/`` sub-package with a ``urls.py`` module. The ``urlpatterns`` variable is
included under the plugin's API namespace by NetBox's plugin loading machinery.
"""

from netbox.api.routers import NetBoxRouter

from . import views

router = NetBoxRouter()
router.register('loadbalancers', views.LoadBalancerViewSet)
router.register('pools', views.PoolViewSet)
router.register('virtual-servers', views.VirtualServerViewSet)
router.register('pool-members', views.PoolMemberViewSet)

urlpatterns = router.urls
