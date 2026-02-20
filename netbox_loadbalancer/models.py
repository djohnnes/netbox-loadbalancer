"""Data models for the netbox_loadbalancer plugin.

Defines the four core models — LoadBalancer, Pool, VirtualServer, and PoolMember —
that together represent a load balancing infrastructure within NetBox.
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

    A load balancer is the top-level object in the hierarchy. It may be optionally
    linked to a device, site, tenant, and management IP address. Pools and virtual
    servers are associated with a load balancer.
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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:loadbalancer', kwargs={'pk': self.pk})



class Pool(NetBoxModel):
    """Represents a pool of backend members that receive traffic from a load balancer.

    Each pool belongs to a single load balancer and defines a load balancing method
    and protocol. Pool names are unique within their parent load balancer.
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

    class Meta:
        ordering = ['loadbalancer', 'name']
        unique_together = ['loadbalancer', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:pool', kwargs={'pk': self.pk})


class VirtualServer(NetBoxModel):
    """Represents a virtual server (VIP) that listens for client traffic.

    A virtual server defines a frontend listener on a load balancer, identified by
    a name, IP address, port, and protocol combination. It may optionally be assigned
    to a pool that handles the backend traffic distribution.
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

    class Meta:
        ordering = ['loadbalancer', 'name']
        unique_together = ['loadbalancer', 'name', 'port', 'protocol']

    def __str__(self):
        return f'{self.name} ({self.get_protocol_display()}/{self.port})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:virtualserver', kwargs={'pk': self.pk})



class PoolMember(NetBoxModel):
    """Represents an individual backend server within a pool.

    A pool member is a destination that receives traffic distributed by its parent
    pool. Each member has a port, weight, and priority that influence how traffic is
    routed. Members are uniquely identified within a pool by the combination of IP
    address and port.
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
        validators=[MaxValueValidator(65535)],
    )
    priority = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=PoolMemberStatusChoices,
        default=PoolMemberStatusChoices.STATUS_ACTIVE,
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['pool', 'name']
        unique_together = ['pool', 'ip_address', 'port']

    def __str__(self):
        return f'{self.name}:{self.port}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_loadbalancer:poolmember', kwargs={'pk': self.pk})

    def clean(self):
        """Enforce unique-together constraint on pool, IP address, and port.

        Django's built-in unique_together cannot handle nullable fields (NULL != NULL
        in SQL), so this method manually checks for duplicates when ip_address is set.
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

