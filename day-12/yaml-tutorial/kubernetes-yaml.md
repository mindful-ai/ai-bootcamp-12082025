# 📘 Kubernetes YAML Tutorial

Kubernetes uses YAML (YAML Ain't Markup Language) files to define
resources declaratively. Instead of giving commands each time, you
describe the desired state in YAML, and Kubernetes ensures your cluster
matches that state.

## 1. Basic Structure of Kubernetes YAML

Every Kubernetes YAML follows this format:

``` yaml
apiVersion: <API version>   # Version of the Kubernetes API to use
kind: <Resource kind>       # Type of Kubernetes object (Pod, Deployment, Service, etc.)
metadata:
  name: <name>              # Name of the resource
  labels:                   # (Optional) key-value labels
    app: myapp
spec:                       # Specification of the desired state
  ...
```

## 2. Key Kubernetes Resources

### (a) Pod

Smallest deployable unit in Kubernetes.

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: myapp
spec:
  containers:
    - name: my-container
      image: nginx:latest
      ports:
        - containerPort: 80
```

### (b) Deployment

Manages replica sets and ensures desired pod count.

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: my-container
          image: nginx:latest
          ports:
            - containerPort: 80
```

### (c) Service

Exposes pods internally (ClusterIP), externally (NodePort), or via
LoadBalancer.

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

### (d) ConfigMap

Stores configuration data.

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  APP_MODE: "production"
  APP_PORT: "8080"
```

### (e) Secret

Stores sensitive data (base64 encoded).

``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=   # base64 encoded 'admin'
  password: cGFzc3dvcmQ=  # base64 encoded 'password'
```

### (f) Ingress

Manages external access with routing rules.

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

## 3. Kubernetes YAML Cheat Sheet

  ------------------------------------------------------------------------------
  Attribute                  Description                 Example
  -------------------------- --------------------------- -----------------------
  apiVersion                 Kubernetes API version for  v1, apps/v1, batch/v1
                             the resource                

  kind                       Resource type               Pod, Deployment,
                                                         Service

  metadata.name              Resource name               my-app

  metadata.labels            Labels to identify resource app: myapp

  spec.replicas              Number of pod replicas (for 3
                             Deployment)                 

  spec.selector              Label selector to match     matchLabels: { app:
                             pods                        myapp }

  spec.template              Pod template inside         ---
                             Deployment                  

  spec.containers            List of containers          \- name: my-container

  spec.containers.image      Container image             nginx:latest

  spec.ports.containerPort   Port exposed by container   80

  spec.service.type          Service type                ClusterIP, NodePort,
                                                         LoadBalancer

  spec.volumes               Mount volumes in Pods       configMap, secret,
                                                         persistentVolumeClaim
  ------------------------------------------------------------------------------

## 4. A Ready-to-Use Kubernetes Template

Here's a reusable `k8s-app.yaml` file:

``` yaml
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp-container
          image: nginx:latest
          ports:
            - containerPort: 80
          envFrom:
            - configMapRef:
                name: my-config
            - secretRef:
                name: my-secret

---
# Service
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer

---
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  APP_MODE: "production"
  APP_PORT: "8080"

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
```

You can apply this with:

``` bash
kubectl apply -f k8s-app.yaml
```

⚡ With this, you have: - ✅ A Deployment (3 replicas of Nginx)\
- ✅ A Service (LoadBalancer)\
- ✅ A ConfigMap and Secret injected as environment variables
