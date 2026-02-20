"""UI panels for displaying object attributes on detail views.

Each panel class extends ``ObjectAttributesPanel`` and defines the attributes shown
on an object's detail page. NetBox renders these panels as card-like sections in the
page layout. The attribute types control how each field is displayed:

- ``TextAttr``: renders the field value as plain text.
- ``ChoiceAttr``: renders choice fields as coloured badges (same as in list tables).
- ``RelatedObjectAttr``: renders a foreign key as a clickable link (``linkify=True``)
  to the related object's detail page.

Panels are referenced in the corresponding ``ObjectView`` classes in ``views.py``,
where they are placed into a ``SimpleLayout`` to define the page structure.
"""

from netbox.ui import attrs, panels


class LoadBalancerPanel(panels.ObjectAttributesPanel):
    """Detail panel for the load balancer detail page.

    Displays all load balancer fields: name, platform and status as coloured badges,
    and device, site, tenant, and management_ip as clickable links to their respective
    detail pages in NetBox.
    """
    name = attrs.TextAttr('name')
    platform = attrs.ChoiceAttr('platform')
    status = attrs.ChoiceAttr('status')
    device = attrs.RelatedObjectAttr('device', linkify=True)
    site = attrs.RelatedObjectAttr('site', linkify=True)
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True)
    management_ip = attrs.RelatedObjectAttr('management_ip', linkify=True)
    description = attrs.TextAttr('description')


class PoolPanel(panels.ObjectAttributesPanel):
    """Detail panel for the pool detail page.

    Shows the pool's name, a clickable link to its parent load balancer, the load
    balancing method and protocol as coloured badges, and the description.
    """
    name = attrs.TextAttr('name')
    loadbalancer = attrs.RelatedObjectAttr('loadbalancer', linkify=True)
    method = attrs.ChoiceAttr('method')
    protocol = attrs.ChoiceAttr('protocol')
    description = attrs.TextAttr('description')


class VirtualServerPanel(panels.ObjectAttributesPanel):
    """Detail panel for the virtual server detail page.

    Displays the full virtual server configuration: name, parent load balancer link,
    VIP address link, port number, protocol and status badges, optional pool link,
    tenant link, and description.
    """
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
    """Detail panel for the pool member detail page.

    Shows the member's name, parent pool link, IP address and device links, port,
    weight, priority, status badge, and description. This is the most attribute-rich
    panel in the plugin.
    """
    name = attrs.TextAttr('name')
    pool = attrs.RelatedObjectAttr('pool', linkify=True)
    ip_address = attrs.RelatedObjectAttr('ip_address', linkify=True)
    device = attrs.RelatedObjectAttr('device', linkify=True)
    port = attrs.TextAttr('port')
    weight = attrs.TextAttr('weight')
    priority = attrs.TextAttr('priority')
    status = attrs.ChoiceAttr('status')
    description = attrs.TextAttr('description')
