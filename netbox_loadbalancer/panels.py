"""UI panels for displaying object attributes on detail views."""

from netbox.ui import attrs, panels


class LoadBalancerPanel(panels.ObjectAttributesPanel):
    """Detail panel showing load balancer attributes including platform, status, and related objects."""
    name = attrs.TextAttr('name')
    platform = attrs.ChoiceAttr('platform')
    status = attrs.ChoiceAttr('status')
    device = attrs.RelatedObjectAttr('device', linkify=True)
    site = attrs.RelatedObjectAttr('site', linkify=True)
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True)
    management_ip = attrs.RelatedObjectAttr('management_ip', linkify=True)
    description = attrs.TextAttr('description')


class PoolPanel(panels.ObjectAttributesPanel):
    """Detail panel showing pool attributes including load balancer, method, and protocol."""
    name = attrs.TextAttr('name')
    loadbalancer = attrs.RelatedObjectAttr('loadbalancer', linkify=True)
    method = attrs.ChoiceAttr('method')
    protocol = attrs.ChoiceAttr('protocol')
    description = attrs.TextAttr('description')


class VirtualServerPanel(panels.ObjectAttributesPanel):
    """Detail panel showing virtual server attributes including VIP address, port, and pool assignment."""
    name = attrs.TextAttr('name')
    loadbalancer = attrs.RelatedObjectAttr('loadbalancer', linkify=True)
    ip_address = attrs.RelatedObjectAttr('ip_address', linkify=True)
    port = attrs.TextAttr('port')
    protocol = attrs.ChoiceAttr('protocol')
    status = attrs.ChoiceAttr('status')
    pool = attrs.RelatedObjectAttr('pool', linkify=True)
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True)
    description = attrs.TextAttr('description')


class PoolMemberPanel(panels.ObjectAttributesPanel):
    """Detail panel showing pool member attributes including IP, device, port, weight, and priority."""
    name = attrs.TextAttr('name')
    pool = attrs.RelatedObjectAttr('pool', linkify=True)
    ip_address = attrs.RelatedObjectAttr('ip_address', linkify=True)
    device = attrs.RelatedObjectAttr('device', linkify=True)
    port = attrs.TextAttr('port')
    weight = attrs.TextAttr('weight')
    priority = attrs.TextAttr('priority')
    status = attrs.ChoiceAttr('status')
    description = attrs.TextAttr('description')
