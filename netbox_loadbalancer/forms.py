"""Form classes for the netbox_loadbalancer plugin.

NetBox uses four distinct form types for each model, and this module defines all
four for each of the plugin's models:

1. **NetBoxModelForm** (e.g. ``LoadBalancerForm``): used on the create/edit pages.
   Fields that reference other NetBox objects use ``DynamicModelChoiceField``, which
   renders as a searchable dropdown that fetches options via AJAX. The ``fieldsets``
   attribute controls how fields are visually grouped in the UI.

2. **NetBoxModelFilterSetForm** (e.g. ``LoadBalancerFilterForm``): renders the filter
   sidebar on list views. Uses ``MultipleChoiceField`` for choice-based filters
   (allowing the user to select several values at once) and ``DynamicModelChoiceField``
   for related-object filters.

3. **NetBoxModelBulkEditForm** (e.g. ``LoadBalancerBulkEditForm``): used when editing
   multiple objects at once. All fields are optional (``required=False``) because the
   user only fills in the fields they want to change. The ``nullable_fields`` tuple
   lists fields that can be explicitly cleared (set to NULL) during a bulk edit.

4. **NetBoxModelImportForm** (e.g. ``LoadBalancerImportForm``): used for CSV bulk
   import. Uses ``CSVChoiceField`` for choice fields and ``CSVModelChoiceField`` for
   foreign keys, which resolve objects by name (the ``to_field_name`` parameter)
   rather than by primary key.
"""

from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from netbox.forms.bulk_import import NetBoxModelImportForm
from utilities.forms.fields import CSVChoiceField, CSVModelChoiceField, DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from dcim.models import Device, Site
from ipam.models import IPAddress
from tenancy.models import Tenant

from .models import LoadBalancer, VirtualServer, Pool, PoolMember
from .choices import (
    LoadBalancerPlatformChoices,
    LoadBalancerStatusChoices,
    VirtualServerStatusChoices,
    VirtualServerProtocolChoices,
    PoolMethodChoices,
    PoolProtocolChoices,
    PoolMemberStatusChoices,
)


# --- LoadBalancer forms ---

class LoadBalancerForm(NetBoxModelForm):
    """Form for creating and editing a single load balancer.

    DynamicModelChoiceField is used for device, site, tenant, and management_ip so
    that the UI renders searchable dropdowns that load options via AJAX. The fieldsets
    tuple groups fields into logical sections: core attributes, assignment fields, and
    tags. The Meta.fields tuple determines which model fields are included in the form.
    """
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    management_ip = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label='Management IP')

    fieldsets = (
        FieldSet('name', 'platform', 'status', 'description', name='Load Balancer'),
        FieldSet('device', 'site', 'tenant', 'management_ip', name='Assignment'),
        FieldSet('tags', name='Tags'),
    )

    class Meta:
        model = LoadBalancer
        fields = ('name', 'platform', 'status', 'device', 'site', 'tenant', 'management_ip', 'description', 'tags')


class LoadBalancerFilterForm(NetBoxModelFilterSetForm):
    """Filter sidebar form for the load balancer list view.

    Renders filter widgets in the sidebar panel. MultipleChoiceField allows the user to
    select several platforms or statuses simultaneously (e.g. show only 'active' and
    'planned' load balancers). DynamicModelChoiceField provides AJAX-powered dropdowns
    for site and tenant filtering.
    """
    model = LoadBalancer
    platform = forms.MultipleChoiceField(choices=LoadBalancerPlatformChoices, required=False)
    status = forms.MultipleChoiceField(choices=LoadBalancerStatusChoices, required=False)
    site_id = DynamicModelChoiceField(queryset=Site.objects.all(), required=False, label='Site')
    tenant_id = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False, label='Tenant')


class LoadBalancerBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple load balancers simultaneously.

    All fields are optional — the user only fills in the fields they want to change
    across the selected objects. The ``nullable_fields`` tuple lists fields (site,
    tenant, description) that can be explicitly cleared (set to NULL/blank) during
    a bulk edit operation.
    """
    model = LoadBalancer
    platform = forms.ChoiceField(choices=LoadBalancerPlatformChoices, required=False)
    status = forms.ChoiceField(choices=LoadBalancerStatusChoices, required=False)
    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    description = forms.CharField(max_length=500, required=False)

    fieldsets = (
        FieldSet('platform', 'status', 'site', 'tenant', 'description'),
    )
    nullable_fields = ('site', 'tenant', 'description')


# --- Pool forms ---

class PoolForm(NetBoxModelForm):
    """Form for creating and editing a single pool.

    The loadbalancer field uses DynamicModelChoiceField to present a searchable
    dropdown of all load balancers. The method and protocol fields use the model's
    default CharField choices so they render as standard select dropdowns.
    """
    loadbalancer = DynamicModelChoiceField(queryset=LoadBalancer.objects.all(), label='Load Balancer')

    fieldsets = (
        FieldSet('name', 'loadbalancer', 'method', 'protocol', 'description', name='Pool'),
        FieldSet('tags', name='Tags'),
    )

    class Meta:
        model = Pool
        fields = ('name', 'loadbalancer', 'method', 'protocol', 'description', 'tags')


class PoolFilterForm(NetBoxModelFilterSetForm):
    """Filter sidebar form for the pool list view.

    Allows filtering pools by their parent load balancer, load balancing method, and
    protocol. The loadbalancer_id field uses DynamicModelChoiceField so the user can
    search for a load balancer by name.
    """
    model = Pool
    loadbalancer_id = DynamicModelChoiceField(
        queryset=LoadBalancer.objects.all(), required=False, label='Load Balancer',
    )
    method = forms.MultipleChoiceField(choices=PoolMethodChoices, required=False)
    protocol = forms.MultipleChoiceField(choices=PoolProtocolChoices, required=False)


class PoolBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple pools simultaneously.

    Allows changing the method, protocol, and description of several pools at once.
    The description field is listed in ``nullable_fields`` so it can be cleared.
    """
    model = Pool
    method = forms.ChoiceField(choices=PoolMethodChoices, required=False)
    protocol = forms.ChoiceField(choices=PoolProtocolChoices, required=False)
    description = forms.CharField(max_length=500, required=False)

    fieldsets = (
        FieldSet('method', 'protocol', 'description'),
    )
    nullable_fields = ('description',)


# --- VirtualServer forms ---

class VirtualServerForm(NetBoxModelForm):
    """Form for creating and editing a single virtual server.

    The pool field uses ``query_params={'loadbalancer_id': '$loadbalancer'}`` to
    dynamically filter the pool dropdown based on the currently selected load balancer.
    The ``$loadbalancer`` syntax tells the frontend JavaScript to read the value from
    the loadbalancer field and pass it as a query parameter when fetching pool options,
    so only pools belonging to the selected load balancer are shown.
    """
    loadbalancer = DynamicModelChoiceField(queryset=LoadBalancer.objects.all(), label='Load Balancer')
    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label='VIP Address')
    pool = DynamicModelChoiceField(
        queryset=Pool.objects.all(),
        required=False,
        query_params={'loadbalancer_id': '$loadbalancer'},
    )
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    fieldsets = (
        FieldSet('name', 'loadbalancer', 'ip_address', 'port', 'protocol', 'status', 'description', name='Virtual Server'),
        FieldSet('pool', 'tenant', name='Assignment'),
        FieldSet('tags', name='Tags'),
    )

    class Meta:
        model = VirtualServer
        fields = (
            'name', 'loadbalancer', 'ip_address', 'port', 'protocol',
            'status', 'pool', 'tenant', 'description', 'tags',
        )


class VirtualServerFilterForm(NetBoxModelFilterSetForm):
    """Filter sidebar form for the virtual server list view.

    Provides filters for load balancer, status, protocol, pool, and tenant. All
    filters are optional and can be combined to narrow down the displayed results.
    """
    model = VirtualServer
    loadbalancer_id = DynamicModelChoiceField(
        queryset=LoadBalancer.objects.all(), required=False, label='Load Balancer',
    )
    status = forms.MultipleChoiceField(choices=VirtualServerStatusChoices, required=False)
    protocol = forms.MultipleChoiceField(choices=VirtualServerProtocolChoices, required=False)
    pool_id = DynamicModelChoiceField(queryset=Pool.objects.all(), required=False, label='Pool')
    tenant_id = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False, label='Tenant')


class VirtualServerBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple virtual servers simultaneously.

    Allows changing status, protocol, tenant, and description across several virtual
    servers at once. Tenant and description can be explicitly cleared via
    ``nullable_fields``.
    """
    model = VirtualServer
    status = forms.ChoiceField(choices=VirtualServerStatusChoices, required=False)
    protocol = forms.ChoiceField(choices=VirtualServerProtocolChoices, required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    description = forms.CharField(max_length=500, required=False)

    fieldsets = (
        FieldSet('status', 'protocol', 'tenant', 'description'),
    )
    nullable_fields = ('tenant', 'description')


# --- PoolMember forms ---

class PoolMemberForm(NetBoxModelForm):
    """Form for creating and editing a single pool member.

    The pool, ip_address, and device fields use DynamicModelChoiceField for searchable
    dropdowns. The port, weight, and priority fields use the model's default integer
    fields. Note that ip_address and device are optional — a pool member can be defined
    with just a name and port if the backend server is not yet registered in NetBox.
    """
    pool = DynamicModelChoiceField(queryset=Pool.objects.all())
    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label='IP Address')
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)

    fieldsets = (
        FieldSet('name', 'pool', 'ip_address', 'device', 'port', 'weight', 'priority', 'status', 'description', name='Pool Member'),
        FieldSet('tags', name='Tags'),
    )

    class Meta:
        model = PoolMember
        fields = (
            'name', 'pool', 'ip_address', 'device', 'port', 'weight',
            'priority', 'status', 'description', 'tags',
        )


class PoolMemberFilterForm(NetBoxModelFilterSetForm):
    """Filter sidebar form for the pool member list view.

    Allows filtering members by their parent pool, operational status, and associated
    device. All filters are optional.
    """
    model = PoolMember
    pool_id = DynamicModelChoiceField(queryset=Pool.objects.all(), required=False, label='Pool')
    status = forms.MultipleChoiceField(choices=PoolMemberStatusChoices, required=False)
    device_id = DynamicModelChoiceField(queryset=Device.objects.all(), required=False, label='Device')


class PoolMemberBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple pool members simultaneously.

    Allows changing status, weight, priority, and description across several pool
    members at once. This is useful for maintenance operations like draining all
    members on a particular server. Description can be cleared via ``nullable_fields``.
    """
    model = PoolMember
    status = forms.ChoiceField(choices=PoolMemberStatusChoices, required=False)
    weight = forms.IntegerField(min_value=0, required=False)
    priority = forms.IntegerField(min_value=0, required=False)
    description = forms.CharField(max_length=500, required=False)

    fieldsets = (
        FieldSet('status', 'weight', 'priority', 'description'),
    )
    nullable_fields = ('description',)


# --- Import forms ---

class LoadBalancerImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating load balancers from a spreadsheet.

    CSVChoiceField validates that the platform and status values in each CSV row match
    one of the defined choices. CSVModelChoiceField resolves site and tenant by name
    (``to_field_name='name'``) so users can reference them in the CSV by their
    human-readable names rather than database IDs.
    """
    platform = CSVChoiceField(choices=LoadBalancerPlatformChoices, help_text='Platform type')
    status = CSVChoiceField(choices=LoadBalancerStatusChoices, required=False, help_text='Operational status')
    site = CSVModelChoiceField(queryset=Site.objects.all(), to_field_name='name', required=False, help_text='Assigned site')
    tenant = CSVModelChoiceField(queryset=Tenant.objects.all(), to_field_name='name', required=False, help_text='Assigned tenant')

    class Meta:
        model = LoadBalancer
        fields = ('name', 'platform', 'status', 'site', 'tenant', 'description', 'tags')


class PoolImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating pools.

    The loadbalancer field resolves the parent load balancer by name from the CSV data.
    """
    loadbalancer = CSVModelChoiceField(queryset=LoadBalancer.objects.all(), to_field_name='name', help_text='Parent load balancer')
    method = CSVChoiceField(choices=PoolMethodChoices, required=False, help_text='Load balancing method')
    protocol = CSVChoiceField(choices=PoolProtocolChoices, required=False, help_text='Pool protocol')

    class Meta:
        model = Pool
        fields = ('name', 'loadbalancer', 'method', 'protocol', 'description', 'tags')


class VirtualServerImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating virtual servers.

    Resolves the parent load balancer, pool, and tenant by name from the CSV data.
    """
    loadbalancer = CSVModelChoiceField(queryset=LoadBalancer.objects.all(), to_field_name='name', help_text='Parent load balancer')
    protocol = CSVChoiceField(choices=VirtualServerProtocolChoices, required=False, help_text='Protocol')
    status = CSVChoiceField(choices=VirtualServerStatusChoices, required=False, help_text='Operational status')
    pool = CSVModelChoiceField(queryset=Pool.objects.all(), to_field_name='name', required=False, help_text='Assigned pool')
    tenant = CSVModelChoiceField(queryset=Tenant.objects.all(), to_field_name='name', required=False, help_text='Assigned tenant')

    class Meta:
        model = VirtualServer
        fields = ('name', 'loadbalancer', 'port', 'protocol', 'status', 'pool', 'tenant', 'description', 'tags')


class PoolMemberImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating pool members.

    Resolves the parent pool by name from the CSV data. The port, weight, and priority
    fields are parsed directly as integers from the CSV columns.
    """
    pool = CSVModelChoiceField(queryset=Pool.objects.all(), to_field_name='name', help_text='Parent pool')
    status = CSVChoiceField(choices=PoolMemberStatusChoices, required=False, help_text='Operational status')

    class Meta:
        model = PoolMember
        fields = ('name', 'pool', 'port', 'weight', 'priority', 'status', 'description', 'tags')
