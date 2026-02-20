"""URL routing for the netbox_loadbalancer plugin.

Maps URL paths to views for all four models using NetBox's get_model_urls utility.
"""

from django.urls import include, path

from utilities.urls import get_model_urls

from . import views  # noqa: F401 — triggers @register_model_view decorators

urlpatterns = [
    # LoadBalancer
    path('loadbalancers/', include(get_model_urls('netbox_loadbalancer', 'loadbalancer', detail=False))),
    path('loadbalancers/<int:pk>/', include(get_model_urls('netbox_loadbalancer', 'loadbalancer'))),

    # Pool
    path('pools/', include(get_model_urls('netbox_loadbalancer', 'pool', detail=False))),
    path('pools/<int:pk>/', include(get_model_urls('netbox_loadbalancer', 'pool'))),

    # VirtualServer
    path('virtual-servers/', include(get_model_urls('netbox_loadbalancer', 'virtualserver', detail=False))),
    path('virtual-servers/<int:pk>/', include(get_model_urls('netbox_loadbalancer', 'virtualserver'))),

    # PoolMember
    path('pool-members/', include(get_model_urls('netbox_loadbalancer', 'poolmember', detail=False))),
    path('pool-members/<int:pk>/', include(get_model_urls('netbox_loadbalancer', 'poolmember'))),
]
