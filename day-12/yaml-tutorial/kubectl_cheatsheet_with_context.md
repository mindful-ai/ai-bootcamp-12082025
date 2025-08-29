# 📘 kubectl Cheat Sheet with Context Management (EKS + Local)

`kubectl` is the command-line tool to interact with Kubernetes
clusters.\
This cheat sheet covers **basic commands, resource management, context
switching, and AWS EKS integration**.

------------------------------------------------------------------------

## 🔹 1. Cluster & Context Management

``` bash
# View cluster info
kubectl cluster-info

# View all contexts (multiple clusters/configs)
kubectl config get-contexts

# View current context
kubectl config current-context

# Switch to another context
kubectl config use-context <context-name>

# Rename a context
kubectl config rename-context old-name new-name

# Delete a context
kubectl config delete-context <context-name>

# Set default namespace for a context
kubectl config set-context --current --namespace=<namespace>
```

------------------------------------------------------------------------

## 🔹 2. Namespaces

``` bash
# List namespaces
kubectl get namespaces

# Create a namespace
kubectl create namespace my-namespace

# Delete a namespace
kubectl delete namespace my-namespace
```

------------------------------------------------------------------------

## 🔹 3. Pods

``` bash
# List pods in default namespace
kubectl get pods

# List pods in all namespaces
kubectl get pods -A

# Get detailed info about a pod
kubectl describe pod <pod-name>

# Create a pod from YAML
kubectl apply -f pod.yaml

# Delete a pod
kubectl delete pod <pod-name>

# Execute a command inside a pod
kubectl exec -it <pod-name> -- /bin/sh

# Port-forward to access pod locally
kubectl port-forward pod/<pod-name> 8080:80
```

------------------------------------------------------------------------

## 🔹 4. Deployments

``` bash
# List deployments
kubectl get deployments

# Scale a deployment
kubectl scale deployment <deployment-name> --replicas=5

# Update image in deployment
kubectl set image deployment/<deployment-name> <container-name>=nginx:latest

# Restart a deployment
kubectl rollout restart deployment <deployment-name>

# Check rollout status
kubectl rollout status deployment <deployment-name>

# Rollback to previous version
kubectl rollout undo deployment <deployment-name>
```

------------------------------------------------------------------------

## 🔹 5. Services

``` bash
# List services
kubectl get svc

# Expose a deployment as a service
kubectl expose deployment <deployment-name> --type=NodePort --port=80 --target-port=8080

# Describe service
kubectl describe svc <service-name>
```

------------------------------------------------------------------------

## 🔹 6. ConfigMaps & Secrets

``` bash
# List configmaps
kubectl get configmaps

# Create configmap from file
kubectl create configmap my-config --from-file=config.txt

# List secrets
kubectl get secrets

# Create a secret
kubectl create secret generic my-secret --from-literal=username=admin --from-literal=password=pass123
```

------------------------------------------------------------------------

## 🔹 7. Logs & Debugging

``` bash
# View pod logs
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# Get logs for a specific container in pod
kubectl logs <pod-name> -c <container-name>

# Debug pod with ephemeral container
kubectl debug <pod-name> -it --image=busybox
```

------------------------------------------------------------------------

## 🔹 8. Apply & Delete Resources

``` bash
# Apply resources from YAML
kubectl apply -f deployment.yaml

# Delete resources from YAML
kubectl delete -f deployment.yaml

# Dry-run (test configuration without applying)
kubectl apply -f deployment.yaml --dry-run=client
```

------------------------------------------------------------------------

## 🔹 9. Shortcuts

``` bash
# Short forms
kubectl get po       # pods
kubectl get svc      # services
kubectl get deploy   # deployments
kubectl get ns       # namespaces
kubectl get cm       # configmaps
```

------------------------------------------------------------------------

# 📘 Kubernetes Contexts

Kubernetes uses **contexts** (in `~/.kube/config`) to switch between
clusters (local, AWS, GCP, etc.).

------------------------------------------------------------------------

## 🔹 Checking & Switching Contexts

``` bash
# List all contexts
kubectl config get-contexts

# Show current context
kubectl config current-context

# Switch to another context
kubectl config use-context <context-name>

# Example: Switch to AWS EKS context
kubectl config use-context arn:aws:eks:ap-south-1:123456789012:cluster/my-eks-cluster

# Switch back to Minikube (local)
kubectl config use-context minikube
```

------------------------------------------------------------------------

## 🔹 How an EKS Context is Created

### 1. Using AWS CLI (Most Common)

``` bash
aws eks --region <region> update-kubeconfig --name <cluster-name>
```

This: - Fetches cluster endpoint & CA from AWS\
- Updates `~/.kube/config` with a new **context**\
- Uses IAM credentials for authentication

✅ Example:

``` bash
aws eks --region ap-south-1 update-kubeconfig --name my-eks-cluster
```

### 2. Using eksctl (Easy Setup)

``` bash
eksctl create cluster --name my-eks-cluster --region ap-south-1
```

Automatically creates EKS + updates kubeconfig.

### 3. Manual Editing (Not Recommended)

Add a new cluster + context manually in `~/.kube/config`.

------------------------------------------------------------------------

## 🔹 Verifying EKS Context

``` bash
kubectl config current-context
kubectl get nodes
```

------------------------------------------------------------------------

# ✅ Summary

-   Use `kubectl config get-contexts` to list all clusters\
-   Use `kubectl config use-context <name>` to switch\
-   Use `aws eks update-kubeconfig` to add an EKS context\
-   Minikube/Docker Desktop usually adds its own context automatically

⚡ With this cheat sheet, you can manage **pods, deployments, services,
configs, logs, AND switch between local & AWS EKS clusters easily**.
