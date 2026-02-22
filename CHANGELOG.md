# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-02-22

### Added

- LoadBalancer model with platform, status, device, site, tenant, and management IP fields
- Pool model with load balancing method and protocol configuration
- VirtualServer model with VIP address, port, protocol, status, and pool assignment
- PoolMember model with IP, device, port, weight, priority, and status fields
- Full REST API for all models (CRUD, bulk operations, brief mode)
- GraphQL API with filtering and pagination for all models
- Object cloning support for all models
- Web UI views with list, detail, create, edit, delete, and bulk operations
- CSV bulk import for all models
- FilterSets with search support for all models
- Navigation menu integration
- Global search indexing
- Port validation (1-65535) on VirtualServer and PoolMember
- Weight validation (1-65535) on PoolMember
- Duplicate pool member detection via clean() validation
- PyPI packaging as `netbox-loadbalancer-plugin`
- Comprehensive test suite (238 tests)
- Apache 2.0 license
