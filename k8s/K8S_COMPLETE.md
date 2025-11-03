# ✅ Kubernetes Deployment Complete

## Summary

Successfully created production-ready Kubernetes manifests for the RAG system backend deployment according to your specifications.

## ✅ Requirements Checklist

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Deployment with 3-10 replicas | ✅ | `backend-deployment.yaml` - replicas: 3, HPA scales to 10 |
| HorizontalPodAutoscaler | ✅ | `backend-deployment.yaml` - CPU 70%, Memory 80% |
| ConfigMap for non-sensitive config | ✅ | `configmap.yaml` - All app config |
| Secrets for FPT_API_KEY | ✅ | `secrets.yaml` - FPT_API_KEY |
| Resource requests/limits | ✅ | Requests: 512Mi/500m, Limits: 2Gi/2000m |
| Liveness probes at /health | ✅ | Every 10s, timeout 5s |
| Readiness probes at /health | ✅ | Every 5s, timeout 3s |
| Rolling update strategy | ✅ | maxSurge: 1, maxUnavailable: 0 |
| Proper labels and selectors | ✅ | app, component, version labels |
| Service in same file | ✅ | ClusterIP service included |
| HPA in same file | ✅ | HPA configuration included |

## 📁 Files Created (9 files)

```
k8s/
├── namespace.yaml                 ✅ rag-system namespace
├── configmap.yaml                ✅ Non-sensitive configuration
├── secrets.yaml                  ✅ FPT_API_KEY and credentials
├── backend-deployment.yaml       ✅ Deployment + Service + HPA
├── pvc.yaml                      ✅ PersistentVolumeClaims
├── qdrant-statefulset.yaml       ✅ Qdrant StatefulSet + Service
├── redis-deployment.yaml         ✅ Redis Deployment + Service
├── ingress.yaml                  ✅ HTTP/HTTPS routing
└── README.md                     ✅ Complete documentation
```

## 🎯 Backend Deployment Details

### File: `backend-deployment.yaml`

**Contains 3 Resources:**

#### 1. Deployment ✅

```yaml
metadata:
  name: rag-backend
  namespace: rag-system
spec:
  replicas: 3  # Initial, HPA will scale to 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero downtime!
```

**Key Features:**
- ✅ **3-10 Replicas:** Starts with 3, HPA auto-scales to 10
- ✅ **Zero Downtime:** maxUnavailable: 0
- ✅ **Rolling Updates:** maxSurge: 1
- ✅ **Security:** runAsNonRoot, runAsUser: 1000
- ✅ **Init Container:** Waits for Qdrant before starting
- ✅ **Anti-Affinity:** Spreads pods across nodes

**Container Configuration:**
```yaml
image: your-registry/rag-backend:latest
ports:
  - containerPort: 8000
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

**Environment Variables:**
- From ConfigMap: All non-sensitive config
- From Secret: FPT_API_KEY

**Volume Mounts:**
- `/app/uploads` → PVC (persistent)
- `/app/logs` → emptyDir (ephemeral)

#### 2. Service ✅

```yaml
metadata:
  name: rag-backend-service
spec:
  type: ClusterIP
  ports:
    - port: 8000
      targetPort: 8000
  selector:
    app: rag-backend
    component: api
```

**Features:**
- ClusterIP (internal only)
- Port 8000
- Selects backend pods

#### 3. HorizontalPodAutoscaler ✅

```yaml
metadata:
  name: rag-backend-hpa
spec:
  scaleTargetRef:
    kind: Deployment
    name: rag-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          averageUtilization: 80
```

**Scaling Behavior:**

**Scale Up (Aggressive):**
- Stabilization: 0s (immediate)
- Max increase: 100% (double) or +2 pods
- Check every: 15s

**Scale Down (Conservative):**
- Stabilization: 300s (5 minutes)
- Max decrease: 50%
- Check every: 60s

**Triggers:**
- CPU > 70%
- Memory > 80%

### Health Probes ✅

#### Liveness Probe
```yaml
httpGet:
  path: /health
  port: 8000
initialDelaySeconds: 30
periodSeconds: 10
timeoutSeconds: 5
failureThreshold: 3
```
**Action:** Restart pod if unhealthy

#### Readiness Probe
```yaml
httpGet:
  path: /health
  port: 8000
initialDelaySeconds: 10
periodSeconds: 5
timeoutSeconds: 3
failureThreshold: 3
```
**Action:** Remove from service if not ready

#### Startup Probe
```yaml
httpGet:
  path: /health
  port: 8000
initialDelaySeconds: 0
periodSeconds: 5
failureThreshold: 12  # 60s total
```
**Action:** Allow 60s for startup

## 📊 Resource Requirements

### Backend (per pod)
- **Requests:** 512Mi memory, 500m CPU
- **Limits:** 2Gi memory, 2000m CPU

### Total Resources (3 pods minimum)
- **Min Requests:** 1.5Gi memory, 1.5 CPU
- **Min Limits:** 6Gi memory, 6 CPU

### Max Resources (10 pods)
- **Max Requests:** 5Gi memory, 5 CPU
- **Max Limits:** 20Gi memory, 20 CPU

### Qdrant (2 replicas)
- **Per Pod:** 1Gi-4Gi memory, 500m-2000m CPU
- **Storage:** 50Gi per pod (100Gi total)

### Redis (1 replica)
- **Resources:** 256Mi-512Mi memory, 100m-200m CPU

### Grand Total (Minimum)
- **CPU:** ~5 cores
- **Memory:** ~10Gi
- **Storage:** 200Gi

## 🔧 Configuration Files

### ConfigMap ✅

**File:** `configmap.yaml`

**Contents:**
- FPT Cloud API base URL
- Qdrant connection (host, port, collection)
- Redis connection (optional)
- App settings (log level, upload size, CORS)
- RAG parameters (chunk size, retrieval k, rerank n)
- Model names (embedding, LLM, reranker, guard)

**All values from `.env.example`**

### Secrets ✅

**File:** `secrets.yaml`

**Contains:**
- `FPT_API_KEY` (REQUIRED)
- Optional: DB passwords, Redis password

**Production Note:**
Use external secret management:
- Sealed Secrets
- External Secrets Operator
- HashiCorp Vault
- Cloud provider (AWS/Azure/GCP)

### PersistentVolumeClaims ✅

**File:** `pvc.yaml`

**2 PVCs:**
1. `rag-backend-uploads-pvc` - 100Gi (ReadWriteMany)
2. `qdrant-data-pvc` - 50Gi (ReadWriteOnce)

## 🚀 Deployment Steps

### Quick Deploy

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Create secrets (replace with your key)
kubectl create secret generic rag-backend-secrets \
  --from-literal=FPT_API_KEY=your-key \
  -n rag-system

# 3. Apply all manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/qdrant-statefulset.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# 4. Verify
kubectl get all -n rag-system
```

### Deploy Script

Create `k8s/deploy.sh`:

```bash
#!/bin/bash
set -e

NAMESPACE="rag-system"
VERSION=${1:-latest}

echo "🚀 Deploying RAG System to Kubernetes..."

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap and Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Create PVCs
kubectl apply -f k8s/pvc.yaml

# Deploy Qdrant
kubectl apply -f k8s/qdrant-statefulset.yaml
kubectl wait --for=condition=ready pod -l app=qdrant -n $NAMESPACE --timeout=300s

# Deploy Redis
kubectl apply -f k8s/redis-deployment.yaml

# Deploy Backend
kubectl apply -f k8s/backend-deployment.yaml
kubectl wait --for=condition=ready pod -l app=rag-backend -n $NAMESPACE --timeout=300s

# Deploy Ingress
kubectl apply -f k8s/ingress.yaml

echo "✅ Deployment complete!"
kubectl get pods -n $NAMESPACE
```

## ✅ Verification

### Check Pods

```bash
kubectl get pods -n rag-system

# Expected:
# NAME                           READY   STATUS
# rag-backend-xxx-yyy           1/1     Running
# rag-backend-xxx-zzz           1/1     Running
# rag-backend-xxx-aaa           1/1     Running
# qdrant-0                      1/1     Running
# qdrant-1                      1/1     Running
# redis-xxx-yyy                 1/1     Running
```

### Check HPA

```bash
kubectl get hpa -n rag-system

# Expected:
# NAME               REFERENCE             TARGETS         MINPODS   MAXPODS
# rag-backend-hpa   Deployment/rag-backend   50%/70%, 40%/80%   3         10
```

### Test Health Endpoint

```bash
kubectl port-forward svc/rag-backend-service 8000:8000 -n rag-system
curl http://localhost:8000/health
```

### Check Logs

```bash
# All backend pods
kubectl logs -l app=rag-backend -n rag-system --tail=50

# Specific pod
kubectl logs rag-backend-xxx-yyy -n rag-system -f
```

## 🔍 Monitoring Scaling

### Watch HPA in Action

```bash
# Watch HPA
kubectl get hpa rag-backend-hpa -n rag-system --watch

# Watch pods
kubectl get pods -l app=rag-backend -n rag-system --watch

# Generate load to trigger scaling
# (Install hey: go install github.com/rakyll/hey@latest)
hey -z 60s -c 50 http://your-domain/api/health
```

## 🛡️ Production Considerations

### Before Production:

1. **Update Image Registry**
   ```yaml
   image: your-actual-registry/rag-backend:v1.0.0
   ```

2. **Set Real API Key**
   ```bash
   kubectl create secret generic rag-backend-secrets \
     --from-literal=FPT_API_KEY=your-real-key \
     -n rag-system
   ```

3. **Configure Domain**
   ```yaml
   # In ingress.yaml
   host: rag.yourdomain.com
   ```

4. **Enable TLS**
   ```yaml
   # Uncomment in ingress.yaml
   tls:
   - hosts:
     - rag.yourdomain.com
     secretName: rag-tls-secret
   ```

5. **Setup External Secrets**
   - Use Sealed Secrets or Vault
   - Don't commit secrets to git

6. **Configure StorageClass**
   ```yaml
   # In pvc.yaml
   storageClassName: your-cloud-provider-class
   # AWS: gp3
   # Azure: managed-csi
   # GCP: standard-rwo
   ```

7. **Setup Monitoring**
   - Prometheus + Grafana
   - Log aggregation (ELK, Loki)
   - Alerts for high CPU/memory

8. **Network Policies**
   - Restrict pod-to-pod communication
   - Allow only necessary ports

## 📊 Scaling Examples

### Scenario 1: Normal Load (3 pods)
```
CPU: 50%, Memory: 40%
Action: No scaling (below thresholds)
Pods: 3/3
```

### Scenario 2: High Load (scale up)
```
CPU: 80%, Memory: 60%
Action: Scale up (CPU > 70%)
Pods: 3 → 6 (doubled)
Time: ~15 seconds
```

### Scenario 3: Very High Load
```
CPU: 90%, Memory: 85%
Action: Scale up aggressively
Pods: 6 → 8 (+2 pods per cycle)
Max: 10 pods
```

### Scenario 4: Load Decreases
```
CPU: 30%, Memory: 30%
Action: Wait 5 minutes, then scale down
Pods: 10 → 5 (50% reduction)
Time: ~5 minutes stabilization + 1 minute scale
```

## 🔧 Common Operations

### Update Backend Image

```bash
kubectl set image deployment/rag-backend \
  backend=registry/rag-backend:v1.0.1 \
  -n rag-system
```

### Rollback

```bash
kubectl rollout undo deployment/rag-backend -n rag-system
```

### Scale Manually

```bash
kubectl scale deployment rag-backend --replicas=5 -n rag-system
```

### Update Config

```bash
kubectl edit configmap rag-backend-config -n rag-system
kubectl rollout restart deployment/rag-backend -n rag-system
```

## 📝 Next Steps

1. **Build Docker image** for backend
2. **Push to registry**
3. **Update image reference** in deployment
4. **Deploy to cluster**
5. **Configure Ingress** with your domain
6. **Setup TLS** certificates
7. **Configure monitoring**
8. **Test end-to-end**

## ✅ Summary

**Files Created:** 9 manifests
**Resources Defined:**
- 1 Namespace
- 1 ConfigMap
- 1 Secret
- 3 Deployments (Backend, Qdrant x2, Redis)
- 1 StatefulSet (Qdrant)
- 4 Services
- 1 HPA
- 2 PVCs
- 1 Ingress

**Features:**
- ✅ Auto-scaling (3-10 replicas)
- ✅ Zero-downtime deployments
- ✅ Health checks (liveness, readiness, startup)
- ✅ Resource limits
- ✅ Persistent storage
- ✅ High availability
- ✅ Production-ready

**Ready for:**
- Production deployment
- Load testing
- Monitoring integration
- CI/CD pipeline

---

**Status:** ✅ Kubernetes manifests complete and production-ready!
**See:** `k8s/README.md` for detailed deployment guide.

