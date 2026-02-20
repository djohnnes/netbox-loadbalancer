"""Web UI views for the netbox_loadbalancer plugin.

This module defines all the views that power the plugin's web interface. NetBox uses
class-based views with a standard set of generic view types for each model:

- **ObjectView**: detail page for a single object, using a panel-based layout.
- **ObjectListView**: paginated table of objects with filtering and search support.
- **ObjectEditView**: form-based create and edit page (handles both add and edit).
- **ObjectDeleteView**: confirmation page for deleting a single object.
- **BulkImportView**: CSV upload page for creating many objects from a spreadsheet.
- **BulkEditView**: form for editing multiple selected objects at once.
- **BulkDeleteView**: confirmation page for deleting multiple selected objects.

The ``@register_model_view`` decorator registers each view with NetBox's URL
dispatcher. It takes the model class and an action name (e.g. 'list', 'edit',
'delete') and automatically generates URL patterns. The ``detail=False`` parameter
indicates the view operates on a collection (no ``pk`` in the URL), while detail
views require an object's primary key.

Each view class sets a few class attributes to configure its behaviour:
- ``queryset``: the base database query for the model.
- ``table``: the django-tables2 table class used for list/bulk views.
- ``form``: the Django form class used for edit/bulk edit views.
- ``filterset`` / ``filterset_form``: the filter set and its corresponding UI form.
- ``layout``: the panel layout for detail views.
"""

from django.db.models import Count
from netbox.views.generic import (
    ObjectListView, ObjectEditView, ObjectDeleteView, ObjectView,
    BulkImportView, BulkEditView, BulkDeleteView,
)
from netbox.ui.layout import SimpleLayout
from netbox.ui.panels import CommentsPanel
from utilities.views import register_model_view

from .models import LoadBalancer, VirtualServer, Pool, PoolMember
from .tables import LoadBalancerTable, VirtualServerTable, PoolTable, PoolMemberTable
from .filtersets import (
    LoadBalancerFilterSet, VirtualServerFilterSet, PoolFilterSet, PoolMemberFilterSet,
)
from .forms import (
    LoadBalancerForm, LoadBalancerFilterForm, LoadBalancerBulkEditForm, LoadBalancerImportForm,
    VirtualServerForm, VirtualServerFilterForm, VirtualServerBulkEditForm, VirtualServerImportForm,
    PoolForm, PoolFilterForm, PoolBulkEditForm, PoolImportForm,
    PoolMemberForm, PoolMemberFilterForm, PoolMemberBulkEditForm, PoolMemberImportForm,
)
from . import panels


# --- LoadBalancer views ---

@register_model_view(LoadBalancer)
class LoadBalancerView(ObjectView):
    """Detail page for a single load balancer.

    Renders the LoadBalancerPanel in a SimpleLayout. The left_panels list contains
    the attribute panel; right_panels is empty (no sidebar widgets).
    """
    queryset = LoadBalancer.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.LoadBalancerPanel()],
        right_panels=[],
    )


@register_model_view(LoadBalancer, 'list', path='', detail=False)
class LoadBalancerListView(ObjectListView):
    """Paginated table of all load balancers with filtering and search.

    The ``path=''`` in the decorator makes this the default (index) view for the
    load balancer URL prefix. The ``detail=False`` indicates this is a collection
    view, not a single-object view.
    """
    queryset = LoadBalancer.objects.all()
    table = LoadBalancerTable
    filterset = LoadBalancerFilterSet
    filterset_form = LoadBalancerFilterForm


@register_model_view(LoadBalancer, 'add', detail=False)
@register_model_view(LoadBalancer, 'edit')
class LoadBalancerEditView(ObjectEditView):
    """Shared form view for both creating and editing load balancers.

    The two ``@register_model_view`` decorators register this single view class for
    both the 'add' action (creating new objects, ``detail=False``) and the 'edit'
    action (modifying existing objects, which requires a ``pk`` in the URL).
    """
    queryset = LoadBalancer.objects.all()
    form = LoadBalancerForm


@register_model_view(LoadBalancer, 'delete')
class LoadBalancerDeleteView(ObjectDeleteView):
    """Confirmation page for deleting a single load balancer.

    Deleting a load balancer will CASCADE-delete all of its pools and virtual servers.
    """
    queryset = LoadBalancer.objects.all()


@register_model_view(LoadBalancer, 'bulk_import', path='import', detail=False)
class LoadBalancerBulkImportView(BulkImportView):
    """CSV upload page for bulk-creating load balancers from a spreadsheet.

    Uses ``LoadBalancerImportForm`` to validate and parse each CSV row.
    """
    queryset = LoadBalancer.objects.all()
    model_form = LoadBalancerImportForm


@register_model_view(LoadBalancer, 'bulk_edit', path='edit', detail=False)
class LoadBalancerBulkEditView(BulkEditView):
    """Form for editing multiple selected load balancers at once.

    The user selects objects from the list view, then is presented with the
    ``LoadBalancerBulkEditForm`` to apply changes to all selected objects.
    """
    queryset = LoadBalancer.objects.all()
    table = LoadBalancerTable
    filterset = LoadBalancerFilterSet
    form = LoadBalancerBulkEditForm


@register_model_view(LoadBalancer, 'bulk_delete', path='delete', detail=False)
class LoadBalancerBulkDeleteView(BulkDeleteView):
    """Confirmation page for deleting multiple selected load balancers at once."""
    queryset = LoadBalancer.objects.all()
    table = LoadBalancerTable
    filterset = LoadBalancerFilterSet


# --- Pool views ---

@register_model_view(Pool)
class PoolView(ObjectView):
    """Detail page for a single pool, displaying its attributes via PoolPanel."""
    queryset = Pool.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.PoolPanel()],
        right_panels=[],
    )


@register_model_view(Pool, 'list', path='', detail=False)
class PoolListView(ObjectListView):
    """Paginated table of all pools with an annotated member count.

    The queryset uses ``.annotate(member_count=Count('members'))`` to add a computed
    ``member_count`` field to each pool. This value is displayed by the
    ``LinkedCountColumn`` in ``PoolTable`` as a clickable count that links to the
    filtered pool member list.
    """
    queryset = Pool.objects.annotate(member_count=Count('members'))
    table = PoolTable
    filterset = PoolFilterSet
    filterset_form = PoolFilterForm


@register_model_view(Pool, 'add', detail=False)
@register_model_view(Pool, 'edit')
class PoolEditView(ObjectEditView):
    """Shared form view for both creating and editing pools."""
    queryset = Pool.objects.all()
    form = PoolForm


@register_model_view(Pool, 'delete')
class PoolDeleteView(ObjectDeleteView):
    """Confirmation page for deleting a single pool.

    Deleting a pool will CASCADE-delete all of its pool members.
    """
    queryset = Pool.objects.all()


@register_model_view(Pool, 'bulk_import', path='import', detail=False)
class PoolBulkImportView(BulkImportView):
    """CSV upload page for bulk-creating pools from a spreadsheet."""
    queryset = Pool.objects.all()
    model_form = PoolImportForm


@register_model_view(Pool, 'bulk_edit', path='edit', detail=False)
class PoolBulkEditView(BulkEditView):
    """Form for editing multiple selected pools at once.

    The queryset includes the member_count annotation so the table renders correctly.
    """
    queryset = Pool.objects.annotate(member_count=Count('members'))
    table = PoolTable
    filterset = PoolFilterSet
    form = PoolBulkEditForm


@register_model_view(Pool, 'bulk_delete', path='delete', detail=False)
class PoolBulkDeleteView(BulkDeleteView):
    """Confirmation page for deleting multiple selected pools at once."""
    queryset = Pool.objects.annotate(member_count=Count('members'))
    table = PoolTable
    filterset = PoolFilterSet


# --- VirtualServer views ---

@register_model_view(VirtualServer)
class VirtualServerView(ObjectView):
    """Detail page for a single virtual server, displaying its attributes via VirtualServerPanel."""
    queryset = VirtualServer.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.VirtualServerPanel()],
        right_panels=[],
    )


@register_model_view(VirtualServer, 'list', path='', detail=False)
class VirtualServerListView(ObjectListView):
    """Paginated table of all virtual servers with filtering and search."""
    queryset = VirtualServer.objects.all()
    table = VirtualServerTable
    filterset = VirtualServerFilterSet
    filterset_form = VirtualServerFilterForm


@register_model_view(VirtualServer, 'add', detail=False)
@register_model_view(VirtualServer, 'edit')
class VirtualServerEditView(ObjectEditView):
    """Shared form view for both creating and editing virtual servers."""
    queryset = VirtualServer.objects.all()
    form = VirtualServerForm


@register_model_view(VirtualServer, 'delete')
class VirtualServerDeleteView(ObjectDeleteView):
    """Confirmation page for deleting a single virtual server."""
    queryset = VirtualServer.objects.all()


@register_model_view(VirtualServer, 'bulk_import', path='import', detail=False)
class VirtualServerBulkImportView(BulkImportView):
    """CSV upload page for bulk-creating virtual servers from a spreadsheet."""
    queryset = VirtualServer.objects.all()
    model_form = VirtualServerImportForm


@register_model_view(VirtualServer, 'bulk_edit', path='edit', detail=False)
class VirtualServerBulkEditView(BulkEditView):
    """Form for editing multiple selected virtual servers at once."""
    queryset = VirtualServer.objects.all()
    table = VirtualServerTable
    filterset = VirtualServerFilterSet
    form = VirtualServerBulkEditForm


@register_model_view(VirtualServer, 'bulk_delete', path='delete', detail=False)
class VirtualServerBulkDeleteView(BulkDeleteView):
    """Confirmation page for deleting multiple selected virtual servers at once."""
    queryset = VirtualServer.objects.all()
    table = VirtualServerTable
    filterset = VirtualServerFilterSet


# --- PoolMember views ---

@register_model_view(PoolMember)
class PoolMemberView(ObjectView):
    """Detail page for a single pool member, displaying its attributes via PoolMemberPanel."""
    queryset = PoolMember.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.PoolMemberPanel()],
        right_panels=[],
    )


@register_model_view(PoolMember, 'list', path='', detail=False)
class PoolMemberListView(ObjectListView):
    """Paginated table of all pool members with filtering and search."""
    queryset = PoolMember.objects.all()
    table = PoolMemberTable
    filterset = PoolMemberFilterSet
    filterset_form = PoolMemberFilterForm


@register_model_view(PoolMember, 'add', detail=False)
@register_model_view(PoolMember, 'edit')
class PoolMemberEditView(ObjectEditView):
    """Shared form view for both creating and editing pool members."""
    queryset = PoolMember.objects.all()
    form = PoolMemberForm


@register_model_view(PoolMember, 'delete')
class PoolMemberDeleteView(ObjectDeleteView):
    """Confirmation page for deleting a single pool member."""
    queryset = PoolMember.objects.all()


@register_model_view(PoolMember, 'bulk_import', path='import', detail=False)
class PoolMemberBulkImportView(BulkImportView):
    """CSV upload page for bulk-creating pool members from a spreadsheet."""
    queryset = PoolMember.objects.all()
    model_form = PoolMemberImportForm


@register_model_view(PoolMember, 'bulk_edit', path='edit', detail=False)
class PoolMemberBulkEditView(BulkEditView):
    """Form for editing multiple selected pool members at once."""
    queryset = PoolMember.objects.all()
    table = PoolMemberTable
    filterset = PoolMemberFilterSet
    form = PoolMemberBulkEditForm


@register_model_view(PoolMember, 'bulk_delete', path='delete', detail=False)
class PoolMemberBulkDeleteView(BulkDeleteView):
    """Confirmation page for deleting multiple selected pool members at once."""
    queryset = PoolMember.objects.all()
    table = PoolMemberTable
    filterset = PoolMemberFilterSet
