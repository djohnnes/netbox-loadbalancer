"""Views for the netbox_loadbalancer plugin.

Provides list, detail, create/edit, delete, bulk import, bulk edit, and bulk delete
views for each of the four core models.
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
    """Detail view for a single load balancer."""
    queryset = LoadBalancer.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.LoadBalancerPanel()],
        right_panels=[],
    )


@register_model_view(LoadBalancer, 'list', path='', detail=False)
class LoadBalancerListView(ObjectListView):
    """List view for load balancers with filtering support."""
    queryset = LoadBalancer.objects.all()
    table = LoadBalancerTable
    filterset = LoadBalancerFilterSet
    filterset_form = LoadBalancerFilterForm


@register_model_view(LoadBalancer, 'add', detail=False)
@register_model_view(LoadBalancer, 'edit')
class LoadBalancerEditView(ObjectEditView):
    """Create and edit view for load balancers."""
    queryset = LoadBalancer.objects.all()
    form = LoadBalancerForm


@register_model_view(LoadBalancer, 'delete')
class LoadBalancerDeleteView(ObjectDeleteView):
    """Delete view for a single load balancer."""
    queryset = LoadBalancer.objects.all()


@register_model_view(LoadBalancer, 'bulk_import', path='import', detail=False)
class LoadBalancerBulkImportView(BulkImportView):
    """CSV bulk import view for load balancers."""
    queryset = LoadBalancer.objects.all()
    model_form = LoadBalancerImportForm


@register_model_view(LoadBalancer, 'bulk_edit', path='edit', detail=False)
class LoadBalancerBulkEditView(BulkEditView):
    """Bulk edit view for modifying multiple load balancers."""
    queryset = LoadBalancer.objects.all()
    table = LoadBalancerTable
    filterset = LoadBalancerFilterSet
    form = LoadBalancerBulkEditForm


@register_model_view(LoadBalancer, 'bulk_delete', path='delete', detail=False)
class LoadBalancerBulkDeleteView(BulkDeleteView):
    """Bulk delete view for removing multiple load balancers."""
    queryset = LoadBalancer.objects.all()
    table = LoadBalancerTable
    filterset = LoadBalancerFilterSet


# --- Pool views ---

@register_model_view(Pool)
class PoolView(ObjectView):
    """Detail view for a single pool."""
    queryset = Pool.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.PoolPanel()],
        right_panels=[],
    )


@register_model_view(Pool, 'list', path='', detail=False)
class PoolListView(ObjectListView):
    """List view for pools with an annotated member count."""
    queryset = Pool.objects.annotate(member_count=Count('members'))
    table = PoolTable
    filterset = PoolFilterSet
    filterset_form = PoolFilterForm


@register_model_view(Pool, 'add', detail=False)
@register_model_view(Pool, 'edit')
class PoolEditView(ObjectEditView):
    """Create and edit view for pools."""
    queryset = Pool.objects.all()
    form = PoolForm


@register_model_view(Pool, 'delete')
class PoolDeleteView(ObjectDeleteView):
    """Delete view for a single pool."""
    queryset = Pool.objects.all()


@register_model_view(Pool, 'bulk_import', path='import', detail=False)
class PoolBulkImportView(BulkImportView):
    """CSV bulk import view for pools."""
    queryset = Pool.objects.all()
    model_form = PoolImportForm


@register_model_view(Pool, 'bulk_edit', path='edit', detail=False)
class PoolBulkEditView(BulkEditView):
    """Bulk edit view for modifying multiple pools."""
    queryset = Pool.objects.annotate(member_count=Count('members'))
    table = PoolTable
    filterset = PoolFilterSet
    form = PoolBulkEditForm


@register_model_view(Pool, 'bulk_delete', path='delete', detail=False)
class PoolBulkDeleteView(BulkDeleteView):
    """Bulk delete view for removing multiple pools."""
    queryset = Pool.objects.annotate(member_count=Count('members'))
    table = PoolTable
    filterset = PoolFilterSet


# --- VirtualServer views ---

@register_model_view(VirtualServer)
class VirtualServerView(ObjectView):
    """Detail view for a single virtual server."""
    queryset = VirtualServer.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.VirtualServerPanel()],
        right_panels=[],
    )


@register_model_view(VirtualServer, 'list', path='', detail=False)
class VirtualServerListView(ObjectListView):
    """List view for virtual servers with filtering support."""
    queryset = VirtualServer.objects.all()
    table = VirtualServerTable
    filterset = VirtualServerFilterSet
    filterset_form = VirtualServerFilterForm


@register_model_view(VirtualServer, 'add', detail=False)
@register_model_view(VirtualServer, 'edit')
class VirtualServerEditView(ObjectEditView):
    """Create and edit view for virtual servers."""
    queryset = VirtualServer.objects.all()
    form = VirtualServerForm


@register_model_view(VirtualServer, 'delete')
class VirtualServerDeleteView(ObjectDeleteView):
    """Delete view for a single virtual server."""
    queryset = VirtualServer.objects.all()


@register_model_view(VirtualServer, 'bulk_import', path='import', detail=False)
class VirtualServerBulkImportView(BulkImportView):
    """CSV bulk import view for virtual servers."""
    queryset = VirtualServer.objects.all()
    model_form = VirtualServerImportForm


@register_model_view(VirtualServer, 'bulk_edit', path='edit', detail=False)
class VirtualServerBulkEditView(BulkEditView):
    """Bulk edit view for modifying multiple virtual servers."""
    queryset = VirtualServer.objects.all()
    table = VirtualServerTable
    filterset = VirtualServerFilterSet
    form = VirtualServerBulkEditForm


@register_model_view(VirtualServer, 'bulk_delete', path='delete', detail=False)
class VirtualServerBulkDeleteView(BulkDeleteView):
    """Bulk delete view for removing multiple virtual servers."""
    queryset = VirtualServer.objects.all()
    table = VirtualServerTable
    filterset = VirtualServerFilterSet


# --- PoolMember views ---

@register_model_view(PoolMember)
class PoolMemberView(ObjectView):
    """Detail view for a single pool member."""
    queryset = PoolMember.objects.all()
    layout = SimpleLayout(
        left_panels=[panels.PoolMemberPanel()],
        right_panels=[],
    )


@register_model_view(PoolMember, 'list', path='', detail=False)
class PoolMemberListView(ObjectListView):
    """List view for pool members with filtering support."""
    queryset = PoolMember.objects.all()
    table = PoolMemberTable
    filterset = PoolMemberFilterSet
    filterset_form = PoolMemberFilterForm


@register_model_view(PoolMember, 'add', detail=False)
@register_model_view(PoolMember, 'edit')
class PoolMemberEditView(ObjectEditView):
    """Create and edit view for pool members."""
    queryset = PoolMember.objects.all()
    form = PoolMemberForm


@register_model_view(PoolMember, 'delete')
class PoolMemberDeleteView(ObjectDeleteView):
    """Delete view for a single pool member."""
    queryset = PoolMember.objects.all()


@register_model_view(PoolMember, 'bulk_import', path='import', detail=False)
class PoolMemberBulkImportView(BulkImportView):
    """CSV bulk import view for pool members."""
    queryset = PoolMember.objects.all()
    model_form = PoolMemberImportForm


@register_model_view(PoolMember, 'bulk_edit', path='edit', detail=False)
class PoolMemberBulkEditView(BulkEditView):
    """Bulk edit view for modifying multiple pool members."""
    queryset = PoolMember.objects.all()
    table = PoolMemberTable
    filterset = PoolMemberFilterSet
    form = PoolMemberBulkEditForm


@register_model_view(PoolMember, 'bulk_delete', path='delete', detail=False)
class PoolMemberBulkDeleteView(BulkDeleteView):
    """Bulk delete view for removing multiple pool members."""
    queryset = PoolMember.objects.all()
    table = PoolMemberTable
    filterset = PoolMemberFilterSet
