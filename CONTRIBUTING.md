# Contributing to NetBox Load Balancer Plugin

Thanks for your interest in contributing! This guide covers how to set up a development environment, run tests, and submit changes.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork:

```bash
git clone https://github.com/<your-username>/netbox-loadbalancer.git
cd netbox-loadbalancer
```

3. Set up the Docker-based NetBox dev environment (see below).

## Development Environment

The easiest way to develop is with [netbox-docker](https://github.com/netbox-community/netbox-docker) and a volume mount that points NetBox at your local plugin source.

### 1. Clone netbox-docker

```bash
git clone https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
```

### 2. Create `docker-compose.override.yml`

Mount your local plugin source into the container so changes are reflected immediately without rebuilding:

```yaml
services:
  netbox:
    build:
      context: .
      dockerfile: Dockerfile-plugins
    ports:
      - "8000:8080"
    volumes:
      - /path/to/netbox-loadbalancer/netbox_loadbalancer:/opt/netbox/venv/lib/python3.12/site-packages/netbox_loadbalancer:ro
```

Replace `/path/to/netbox-loadbalancer` with the absolute path to your cloned fork.

### 3. Create `Dockerfile-plugins`

```dockerfile
ARG FROM=docker.io/netboxcommunity/netbox:v4.5-4.0.0
FROM ${FROM}

RUN /usr/local/bin/uv pip install --python /opt/netbox/venv/bin/python netbox-loadbalancer-plugin
```

The volume mount in the override file will overlay the installed package with your local source.

### 4. Enable the plugin

Create (or edit) `configuration/plugins.py`:

```python
PLUGINS = [
    'netbox_loadbalancer',
]

PLUGINS_CONFIG = {}
```

### 5. Start NetBox

```bash
docker compose up -d
```

NetBox will be available at `http://localhost:8000`. Edit plugin source files locally and restart the NetBox container to pick up changes:

```bash
docker compose restart netbox
```

## Running Tests

Tests must run through NetBox's `manage.py test` runner — they depend on NetBox's database, core models, and test framework.

```bash
docker compose exec netbox python /opt/netbox/netbox/manage.py test netbox_loadbalancer --verbosity=2
```

All tests must pass before submitting a pull request.

## Code Style

- Follow existing patterns in the codebase. Look at how current models, serializers, views, and filtersets are structured and match that style.
- Keep it simple. Avoid over-engineering or adding abstractions for hypothetical future use.
- No linter or formatter is enforced, but be consistent with the surrounding code.

## Submitting Changes

1. Create a feature branch from `main`:

```bash
git checkout -b my-feature main
```

2. Make your changes with clear, descriptive commits.
3. Run the full test suite and make sure it passes.
4. Push your branch and open a pull request against `main`.
5. Describe what the PR does and why in the PR description.

## Reporting Bugs

Use [GitHub Issues](https://github.com/djohnnes/netbox-loadbalancer/issues) to report bugs. Please include:

- NetBox version and plugin version
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or tracebacks if applicable

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
