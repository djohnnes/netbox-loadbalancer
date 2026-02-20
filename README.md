# NetBox Load Balancer Plugin

A [NetBox](https://github.com/netbox-community/netbox) plugin for managing load balancers, virtual servers, pools, and pool members.

**Version:** 0.1.0

## Why This Plugin?

### The Problem

NetBox natively tracks devices, IPs, sites, and tenants — but has **no concept of load balancing**. Teams end up documenting load balancer configurations in spreadsheets, wiki pages, or vendor-specific management tools, creating information silos that are disconnected from the rest of their network source of truth.

### What This Plugin Adds

A complete load balancing data model integrated directly into NetBox:

**Single source of truth** — Load balancers, VIPs, pools, and members live alongside your devices, IPs, and sites. No more cross-referencing spreadsheets with NetBox to find which IP is a VIP or which device runs the load balancer.

**Relationship visibility** — You can trace the full traffic path: which virtual server listens on which VIP, which pool it routes to, and which backend members serve the traffic. Foreign key links to existing NetBox objects (devices, IPs, sites, tenants) tie load balancing into your broader infrastructure map.

**Operational awareness** — Status tracking (active, planned, maintenance, drain, disabled, decommissioned) across all objects gives teams a clear picture of what's in production, what's being deployed, and what's being retired.

**Multi-vendor support** — Platform-agnostic model covers F5, HAProxy, Citrix, NGINX, AWS ALB, Azure LB, and others. You document the logical configuration regardless of vendor, making it useful for mixed environments.

**Full NetBox integration** — Everything you expect from a first-class NetBox object:
- REST API with full CRUD, filtering, and bulk operations
- CSV bulk import for migrating existing data from spreadsheets
- Global search (find VIPs and members from the search bar)
- Tags and custom fields for your own metadata
- Change logging and audit trail
- Tenant assignment for multi-team environments

**Day-to-day use cases:**
- Quickly answer "what backends serve this VIP?" or "what VIPs does this server sit behind?"
- Audit all load balancers at a site before a maintenance window
- Bulk-drain pool members on a server before patching
- Track planned vs active load balancer deployments
- Hand off load balancer documentation to new team members with zero tribal knowledge

## Features

- Model and track load balancers across multiple platforms (F5, HAProxy, Citrix, NGINX, AWS, Azure)
- Define virtual servers (VIPs) with IP, port, and protocol settings
- Manage server pools with configurable load balancing methods
- Track pool members with weight, priority, and health status
- Full REST API with filtering, bulk operations, and brief mode
- NetBox UI integration with navigation, search, tables, and forms
- Tag support on all models
- Filterset support for all model fields

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
| 4.0+           | 0.1.x          |

## Installation

1. Add the plugin to your NetBox `local_requirements.txt` or install it:

```bash
pip install netbox-loadbalancer
```

2. Enable the plugin in `configuration.py`:

```python
PLUGINS = [
    'netbox_loadbalancer',
]
```

3. Run database migrations:

```bash
python manage.py migrate netbox_loadbalancer
```

4. Restart NetBox services.

## Models

| Model | Description | Key Fields |
|-------|-------------|------------|
| **LoadBalancer** | A load balancer appliance or service | name, platform, status, device, site, tenant, management_ip |
| **Pool** | A backend server pool belonging to a load balancer | name, loadbalancer, method, protocol |
| **VirtualServer** | A virtual server (VIP) fronting a pool | name, loadbalancer, ip_address, port, protocol, status, pool, tenant |
| **PoolMember** | A member of a server pool | name, pool, ip_address, device, port, weight, priority, status |

### Status Choices

- **LoadBalancer:** Active, Planned, Maintenance, Decommissioned
- **VirtualServer:** Active, Planned, Disabled
- **PoolMember:** Active, Drain, Disabled

### Platform Choices

F5 BIG-IP, HAProxy, Citrix ADC, NGINX, AWS ELB/ALB, Azure LB, Other

### Pool Methods

Round Robin, Least Connections, IP Hash, Weighted, Other

## Usage

### Web UI

Navigate to **Plugins > Load Balancer** in the NetBox menu to manage all objects.

### REST API

All endpoints are available under `/api/plugins/loadbalancer/`.

| Endpoint | Description |
|----------|-------------|
| `/api/plugins/loadbalancer/loadbalancers/` | Load Balancers |
| `/api/plugins/loadbalancer/pools/` | Pools |
| `/api/plugins/loadbalancer/virtual-servers/` | Virtual Servers |
| `/api/plugins/loadbalancer/pool-members/` | Pool Members |

#### Example: Create a Load Balancer

```bash
curl -X POST \
  -H "Authorization: Token $NETBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "lb-prod-01", "platform": "f5", "status": "active"}' \
  https://netbox.example.com/api/plugins/loadbalancer/loadbalancers/
```

#### Example: Create a Pool

```bash
curl -X POST \
  -H "Authorization: Token $NETBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "web-pool", "loadbalancer": 1, "method": "round-robin", "protocol": "http"}' \
  https://netbox.example.com/api/plugins/loadbalancer/pools/
```

## Development

### Running Tests

From the NetBox Docker environment:

```bash
docker compose exec netbox python /opt/netbox/netbox/manage.py test netbox_loadbalancer --verbosity=2
```

### Test Coverage

The test suite includes:
- **Model tests** -- object creation, `__str__()`, `get_absolute_url()`
- **API tests** -- GET, POST, PATCH, DELETE, bulk operations, brief mode
- **View tests** -- list, detail, create, edit, delete, bulk edit, bulk delete, changelog, permissions
- **FilterSet tests** -- all model fields, search, multi-value filters

## Author

David Johnnes ([david.johnnes@gmail.com](mailto:david.johnnes@gmail.com))

## License

Apache License 2.0. See [LICENSE](LICENSE).
