# Nemoclaw CLI Command Reference

## 1. Introduction

Welcome to the comprehensive Command Line Interface (CLI) reference for **Nemoclaw**. Nemoclaw is an advanced, enterprise-grade orchestration and management tool designed for distributed containerized environments, microservices architectures, and cloud-native deployments. This document serves as the definitive guide for system administrators, DevOps engineers, and developers who interact with the Nemoclaw ecosystem via the command line.

The Nemoclaw CLI provides a powerful, scriptable, and human-readable interface to interact with the Nemoclaw control plane. It allows users to deploy applications, manage cluster resources, inspect system health, configure security policies, and troubleshoot complex distributed systems. This guide covers every command, flag, argument, and provides detailed examples of usage to ensure you can leverage the full potential of Nemoclaw.

## 2. Installation and Configuration

Before diving into the commands, ensure that the Nemoclaw CLI is properly installed and configured on your system.

### 2.1. Installation

The Nemoclaw CLI can be installed via various package managers depending on your operating system.

**For Linux (Debian/Ubuntu):**
```bash
curl -fsSL https://apt.nemoclaw.io/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://apt.nemoclaw.io/ stable main"
sudo apt-get update
sudo apt-get install nemoclaw-cli
```

**For macOS (Homebrew):**
```bash
brew tap nemoclaw/tap
brew install nemoclaw-cli
```

**For Windows (Chocolatey):**
```powershell
choco install nemoclaw-cli
```

### 2.2. Configuration

After installation, the CLI must be configured to communicate with your Nemoclaw control plane. The configuration is typically stored in `~/.nemoclaw/config.yaml`.

You can initialize the configuration using the `init` command:
```bash
nemoclaw init --server https://api.nemoclaw.example.com --token YOUR_ACCESS_TOKEN
```

Alternatively, you can use environment variables:
- `NEMOCLAW_SERVER`: The URL of the Nemoclaw API server.
- `NEMOCLAW_TOKEN`: The authentication token.
- `NEMOCLAW_NAMESPACE`: The default namespace to use for commands.

## 3. Global Flags

The following global flags can be used with almost any Nemoclaw CLI command to modify its behavior, output format, or authentication context.

- `--server, -s`: Specify the Nemoclaw API server URL. Overrides the configuration file and environment variables.
- `--token, -t`: Specify the authentication token.
- `--namespace, -n`: Specify the namespace for the operation. Defaults to `default`.
- `--output, -o`: Specify the output format. Supported formats: `text`, `json`, `yaml`, `table`. Default is `table`.
- `--verbose, -v`: Enable verbose logging for debugging purposes.
- `--debug`: Enable extremely detailed debug logging, including raw HTTP requests and responses.
- `--timeout`: Specify the timeout for the command execution (e.g., `30s`, `1m`). Default is `60s`.
- `--dry-run`: Simulate the command execution without making any actual changes to the system.

## 4. Core Commands

This section covers the fundamental commands used for interacting with Nemoclaw resources.

### 4.1. `nemoclaw get`

The `get` command is used to retrieve information about one or more resources in the Nemoclaw cluster.

**Syntax:**
```bash
nemoclaw get <resource_type> [resource_name] [flags]
```

**Supported Resource Types:**
- `pods` (or `po`)
- `services` (or `svc`)
- `deployments` (or `deploy`)
- `nodes` (or `no`)
- `configs` (or `cfg`)

**Flags:**
- `--watch, -w`: Continuously watch for changes to the requested resources.
- `--labels, -l`: Filter resources based on label selectors (e.g., `app=frontend,env=prod`).
- `--all-namespaces, -A`: Retrieve resources from all namespaces.

**Examples:**

1. Get all pods in the default namespace:
```bash
nemoclaw get pods
```

2. Get a specific deployment in JSON format:
```bash
nemoclaw get deployment web-backend -o json
```

3. Watch for changes to services with a specific label:
```bash
nemoclaw get svc -l tier=backend --watch
```

### 4.2. `nemoclaw describe`

The `describe` command provides a detailed, human-readable overview of a specific resource, including its current state, events, and configuration.

**Syntax:**
```bash
nemoclaw describe <resource_type> <resource_name> [flags]
```

**Examples:**

1. Describe a specific node to check its resource utilization and conditions:
```bash
nemoclaw describe node worker-01
```

2. Describe a pod to troubleshoot startup issues:
```bash
nemoclaw describe pod api-gateway-7f8b9c-xyz
```

### 4.3. `nemoclaw create`

The `create` command is used to instantiate new resources in the Nemoclaw cluster, typically from a configuration file.

**Syntax:**
```bash
nemoclaw create -f <filename_or_url> [flags]
```

**Flags:**
- `--filename, -f`: (Required) The path to the YAML or JSON configuration file, or a URL pointing to one.
- `--recursive, -R`: Process the directory recursively if a directory is provided instead of a file.
- `--validate`: Validate the configuration file against the Nemoclaw schema before attempting creation. Default is `true`.

**Examples:**

1. Create resources from a local YAML file:
```bash
nemoclaw create -f ./manifests/database.yaml
```

2. Create resources from a directory recursively:
```bash
nemoclaw create -f ./manifests/prod/ -R
```

### 4.4. `nemoclaw apply`

The `apply` command is the declarative way to manage resources. It creates resources if they do not exist or updates them if they do, based on the provided configuration file.

**Syntax:**
```bash
nemoclaw apply -f <filename_or_url> [flags]
```

**Flags:**
- `--filename, -f`: (Required) The path to the configuration file.
- `--prune`: Automatically delete resources that are not present in the configuration file but exist in the cluster (requires label selectors).
- `--force`: Force the update by deleting and recreating the resource if a standard update fails.

**Examples:**

1. Apply changes to a deployment:
```bash
nemoclaw apply -f ./manifests/frontend-deployment.yaml
```

2. Apply a directory of manifests and prune obsolete resources:
```bash
nemoclaw apply -f ./manifests/app/ --prune -l app=my-app
```

### 4.5. `nemoclaw delete`

The `delete` command removes resources from the Nemoclaw cluster.

**Syntax:**
```bash
nemoclaw delete <resource_type> <resource_name> [flags]
nemoclaw delete -f <filename> [flags]
```

**Flags:**
- `--force`: Force immediate deletion, bypassing graceful termination periods.
- `--cascade`: Delete resources that depend on the target resource (e.g., deleting a deployment deletes its pods). Default is `true`.
- `--all`: Delete all resources of the specified type in the namespace.

**Examples:**

1. Delete a specific service:
```bash
nemoclaw delete svc legacy-api
```

2. Delete all pods in the current namespace (use with caution):
```bash
nemoclaw delete pods --all
```

3. Delete resources defined in a file:
```bash
nemoclaw delete -f ./manifests/obsolete-job.yaml
```

## 5. Application Management Commands

These commands are specifically tailored for managing the lifecycle of applications deployed via Nemoclaw.

### 5.1. `nemoclaw scale`

The `scale` command adjusts the number of replicas for a deployment, replica set, or stateful set.

**Syntax:**
```bash
nemoclaw scale <resource_type> <resource_name> --replicas=<count> [flags]
```

**Flags:**
- `--replicas`: (Required) The desired number of replicas.
- `--current-replicas`: Precondition: only scale if the current number of replicas matches this value.

**Examples:**

1. Scale a deployment to 5 replicas:
```bash
nemoclaw scale deployment web-frontend --replicas=5
```

2. Scale a stateful set down to 1 replica:
```bash
nemoclaw scale statefulset database-cluster --replicas=1
```

### 5.2. `nemoclaw rollout`

The `rollout` command manages the deployment of new versions of an application, allowing for status checks, pausing, resuming, and undoing rollouts.

**Syntax:**
```bash
nemoclaw rollout <subcommand> <resource_type> <resource_name> [flags]
```

**Subcommands:**
- `status`: Check the status of an ongoing rollout.
- `pause`: Pause an ongoing rollout.
- `resume`: Resume a paused rollout.
- `undo`: Roll back to a previous version.
- `history`: View the rollout history and revisions.

**Examples:**

1. Check the status of a deployment rollout:
```bash
nemoclaw rollout status deployment/payment-service
```

2. Undo the last deployment (rollback):
```bash
nemoclaw rollout undo deployment/payment-service
```

3. Roll back to a specific revision:
```bash
nemoclaw rollout undo deployment/payment-service --to-revision=3
```

### 5.3. `nemoclaw expose`

The `expose` command creates a network service to expose a deployment, pod, or replica set to internal or external traffic.

**Syntax:**
```bash
nemoclaw expose <resource_type> <resource_name> --port=<port> [flags]
```

**Flags:**
- `--port`: (Required) The port that the service should serve on.
- `--target-port`: The port on the containers that the service should direct traffic to. Defaults to the `--port` value.
- `--type`: The type of service to create (`ClusterIP`, `NodePort`, `LoadBalancer`). Default is `ClusterIP`.
- `--name`: The name of the newly created service. Defaults to the name of the exposed resource.

**Examples:**

1. Expose a deployment internally on port 8080:
```bash
nemoclaw expose deployment internal-api --port=8080 --target-port=3000
```

2. Expose a deployment externally using a LoadBalancer:
```bash
nemoclaw expose deployment public-web --port=80 --type=LoadBalancer
```

## 6. Troubleshooting and Debugging Commands

When things go wrong, these commands are essential for diagnosing issues within the Nemoclaw environment.

### 6.1. `nemoclaw logs`

The `logs` command retrieves the standard output and standard error logs from a specific pod or container.

**Syntax:**
```bash
nemoclaw logs <pod_name> [flags]
```

**Flags:**
- `--container, -c`: Specify the container name if the pod has multiple containers.
- `--follow, -f`: Stream the logs continuously.
- `--tail`: Number of lines to show from the end of the logs. Default is all.
- `--previous, -p`: Print the logs for the previous instance of the container (useful if the container crashed and restarted).
- `--since`: Only return logs newer than a relative duration (e.g., `5m`, `1h`).

**Examples:**

1. Fetch the last 100 lines of logs from a pod:
```bash
nemoclaw logs auth-service-pod-xyz --tail=100
```

2. Stream logs from a specific container within a pod:
```bash
nemoclaw logs multi-container-pod -c sidecar-proxy -f
```

3. Get logs from a crashed container:
```bash
nemoclaw logs crashing-pod --previous
```

### 6.2. `nemoclaw exec`

The `exec` command executes a command directly inside a running container. This is invaluable for interactive debugging.

**Syntax:**
```bash
nemoclaw exec <pod_name> [flags] -- <command> [args...]
```

**Flags:**
- `--stdin, -i`: Pass stdin to the container.
- `--tty, -t`: Allocate a TTY for the container (required for interactive shells).
- `--container, -c`: Specify the container name if the pod has multiple containers.

**Examples:**

1. Open an interactive bash shell inside a pod:
```bash
nemoclaw exec -it my-database-pod -- /bin/bash
```

2. Run a single command to check a configuration file:
```bash
nemoclaw exec web-server-pod -- cat /etc/nginx/nginx.conf
```

3. Execute a database dump command inside a specific container:
```bash
nemoclaw exec db-pod -c postgres -- pg_dump -U admin mydb > backup.sql
```

### 6.3. `nemoclaw port-forward`

The `port-forward` command forwards one or more local ports to a pod, allowing you to access internal services directly from your local machine without exposing them via a Nemoclaw Service.

**Syntax:**
```bash
nemoclaw port-forward <resource_type>/<resource_name> <local_port>:<remote_port> [flags]
```

**Examples:**

1. Forward local port 8080 to port 80 on a pod:
```bash
nemoclaw port-forward pod/internal-dashboard 8080:80
```

2. Forward local port 5432 to a database service:
```bash
nemoclaw port-forward svc/postgres-db 5432:5432
```

## 7. Cluster Administration Commands

These commands are typically used by cluster administrators to manage nodes, security, and overall cluster health.

### 7.1. `nemoclaw cordon` and `nemoclaw uncordon`

The `cordon` command marks a node as unschedulable, preventing new pods from being placed on it. `uncordon` reverses this action.

**Syntax:**
```bash
nemoclaw cordon <node_name>
nemoclaw uncordon <node_name>
```

**Examples:**

1. Cordon a node before performing maintenance:
```bash
nemoclaw cordon worker-node-03
```

### 7.2. `nemoclaw drain`

The `drain` command safely evicts all pods from a node, ensuring that workloads are rescheduled onto other available nodes before the node is taken offline for maintenance or decommissioning.

**Syntax:**
```bash
nemoclaw drain <node_name> [flags]
```

**Flags:**
- `--ignore-daemonsets`: Ignore DaemonSet-managed pods (which cannot be evicted).
- `--delete-local-data`: Continue even if there are pods using emptyDir (local data that will be lost).
- `--force`: Force eviction of pods not managed by a ReplicationController, ReplicaSet, Job, DaemonSet, or StatefulSet.
- `--grace-period`: Period of time in seconds given to each pod to terminate gracefully.

**Examples:**

1. Drain a node safely, ignoring daemonsets:
```bash
nemoclaw drain worker-node-03 --ignore-daemonsets --delete-local-data
```

### 7.3. `nemoclaw top`

The `top` command displays resource (CPU and Memory) usage for nodes or pods, helping administrators identify bottlenecks and optimize resource allocation.

**Syntax:**
```bash
nemoclaw top <resource_type> [flags]
```

**Supported Resource Types:**
- `nodes`
- `pods`

**Flags:**
- `--sort-by`: Sort the output by `cpu` or `memory`.
- `--namespace, -n`: Show metrics for pods in a specific namespace.

**Examples:**

1. Show resource usage for all nodes:
```bash
nemoclaw top nodes
```

2. Show resource usage for pods in the `production` namespace, sorted by memory:
```bash
nemoclaw top pods -n production --sort-by=memory
```

### 7.4. `nemoclaw auth`

The `auth` command helps verify authorization and permissions within the cluster.

**Syntax:**
```bash
nemoclaw auth can-i <verb> <resource> [flags]
```

**Examples:**

1. Check if the current user can create deployments:
```bash
nemoclaw auth can-i create deployments
```

2. Check if a specific service account can delete secrets:
```bash
nemoclaw auth can-i delete secrets --as=system:serviceaccount:default:my-sa
```

## 8. Advanced Configuration and Plugins

Nemoclaw CLI supports advanced configuration and extensibility through plugins.

### 8.1. Context Management

Nemoclaw allows you to manage multiple cluster configurations (contexts) within a single configuration file.

- `nemoclaw config get-contexts`: List all available contexts.
- `nemoclaw config current-context`: Show the currently active context.
- `nemoclaw config use-context <context_name>`: Switch to a different context.
- `nemoclaw config set-context <name> --cluster=<cluster> --user=<user> --namespace=<ns>`: Create or modify a context.

### 8.2. Plugins

The Nemoclaw CLI can be extended using plugins. A plugin is simply an executable file whose name begins with `nemoclaw-`.

- `nemoclaw plugin list`: List all installed plugins.
- To execute a plugin named `nemoclaw-custom-tool`, you simply run `nemoclaw custom-tool`.

## 9. Best Practices

1. **Use Declarative Management:** Whenever possible, use `nemoclaw apply -f <directory>` rather than imperative commands like `nemoclaw create` or `nemoclaw expose`. This ensures your infrastructure is version-controlled and reproducible.
2. **Leverage Dry Runs:** Before applying complex changes, use the `--dry-run=client` or `--dry-run=server` flags to validate your configurations without affecting the cluster.
3. **Namespace Isolation:** Always specify namespaces (`-n`) or set a default namespace in your context to avoid accidentally modifying resources in the wrong environment (e.g., modifying `prod` instead of `dev`).
4. **Secure Access:** Never hardcode tokens in scripts. Use environment variables or secure secret management systems to inject credentials into your CI/CD pipelines.
5. **Monitor Resource Usage:** Regularly use `nemoclaw top` and `nemoclaw describe` to ensure your applications are requesting appropriate CPU and memory limits, preventing noisy neighbor issues.

## 10. Conclusion

The Nemoclaw CLI is a versatile and indispensable tool for managing modern distributed systems. By mastering the commands and flags detailed in this reference, you can efficiently deploy, monitor, and troubleshoot your applications, ensuring high availability and optimal performance across your infrastructure. For further assistance, you can always append the `--help` flag to any command to view inline documentation and additional examples.