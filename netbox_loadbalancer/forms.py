"""Form classes for creating, editing, filtering, bulk-editing, and importing
load balancer objects.
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
    """Form for creating and editing a load balancer."""
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
    """Filter form for narrowing down load balancer lists by platform, status, site, or tenant."""
    model = LoadBalancer
    platform = forms.MultipleChoiceField(choices=LoadBalancerPlatformChoices, required=False)
    status = forms.MultipleChoiceField(choices=LoadBalancerStatusChoices, required=False)
    site_id = DynamicModelChoiceField(queryset=Site.objects.all(), required=False, label='Site')
    tenant_id = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False, label='Tenant')


class LoadBalancerBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple load balancers at once."""
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
    """Form for creating and editing a pool."""
    loadbalancer = DynamicModelChoiceField(queryset=LoadBalancer.objects.all(), label='Load Balancer')

    fieldsets = (
        FieldSet('name', 'loadbalancer', 'method', 'protocol', 'description', name='Pool'),
        FieldSet('tags', name='Tags'),
    )

    class Meta:
        model = Pool
        fields = ('name', 'loadbalancer', 'method', 'protocol', 'description', 'tags')


class PoolFilterForm(NetBoxModelFilterSetForm):
    """Filter form for narrowing down pool lists by load balancer, method, or protocol."""
    model = Pool
    loadbalancer_id = DynamicModelChoiceField(
        queryset=LoadBalancer.objects.all(), required=False, label='Load Balancer',
    )
    method = forms.MultipleChoiceField(choices=PoolMethodChoices, required=False)
    protocol = forms.MultipleChoiceField(choices=PoolProtocolChoices, required=False)


class PoolBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple pools at once."""
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
    """Form for creating and editing a virtual server."""
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
    """Filter form for narrowing down virtual server lists by load balancer, status, protocol, pool, or tenant."""
    model = VirtualServer
    loadbalancer_id = DynamicModelChoiceField(
        queryset=LoadBalancer.objects.all(), required=False, label='Load Balancer',
    )
    status = forms.MultipleChoiceField(choices=VirtualServerStatusChoices, required=False)
    protocol = forms.MultipleChoiceField(choices=VirtualServerProtocolChoices, required=False)
    pool_id = DynamicModelChoiceField(queryset=Pool.objects.all(), required=False, label='Pool')
    tenant_id = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False, label='Tenant')


class VirtualServerBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple virtual servers at once."""
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
    """Form for creating and editing a pool member."""
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
    """Filter form for narrowing down pool member lists by pool, status, or device."""
    model = PoolMember
    pool_id = DynamicModelChoiceField(queryset=Pool.objects.all(), required=False, label='Pool')
    status = forms.MultipleChoiceField(choices=PoolMemberStatusChoices, required=False)
    device_id = DynamicModelChoiceField(queryset=Device.objects.all(), required=False, label='Device')


class PoolMemberBulkEditForm(NetBoxModelBulkEditForm):
    """Bulk edit form for modifying multiple pool members at once."""
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
    """CSV import form for bulk-creating load balancers."""
    platform = CSVChoiceField(choices=LoadBalancerPlatformChoices, help_text='Platform type')
    status = CSVChoiceField(choices=LoadBalancerStatusChoices, required=False, help_text='Operational status')
    site = CSVModelChoiceField(queryset=Site.objects.all(), to_field_name='name', required=False, help_text='Assigned site')
    tenant = CSVModelChoiceField(queryset=Tenant.objects.all(), to_field_name='name', required=False, help_text='Assigned tenant')

    class Meta:
        model = LoadBalancer
        fields = ('name', 'platform', 'status', 'site', 'tenant', 'description', 'tags')


class PoolImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating pools."""
    loadbalancer = CSVModelChoiceField(queryset=LoadBalancer.objects.all(), to_field_name='name', help_text='Parent load balancer')
    method = CSVChoiceField(choices=PoolMethodChoices, required=False, help_text='Load balancing method')
    protocol = CSVChoiceField(choices=PoolProtocolChoices, required=False, help_text='Pool protocol')

    class Meta:
        model = Pool
        fields = ('name', 'loadbalancer', 'method', 'protocol', 'description', 'tags')


class VirtualServerImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating virtual servers."""
    loadbalancer = CSVModelChoiceField(queryset=LoadBalancer.objects.all(), to_field_name='name', help_text='Parent load balancer')
    protocol = CSVChoiceField(choices=VirtualServerProtocolChoices, required=False, help_text='Protocol')
    status = CSVChoiceField(choices=VirtualServerStatusChoices, required=False, help_text='Operational status')
    pool = CSVModelChoiceField(queryset=Pool.objects.all(), to_field_name='name', required=False, help_text='Assigned pool')
    tenant = CSVModelChoiceField(queryset=Tenant.objects.all(), to_field_name='name', required=False, help_text='Assigned tenant')

    class Meta:
        model = VirtualServer
        fields = ('name', 'loadbalancer', 'port', 'protocol', 'status', 'pool', 'tenant', 'description', 'tags')


class PoolMemberImportForm(NetBoxModelImportForm):
    """CSV import form for bulk-creating pool members."""
    pool = CSVModelChoiceField(queryset=Pool.objects.all(), to_field_name='name', help_text='Parent pool')
    status = CSVChoiceField(choices=PoolMemberStatusChoices, required=False, help_text='Operational status')

    class Meta:
        model = PoolMember
        fields = ('name', 'pool', 'port', 'weight', 'priority', 'status', 'description', 'tags')
