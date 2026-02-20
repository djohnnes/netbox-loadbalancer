"""URL routing for the netbox_loadbalancer plugin.

Maps URL paths to views for all four models. NetBox plugins define their URL patterns
in a module-level ``urlpatterns`` list, which is automatically included under the
plugin's ``base_url`` prefix (``/plugins/loadbalancer/``).

Each model has two URL entries:
1. A collection path (e.g. ``loadbalancers/``) with ``detail=False`` for list, add,
   bulk import, bulk edit, and bulk delete views.
2. A detail path (e.g. ``loadbalancers/<int:pk>/``) for the object detail, edit,
   and delete views that operate on a specific object identified by primary key.

The ``get_model_urls()`` utility generates the URL patterns for all views that were
registered with ``@register_model_view`` in ``views.py``. The ``from . import views``
import is necessary even though ``views`` is not referenced directly — importing the
module triggers the ``@register_model_view`` decorators, which register each view
class with NetBox's URL dispatcher.
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
