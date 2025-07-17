
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
  APP_TITLE: "Kubernetes Note Taking App"
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
  name: note-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: note
  template:
    metadata:
      labels:
        app: note
    spec:
      serviceAccountName: demo-sa
      containers:
        - name: note-container
          image: your-dockerhub-username/k8s-note-app:latest
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: app-config
          volumeMounts:
            - mountPath: "/data"
              name: note-storage
      volumes:
        - name: note-storage
          persistentVolumeClaim:
            claimName: demo-pvc

```
### `deployment/app-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-app-service
spec:
  type: NodePort
  selector:
    app: demo
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30007  # Choose a port between 30000–32767
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
from flask import Flask, request, redirect
import os

app = Flask(__name__)
DATA_PATH = "/data/notes.txt"
APP_TITLE = os.getenv("APP_TITLE", "K8s Note App")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note", "")
        with open(DATA_PATH, "a") as f:
            f.write(note + "\n")
        return redirect("/")

    notes = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            notes = f.readlines()
    return f"""
        <h1>{APP_TITLE}</h1>
        <form method="post">
            <textarea name="note" rows="4" cols="50" placeholder="Write your note here..."></textarea><br>
            <input type="submit" value="Add Note">
        </form>
        <h2>Saved Notes:</h2>
        <ul>{"".join(f"<li>{note.strip()}</li>" for note in notes)}</ul>
    """

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    app.run(host="0.0.0.0", port=5000)

```

---

### `app/Dockerfile`

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY note_app.py .
RUN pip install flask
CMD ["python", "note_app.py"]
```

---

## 🧪 Deployment Steps

### 1. Build and Push Docker Image

```bash
docker build -t your-dockerhub-username/k8s-note-app:latest .
docker push your-dockerhub-username/k8s-note-app:latest

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
kubectl apply -f deployment/app-service.yaml

```

---
## Forward the port to `8080` 
```bash
kubectl port-forward --address 0.0.0.0 service/note-app-service 8080:80
```
And open in browser:
```bash
http://<EC2_PUBLIC_IP>:8080
```
---
## ✅ Testing the App


1. Open the app in a browser

2. Submit a new note in the textarea form

3. See saved notes appear below

---
   
## 📦 Cleanup
```bash
kubectl delete -f deployment/
kubectl delete -f persistent-volume/
kubectl delete -f configmap/
kubectl delete -f rbac/
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
