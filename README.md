
# 📘 Kubernetes Basics Project

A simple Kubernetes project to understand key concepts like Volumes, Persistent Volumes, ConfigMaps, RBAC, and how to use them in a real-world deployment.

---

## 🗂️ Directory Structure

```
k8s-basics-project/
│
├── configmap/
│   └── app-configmap.yaml
│
├── deployment/
│   └── app-deployment.yaml
│
├── persistent-volume/
│   ├── pv.yaml
│   └── pvc.yaml
│
├── rbac/
│   ├── role.yaml
│   ├── rolebinding.yaml
│   └── serviceaccount.yaml
│
├── app/
│   ├── app.py
│   └── Dockerfile
│
└── README.md
```

---

## 📁 1. ConfigMap

**File:** `configmap/app-configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  WELCOME_MESSAGE: "Welcome to Kubernetes Learning Project!"
```

---

## 📁 2. Persistent Volume & Claim

### `persistent-volume/pv.yaml`

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: demo-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

### `persistent-volume/pvc.yaml`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

---

## 📁 3. Deployment

**File:** `deployment/app-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo
  template:
    metadata:
      labels:
        app: demo
    spec:
      serviceAccountName: demo-sa
      containers:
        - name: app-container
          image: your-dockerhub-username/k8s-demo-app:latest
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: app-config
          volumeMounts:
            - mountPath: "/data"
              name: demo-storage
      volumes:
        - name: demo-storage
          persistentVolumeClaim:
            claimName: demo-pvc
```

---

## 📁 4. RBAC Setup

### `rbac/serviceaccount.yaml`

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-sa
```

### `rbac/role.yaml`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: configmap-reader
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
```

### `rbac/rolebinding.yaml`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-configmap-binding
  namespace: default
subjects:
- kind: ServiceAccount
  name: demo-sa
  namespace: default
roleRef:
  kind: Role
  name: configmap-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## 📁 5. Sample Application

### `app/app.py`

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    message = os.getenv("WELCOME_MESSAGE", "Hello World!")
    return f"<h1>{message}</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

### `app/Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
CMD ["python", "app.py"]
```

---

## 🧪 Deployment Steps

### 1. Build and Push Docker Image

```bash
docker build -t your-dockerhub-username/k8s-demo-app:latest ./app
docker push your-dockerhub-username/k8s-demo-app:latest
```

### 2. Apply Kubernetes Resources

```bash
kubectl apply -f persistent-volume/pv.yaml
kubectl apply -f persistent-volume/pvc.yaml
kubectl apply -f configmap/app-configmap.yaml
kubectl apply -f rbac/serviceaccount.yaml
kubectl apply -f rbac/role.yaml
kubectl apply -f rbac/rolebinding.yaml
kubectl apply -f deployment/app-deployment.yaml
```

---

## ✅ Concepts Demonstrated

| Concept | Description |
|--------|-------------|
| Volumes | Mounting a volume inside the container |
| Persistent Volumes | Using PV and PVC for storage |
| ConfigMaps | Managing environment variables |
| ConfigMap in Deployment | Injecting config into pods |
| RBAC | Restricting access using Role, RoleBinding, and ServiceAccount |
