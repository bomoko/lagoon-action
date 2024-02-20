# Lagoon CLI Action

This GitHub Action allows you to run lagoon-cli commands with SSH authentication. It supports two main actions: `deploy` and `upsert_variable`.

## Inputs

### `action` (required)

One of the following actions: `deploy` (default), `upsert_variable`.

### `ssh_private_key` (required)

SSH private key for Lagoon authentication.

### `lagoon_graphql_endpoint` (optional)

Lagoon GraphQL endpoint. Default is `https://api.lagoon.amazeeio.cloud/graphql`.

### `lagoon_ssh_hostname` (optional)

Lagoon SSH hostname. Default is `ssh.lagoon.amazeeio.cloud`.

### `lagoon_port` (optional)

Lagoon SSH port. Default is `32222`.

### `lagoon_project` (optional)

Lagoon project name.

### `lagoon_environment` (optional)

Lagoon environment name.

### `lagoon_wait_for_deployment` (optional)

Whether to wait for deployment completion (`true` or `false`). Default is `true`.

### `variable_scope` (required for `upsert_variable` action)

Variable scope for the `upsert_variable` action. Can be one of "global", "build", and "runtime".

### `variable_name` (required for `upsert_variable` action)

Variable name for the `upsert_variable` action.

### `variable_value` (required for `upsert_variable` action)

Variable value for the `upsert_variable` action.

## Example Usage

```yaml
name: Lagoon Deployment

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Lagoon Deployment
      uses: uselagoon/lagoon-cli-action@v1
      with:
        action: 'deploy'
        ssh_private_key: ${{ secrets.LAGOON_SSH_PRIVATE_KEY }}
        lagoon_project: 'your-project-name'
        lagoon_environment: 'your-environment-name'
        lagoon_wait_for_deployment: 'true'

  upsert-variable:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v2

    - name: Lagoon Upsert Variable
      uses: uselagoon/lagoon-cli-action@v1
      with:
        action: 'upsert_variable'
        ssh_private_key: ${{ secrets.LAGOON_SSH_PRIVATE_KEY }}
        lagoon_project: 'your-project-name'
        lagoon_environment: 'your-environment-name'
        variable_scope: 'runtime'
        variable_name: 'your-variable-name'
        variable_value: 'your-variable-value'

