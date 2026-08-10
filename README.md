# Locust Performance Testing Template

[![Python](https://img.shields.io/badge/Python-3.14.7-blue.svg)](https://www.python.org/)
[![Locust](https://img.shields.io/badge/Locust-2.46.3-orange.svg)](https://locust.io/)
[![CI](https://github.com/lucas-porto1/locust-performance-py/actions/workflows/ci.yml/badge.svg)](https://github.com/lucas-porto1/locust-performance-py/actions/workflows/ci.yml)

A lightweight reference project for API performance testing with Locust and Python. It uses [JSONPlaceholder](https://jsonplaceholder.typicode.com/) to demonstrate service organization, reusable workload profiles, and common HTTP operations without unnecessary framework layers.

## What This Template Demonstrates

- Reusable smoke, baseline, load, peak, concurrency, stress, spike, and soak profiles.
- Weighted user behavior with concurrent virtual users.
- Resource-oriented clients for a service that grows over time.
- Collection, item, nested-resource, and write operations.
- Response validation with `catch_response`.
- Stable metric names for endpoints containing dynamic IDs.
- Automated linting and a short CI smoke test.

## Project Structure

```text
.
|-- .github/
|   |-- workflows/ci.yml
|   `-- dependabot.yml
|-- .env.example
|-- clients/
|   `-- json_placeholder/
|       |-- comments_client.py
|       |-- posts_client.py
|       `-- users_client.py
|-- load_shapes/
|   |-- spike_shape.py
|   `-- stress_shape.py
|-- profiles/
|   |-- concurrency.conf
|   |-- load.conf
|   |-- peak.conf
|   |-- performance.conf
|   |-- smoke.conf
|   |-- soak.conf
|   |-- spike.conf
|   `-- stress.conf
|-- test_data/
|   `-- json_placeholder/
|       `-- payloads.py
|-- locustfiles/
|   `-- json_placeholder.py
|-- pyproject.toml
`-- requirements.txt
```

- `clients/<service>/`: HTTP requests grouped by service and resource.
- `locustfiles/`: executable Locust behavior, task weights, wait time, and service host.
- `test_data/<service>/`: payload factories and dynamic service data.
- `profiles/`: reusable workload settings that are not tied to one service.
- `load_shapes/`: custom workload curves for stress and spike tests.
- `.env.example`: documented environment variables with safe example values.

## JSONPlaceholder Example

JSONPlaceholder exposes six resources: posts, comments, albums, photos, todos, and users. This template intentionally uses only three to demonstrate how a service can be divided without adding every available endpoint.

| Client | Example routes |
| --- | --- |
| `posts_client.py` | `/posts`, `/posts/{id}`, `/posts/{id}/comments` |
| `comments_client.py` | `/comments`, `/comments/{id}` |
| `users_client.py` | `/users`, `/users/{id}`, `/users/{id}/todos` |

The provider also supports routes such as `/albums/{id}/photos`, `/users/{id}/albums`, and `/users/{id}/posts`. See the [official guide](https://jsonplaceholder.typicode.com/guide/).

Use one client file per meaningful resource or domain inside a service. Do not create one file for every individual endpoint.

## Performance Test Types

| Type | Purpose |
| --- | --- |
| Smoke | Confirms quickly that the script, dependencies, and target are available. |
| Performance baseline | Establishes initial response-time and throughput measurements with a small workload. |
| Load | Validates behavior under the expected regular workload. |
| Peak | Validates the highest expected and planned workload. |
| Concurrency | Exercises different routes and operations at the same time with multiple users. |
| Stress | Continuously increases workload beyond the expected peak to identify limits. |
| Spike | Applies a sudden traffic increase and observes stability and recovery. |
| Soak | Maintains workload for an extended period to find degradation or resource leaks. |

Performance testing is the broader category. The profiles above represent different workload strategies within it.

## User Behavior and Concurrency

Read operations have a higher weight than write operations. Each virtual user independently selects a task and waits between 2 and 10 seconds before selecting the next one.

| Tasks | Weight |
| --- | ---: |
| List posts and comments | 3 |
| Get one post, its comments, or list users | 2 |
| Individual user, nested todo, and write operations | 1 |

With multiple users, different clients, methods, and routes run concurrently. One user can request `/posts` while others create a comment, request a user, or retrieve `/users/{id}/todos`.

## Getting Started

### Prerequisites

- Python 3.14.7

### Installation

```bash
git clone https://github.com/lucas-porto1/locust-performance-py.git
cd locust-performance-py
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS or Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment file:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS or Linux
cp .env.example .env
```

## Running the Profiles

Static profiles reuse the same Locust user file:

| Profile | Example workload | Command |
| --- | --- | --- |
| Smoke | 1 user for 10 seconds | `locust -f locustfiles/json_placeholder.py --config profiles/smoke.conf` |
| Performance baseline | 2 users for 1 minute | `locust -f locustfiles/json_placeholder.py --config profiles/performance.conf` |
| Load | 10 users for 5 minutes | `locust -f locustfiles/json_placeholder.py --config profiles/load.conf` |
| Peak | 20 users for 3 minutes | `locust -f locustfiles/json_placeholder.py --config profiles/peak.conf` |
| Concurrency | 20 users started rapidly for 2 minutes | `locust -f locustfiles/json_placeholder.py --config profiles/concurrency.conf` |
| Soak | 5 users for 30 minutes | `locust -f locustfiles/json_placeholder.py --config profiles/soak.conf` |

Stress and spike add their custom shapes:

```bash
locust -f locustfiles/json_placeholder.py,load_shapes/stress_shape.py --config profiles/stress.conf
locust -f locustfiles/json_placeholder.py,load_shapes/spike_shape.py --config profiles/spike.conf
```

The stress shape increases from 10 to 50 users over five cumulative stages. The spike shape starts with 5 users, quickly starts 40 users, holds the spike, and returns to 5 users.

The example values are intentionally small and do not represent production capacity. A real soak test commonly runs for several hours.

### Target Environment

The project loads `.env` automatically with `python-dotenv`. Change the target locally in `.env`:

```env
JSON_PLACEHOLDER_API_URL=https://your-environment.example.com
```

The Locust user requires that value, preventing performance tests from accidentally running against an unintended environment:

```python
host = os.environ["JSON_PLACEHOLDER_API_URL"]
```

An operating-system environment variable can still override `.env` because `load_dotenv()` does not replace existing variables:

```powershell
$env:JSON_PLACEHOLDER_API_URL="https://your-environment.example.com"
locust -f locustfiles/json_placeholder.py --config profiles/load.conf
```

The variable is required. Copy `.env.example` to `.env` before running the project locally. Do not commit `.env`; it is already ignored by Git and only `.env.example` should be versioned.

## Reusing Profiles Across Services

Profiles describe workload, not APIs. A project with many services should reuse the same files:

```bash
locust -f locustfiles/catalog.py --config profiles/load.conf
locust -f locustfiles/payments.py --config profiles/load.conf
```

To exercise services together, provide multiple user files:

```bash
locust -f locustfiles/catalog.py,locustfiles/payments.py --config profiles/concurrency.conf
```

Create a service-specific profile only when that service has a genuinely different workload. This avoids duplicating every profile for every API.

Generic profiles reuse report filenames. Override the report name when running multiple services to avoid replacing a previous result:

```bash
locust -f locustfiles/catalog.py --config profiles/load.conf --html catalog-load-report.html
```

## Code Quality

```bash
pip install -r requirements.txt
ruff check .
ruff format --check .
```

Apply safe automatic fixes:

```bash
ruff check . --fix
ruff format .
```

## Adapting the Template

1. Add a directory under `clients/` for the service.
2. Split a large service client by resource or domain when it improves navigation.
3. Add service data under `test_data/<service>/`.
4. Add a service file under `locustfiles/` with its own host, tasks, and weights.
5. Reuse a profile and add an override only when the workload is different.
6. Define performance thresholds from the real system SLA before using the test as a release gate.

## Continuous Integration

GitHub Actions passes the public `JSON_PLACEHOLDER_API_URL` directly through the workflow `env` section and does not depend on a local `.env` file. For real projects, use GitHub Variables for non-sensitive URLs and GitHub Secrets for tokens or credentials.

The workflow runs only the generic smoke profile with the included JSONPlaceholder user. Full load, peak, stress, spike, concurrency, and soak tests remain intentional executions to avoid accidental load on shared environments.

## Responsible Use

Only run performance tests against systems you own or are explicitly authorized to test. Start with a small workload and increase it gradually while monitoring the target environment.
