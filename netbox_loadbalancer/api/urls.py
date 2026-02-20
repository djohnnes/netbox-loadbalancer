"""API URL routing for the netbox_loadbalancer plugin.

Registers REST API endpoints for all four models under the plugin's API namespace.
"""

from netbox.api.routers import NetBoxRouter

from . import views

router = NetBoxRouter()
router.register('loadbalancers', views.LoadBalancerViewSet)
router.register('pools', views.PoolViewSet)
router.register('virtual-servers', views.VirtualServerViewSet)
router.register('pool-members', views.PoolMemberViewSet)

urlpatterns = router.urls
