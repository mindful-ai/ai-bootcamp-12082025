
# 🚀 Kubernetes Workshop: Multi-Container ML App

This workshop demonstrates deploying a **multi-container machine learning application** on **Kubernetes (K8s)** using Docker Desktop.

---

## 🎯 Objectives
- Deploy a **frontend (Streamlit)**, **backend (FastAPI)**, **model-serving API**, and **logger**.
- Expose the frontend for browser access.
- Demonstrate **scaling** (increase replicas of backend/model-serving).
- Learn **cleanup** best practices.

---

## 🛠️ Part 1: Setup Kubernetes on Docker Desktop
1. Enable **Kubernetes** in Docker Desktop (`Settings → Kubernetes → Enable`).
2. Verify installation:
   ```bash
   kubectl version --client
   kubectl cluster-info
   kubectl get nodes
   ```

---

## 📂 Part 2: Kubernetes Manifests

We’ll use a namespace `ml-demo` and apply manifests for each service.

### 1️⃣ Namespace
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ml-demo
```

Apply:
```bash
kubectl apply -f k8s/namespace.yaml
```

---

### 2️⃣ Backend Deployment + Service
```yaml
# k8s/backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: ml-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: backend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5002
        env:
        - name: MODEL_SERVING_URL
          value: "http://model-serving:5001/predict"
        - name: LOGGER_URL
          value: "http://logger:5003/log"
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: ml-demo
spec:
  selector:
    app: backend
  ports:
    - port: 5002
      targetPort: 5002
```

---

### 3️⃣ Model Serving Deployment + Service
```yaml
# k8s/model-serving.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-serving
  namespace: ml-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: model-serving
  template:
    metadata:
      labels:
        app: model-serving
    spec:
      containers:
      - name: model-serving
        image: model_serving:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5001
---
apiVersion: v1
kind: Service
metadata:
  name: model-serving
  namespace: ml-demo
spec:
  selector:
    app: model-serving
  ports:
    - port: 5001
      targetPort: 5001
```

---

### 4️⃣ Logger Deployment + Service
```yaml
# k8s/logger.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logger
  namespace: ml-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: logger
  template:
    metadata:
      labels:
        app: logger
    spec:
      containers:
      - name: logger
        image: logger:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5003
---
apiVersion: v1
kind: Service
metadata:
  name: logger
  namespace: ml-demo
spec:
  selector:
    app: logger
  ports:
    - port: 5003
      targetPort: 5003
```

---

### 5️⃣ Frontend Deployment + Service
```yaml
# k8s/frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ml-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: frontend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8501
        env:
        - name: BACKEND_URL
          value: "http://backend:5002/predict"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: ml-demo
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - port: 8501
      targetPort: 8501
      nodePort: 30080
```

👉 Access frontend at: **http://localhost:30080**

---

## 🚀 Part 3: Deploy to Kubernetes

Apply everything:
```bash
kubectl apply -f k8s/ --namespace=ml-demo
kubectl get all -n ml-demo
```

Check pods:
```bash
kubectl get pods -n ml-demo -o wide
```

---

## 📈 Part 4: Scaling Exercise

### Scale backend from 1 → 5 replicas:
```bash
kubectl scale deployment backend --replicas=5 -n ml-demo
kubectl get pods -n ml-demo -o wide
```

👉 Requests to `backend` are now load-balanced.

### Scale model-serving:
```bash
kubectl scale deployment model-serving --replicas=3 -n ml-demo
kubectl get pods -n ml-demo
```

---

## 🧹 Part 5: Cleanup

### Delete namespace (recommended):
```bash
kubectl delete namespace ml-demo
```

### OR delete specific YAML resources:
```bash
kubectl delete -f k8s/ -n ml-demo
```

### OR nuke everything in namespace:
```bash
kubectl delete all --all -n ml-demo
```

---

✅ **Key Learnings:**
- Moved from **Docker Compose → Kubernetes**.
- Understood **Deployments, Services, scaling**.
- Learned **cleanup strategies**.
