"""Data models for the netbox_loadbalancer plugin.

Defines the four core models that together represent a load balancing infrastructure
within NetBox. The object hierarchy is:

    LoadBalancer
    ├── Pool  (many-to-one: each pool belongs to one load balancer)
    │   └── PoolMember  (many-to-one: each member belongs to one pool)
    └── VirtualServer  (many-to-one: each VS belongs to one load balancer)
            └── optionally linked to a Pool for backend traffic distribution

All models extend ``NetBoxModel``, which is NetBox's base model class. It provides
built-in support for tags, custom fields, change logging, journaling, and the
standard NetBox REST API features. Every model must implement ``__str__()`` for
display and ``get_absolute_url()`` to link to its detail view.

Foreign key relationships use ``on_delete=models.CASCADE`` for mandatory parent
relationships (deleting a load balancer also deletes its pools and virtual servers)
and ``on_delete=models.SET_NULL`` for optional relationships (deleting a site does
not delete its load balancers — the field is simply cleared).
"""

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

from .choices import (
    LoadBalancerPlatformChoices,
    LoadBalancerStatusChoices,
    VirtualServerStatusChoices,
    VirtualServerProtocolChoices,
    PoolMethodChoices,
    PoolProtocolChoices,
    PoolMemberStatusChoices,
)


class LoadBalancer(NetBoxModel):
    """Represents a physical or virtual load balancer appliance.

    This is the top-level object in the plugin's data hierarchy. Real-world examples
    include F5 BIG-IP appliances, HAProxy instances, or cloud load balancers like
    AWS ALB. All pools and virtual servers must belong to exactly one load balancer.

    Optional foreign keys allow linking to existing NetBox objects:
    - ``device``: the physical or virtual device running the load balancer software
    - ``site``: the data centre or location where the load balancer resides
    - ``tenant``: the organisation or team that owns the load balancer
    - ``management_ip``: the IP address used for administrative access

    All optional FKs use ``on_delete=SET_NULL`` so that deleting a device or site
    does not cascade-delete the load balancer — the field is simply set to NULL.
    """

    name = models.CharField(max_length=200, unique=True)
    platform = models.CharField(
        max_length=50,
        choices=LoadBalancerPlatformChoices,
    )
    status = models.CharField(
        max_length=50,
        choices=LoadBalancerStatusChoices,
        default=LoadBalancerStatusChoices.STATUS_ACTIVE,
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='loadbalancers',
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='loadbalancers',
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='loadbalancers',
    )
    management_ip = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='loadbalancers',
        verbose_name='Management IP',
    )
    description = models.CharField(max_length=500, blank=True)

    clone_fields = ('platform', 'status', 'device', 'site', 'tenant', 'description')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:loadbalancer', kwargs={'pk': self.pk})



class Pool(NetBoxModel):
    """Represents a pool (also called a server farm or backend) of members that receive traffic.

    A pool groups together one or more backend servers (PoolMember objects) and defines
    how traffic is distributed among them. The ``method`` field selects the load
    balancing algorithm (e.g. round-robin, least-connections) and the ``protocol``
    field indicates what kind of traffic the pool handles (e.g. HTTP, TCP).

    Each pool belongs to exactly one load balancer via a CASCADE foreign key — if the
    parent load balancer is deleted, all of its pools are deleted too. Pool names are
    enforced unique within their parent load balancer by the ``unique_together``
    constraint on ``['loadbalancer', 'name']``.
    """

    name = models.CharField(max_length=200)
    loadbalancer = models.ForeignKey(
        to=LoadBalancer,
        on_delete=models.CASCADE,
        related_name='pools',
    )
    method = models.CharField(
        max_length=50,
        choices=PoolMethodChoices,
        default=PoolMethodChoices.METHOD_ROUND_ROBIN,
    )
    protocol = models.CharField(
        max_length=50,
        choices=PoolProtocolChoices,
        default=PoolProtocolChoices.PROTOCOL_HTTP,
    )
    description = models.CharField(max_length=500, blank=True)

    clone_fields = ('loadbalancer', 'method', 'protocol', 'description')

    class Meta:
        ordering = ['loadbalancer', 'name']
        unique_together = ['loadbalancer', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:pool', kwargs={'pk': self.pk})


class VirtualServer(NetBoxModel):
    """Represents a virtual server (VIP) that listens for incoming client traffic.

    In load balancing terminology, a virtual server is the frontend entry point that
    clients connect to. It is defined by a combination of an IP address (the "VIP"),
    a port number, and a protocol. For example, a virtual server might listen on
    ``10.0.0.1:443/HTTPS`` and forward matching traffic to a pool of web servers.

    Each virtual server belongs to exactly one load balancer (CASCADE). The ``pool``
    foreign key is optional (SET_NULL) — a virtual server can exist without a pool
    assignment, for example while being planned. The ``ip_address`` links to NetBox's
    built-in IPAM module for VIP tracking. The ``tenant`` allows ownership assignment.

    Uniqueness is enforced on ``['loadbalancer', 'name', 'port', 'protocol']`` so
    that the same load balancer cannot have two virtual servers with identical
    name/port/protocol combinations.
    """

    name = models.CharField(max_length=200)
    loadbalancer = models.ForeignKey(
        to=LoadBalancer,
        on_delete=models.CASCADE,
        related_name='virtual_servers',
    )
    ip_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='virtual_servers',
        verbose_name='VIP Address',
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    protocol = models.CharField(
        max_length=50,
        choices=VirtualServerProtocolChoices,
        default=VirtualServerProtocolChoices.PROTOCOL_HTTP,
    )
    status = models.CharField(
        max_length=50,
        choices=VirtualServerStatusChoices,
        default=VirtualServerStatusChoices.STATUS_ACTIVE,
    )
    pool = models.ForeignKey(
        to=Pool,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='virtual_servers',
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='virtual_servers',
    )
    description = models.CharField(max_length=500, blank=True)

    clone_fields = ('loadbalancer', 'protocol', 'status', 'pool', 'tenant', 'description')

    class Meta:
        ordering = ['loadbalancer', 'name']
        unique_together = ['loadbalancer', 'name', 'port', 'protocol']

    def __str__(self):
        return f'{self.name} ({self.get_protocol_display()}/{self.port})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:virtualserver', kwargs={'pk': self.pk})



class PoolMember(NetBoxModel):
    """Represents an individual backend server (node) within a pool.

    A pool member is a single destination that receives traffic distributed by its
    parent pool's load balancing algorithm. For example, if a pool uses round-robin,
    each request is sent to the next pool member in sequence.

    Key fields that influence traffic routing:
    - ``port``: the TCP/UDP port the backend application listens on (1-65535)
    - ``weight``: a relative value that determines how much traffic this member
      receives compared to other members (higher weight = more traffic). Defaults to 1.
    - ``priority``: used for active/standby configurations where lower-priority
      members only receive traffic when higher-priority members are unavailable.
    - ``status``: active members receive traffic, drain members finish existing
      connections but accept no new ones, and disabled members are completely offline.

    Each member belongs to exactly one pool (CASCADE). The optional ``ip_address``
    and ``device`` FKs link to NetBox's IPAM and DCIM modules. Members are uniquely
    identified within a pool by the combination of ``['pool', 'ip_address', 'port']``,
    but because ``ip_address`` is nullable, this constraint is enforced in the
    ``clean()`` method rather than purely at the database level.
    """

    name = models.CharField(max_length=200)
    pool = models.ForeignKey(
        to=Pool,
        on_delete=models.CASCADE,
        related_name='members',
    )
    ip_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pool_members',
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pool_members',
    )
    port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    weight = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    priority = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=PoolMemberStatusChoices,
        default=PoolMemberStatusChoices.STATUS_ACTIVE,
    )
    description = models.CharField(max_length=500, blank=True)

    clone_fields = ('pool', 'weight', 'priority', 'status', 'description')

    class Meta:
        ordering = ['pool', 'name']
        unique_together = ['pool', 'ip_address', 'port']

    def __str__(self):
        return f'{self.name}:{self.port}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:poolmember', kwargs={'pk': self.pk})

    def clean(self):
        """Enforce unique-together constraint on pool, IP address, and port.

        Django's built-in ``unique_together`` cannot handle nullable fields correctly
        because in SQL, ``NULL != NULL`` — meaning the database considers two rows with
        NULL ip_address as distinct, even if their pool and port match. This is the
        correct SQL behaviour but not what we want semantically.

        This method compensates by manually querying for existing members with the same
        pool, ip_address, and port whenever ip_address is not NULL. When editing an
        existing member (self.pk is set), the current instance is excluded from the
        duplicate check. If a duplicate is found, a ValidationError is raised and the
        save is prevented.
        """
        super().clean()
        if self.ip_address is not None:
            qs = PoolMember.objects.filter(
                pool=self.pool, ip_address=self.ip_address, port=self.port,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    'A pool member with this pool, IP address, and port already exists.'
                )

