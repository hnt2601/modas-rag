# Kubernetes Manifests for RAG System

Production-ready Kubernetes deployment configurations for the RAG system.

## 📁 Files Overview

```
k8s/
├── namespace.yaml              # rag-system namespace
├── configmap.yaml             # Non-sensitive configuration
├── secrets.yaml               # Sensitive credentials (FPT_API_KEY)
├── backend-deployment.yaml    # Backend Deployment + Service + HPA
├── pvc.yaml                   # PersistentVolumeClaims
├── qdrant-statefulset.yaml    # Qdrant vector database
├── redis-deployment.yaml      # Redis cache (optional)
├── ingress.yaml               # HTTP/HTTPS routing
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- StorageClass available (default: `standard`)
- Ingress controller (NGINX recommended)

### 1. Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### 2. Create Secrets

**Option A: From file (not recommended for production)**
```bash
# Edit secrets.yaml and add your FPT_API_KEY
kubectl apply -f secrets.yaml
```

**Option B: From command line (recommended)**
```bash
kubectl create secret generic rag-backend-secrets \
  --from-literal=FPT_API_KEY=your-actual-fpt-api-key \
  -n rag-system
```

### 3. Create ConfigMap

```bash
kubectl apply -f configmap.yaml
```

### 4. Create PersistentVolumeClaims

```bash
kubectl apply -f pvc.yaml
```

### 5. Deploy Qdrant (Vector Database)

```bash
kubectl apply -f qdrant-statefulset.yaml
```

Wait for Qdrant to be ready:
```bash
kubectl wait --for=condition=ready pod -l app=qdrant -n rag-system --timeout=300s
```

### 6. Deploy Redis (Optional)

```bash
kubectl apply -f redis-deployment.yaml
```

### 7. Deploy Backend

```bash
kubectl apply -f backend-deployment.yaml
```

Wait for backend to be ready:
```bash
kubectl wait --for=condition=ready pod -l app=rag-backend -n rag-system --timeout=300s
```

### 8. Create Ingress

```bash
# Update domain in ingress.yaml first
kubectl apply -f ingress.yaml
```

## 🔍 Verification

### Check All Resources

```bash
kubectl get all -n rag-system
```

### Check Pods Status

```bash
kubectl get pods -n rag-system -o wide
```

Expected output:
```
NAME                           READY   STATUS    RESTARTS   AGE
rag-backend-xxx-yyy           1/1     Running   0          2m
rag-backend-xxx-zzz           1/1     Running   0          2m
rag-backend-xxx-aaa           1/1     Running   0          2m
qdrant-0                      1/1     Running   0          3m
qdrant-1                      1/1     Running   0          3m
redis-xxx-yyy                 1/1     Running   0          3m
```

### Check Services

```bash
kubectl get svc -n rag-system
```

### Check HPA Status

```bash
kubectl get hpa -n rag-system
```

### Check Ingress

```bash
kubectl get ingress -n rag-system
```

### Test Health Endpoint

```bash
# Port forward for testing
kubectl port-forward svc/rag-backend-service 8000:8000 -n rag-system

# In another terminal
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "qdrant": "ok",
    "fpt_cloud": "ok"
  }
}
```

## 📊 Resource Configuration

### Backend Deployment

**Replicas:** 3-10 (auto-scaled by HPA)

**Resources per Pod:**
- Requests: 512Mi memory, 500m CPU
- Limits: 2Gi memory, 2000m CPU

**Total Resources (3 pods):**
- Requests: 1.5Gi memory, 1.5 CPU
- Limits: 6Gi memory, 6 CPU

### Qdrant StatefulSet

**Replicas:** 2 (for HA)

**Resources per Pod:**
- Requests: 1Gi memory, 500m CPU
- Limits: 4Gi memory, 2 CPU

**Storage:** 50Gi per pod (100Gi total)

### Redis Deployment

**Replicas:** 1

**Resources:**
- Requests: 256Mi memory, 100m CPU
- Limits: 512Mi memory, 200m CPU

## 🔄 HorizontalPodAutoscaler (HPA)

The backend automatically scales based on:

**Metrics:**
- CPU utilization > 70%
- Memory utilization > 80%

**Scaling Behavior:**
- **Scale Up:** Immediate (0s stabilization)
  - Max 100% increase (double pods)
  - Or max 2 pods added
  - Every 15 seconds
- **Scale Down:** Conservative (5 min stabilization)
  - Max 50% decrease
  - Every 60 seconds

**Example Scenarios:**

| Current | CPU % | Memory % | Action | New Pods |
|---------|-------|----------|--------|----------|
| 3 pods  | 80%   | 60%      | Scale up | 6 pods |
| 6 pods  | 50%   | 50%      | Wait 5 min | 6 pods |
| 6 pods  | 30%   | 30%      | Scale down | 3 pods |

## 🛡️ Health Checks

### Liveness Probe
- Path: `/health`
- Initial Delay: 30s
- Period: 10s
- Timeout: 5s
- Failure Threshold: 3

**Action:** Restart container if fails

### Readiness Probe
- Path: `/health`
- Initial Delay: 10s
- Period: 5s
- Timeout: 3s
- Failure Threshold: 3

**Action:** Remove from service if fails

### Startup Probe
- Path: `/health`
- Initial Delay: 0s
- Period: 5s
- Timeout: 3s
- Failure Threshold: 12 (60s total)

**Action:** Allow up to 60s for app startup

## 🔐 Security

### Secrets Management

**Current:** Basic Kubernetes Secrets (base64 encoded)

**Recommended for Production:**
- Sealed Secrets
- External Secrets Operator
- HashiCorp Vault
- Cloud provider secret managers (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)

### RBAC

Create ServiceAccount with minimal permissions:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rag-backend-sa
  namespace: rag-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rag-backend-role
  namespace: rag-system
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rag-backend-rolebinding
  namespace: rag-system
subjects:
- kind: ServiceAccount
  name: rag-backend-sa
  namespace: rag-system
roleRef:
  kind: Role
  name: rag-backend-role
  apiGroup: rbac.authorization.k8s.io
```

Add to Deployment:
```yaml
spec:
  template:
    spec:
      serviceAccountName: rag-backend-sa
```

## 📈 Monitoring

### Prometheus Metrics

Backend pods are annotated for Prometheus scraping:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

### Grafana Dashboard

Import dashboards for:
- Pod metrics
- HPA metrics
- Service metrics
- Qdrant metrics

### Logging

View logs:

```bash
# All backend pods
kubectl logs -l app=rag-backend -n rag-system --tail=100 -f

# Specific pod
kubectl logs rag-backend-xxx-yyy -n rag-system --tail=100 -f

# Previous instance (if crashed)
kubectl logs rag-backend-xxx-yyy -n rag-system --previous
```

## 🔧 Common Operations

### Scale Manually

```bash
# Scale backend
kubectl scale deployment rag-backend --replicas=5 -n rag-system

# Check HPA
kubectl get hpa -n rag-system
```

### Update Configuration

```bash
# Edit ConfigMap
kubectl edit configmap rag-backend-config -n rag-system

# Rollout restart to pick up changes
kubectl rollout restart deployment/rag-backend -n rag-system
```

### Update Docker Image

```bash
# Update image
kubectl set image deployment/rag-backend \
  backend=your-registry/rag-backend:v1.0.1 \
  -n rag-system

# Check rollout status
kubectl rollout status deployment/rag-backend -n rag-system
```

### Rollback

```bash
# View rollout history
kubectl rollout history deployment/rag-backend -n rag-system

# Rollback to previous version
kubectl rollout undo deployment/rag-backend -n rag-system

# Rollback to specific revision
kubectl rollout undo deployment/rag-backend --to-revision=2 -n rag-system
```

### Debug Pod

```bash
# Execute shell in pod
kubectl exec -it rag-backend-xxx-yyy -n rag-system -- /bin/bash

# Run command
kubectl exec rag-backend-xxx-yyy -n rag-system -- env

# Copy file from pod
kubectl cp rag-system/rag-backend-xxx-yyy:/app/logs/app.log ./app.log
```

### Resource Usage

```bash
# CPU and memory usage
kubectl top pods -n rag-system

# Node usage
kubectl top nodes
```

## 🚨 Troubleshooting

### Pods Not Starting

```bash
# Describe pod for events
kubectl describe pod rag-backend-xxx-yyy -n rag-system

# Check logs
kubectl logs rag-backend-xxx-yyy -n rag-system
```

Common issues:
- Image pull errors (check registry credentials)
- ConfigMap/Secret not found
- Resource limits too low
- PVC not bound

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints rag-backend-service -n rag-system

# Check if pods are ready
kubectl get pods -l app=rag-backend -n rag-system
```

### HPA Not Scaling

```bash
# Check HPA status
kubectl describe hpa rag-backend-hpa -n rag-system

# Check metrics-server
kubectl get deployment metrics-server -n kube-system
```

### Qdrant Connection Issues

```bash
# Check Qdrant pods
kubectl get pods -l app=qdrant -n rag-system

# Check Qdrant service
kubectl get svc qdrant-service -n rag-system

# Test connectivity from backend pod
kubectl exec rag-backend-xxx-yyy -n rag-system -- \
  curl http://qdrant-service:6333
```

## 🗑️ Cleanup

### Delete All Resources

```bash
# Delete everything in namespace
kubectl delete namespace rag-system
```

### Delete Specific Resources

```bash
# Delete deployment
kubectl delete deployment rag-backend -n rag-system

# Delete service
kubectl delete service rag-backend-service -n rag-system

# Delete PVCs (WARNING: Deletes data!)
kubectl delete pvc --all -n rag-system
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Qdrant Kubernetes](https://qdrant.tech/documentation/guides/distributed_deployment/)

## 🔄 CI/CD Integration

See `.github/workflows/deploy.yaml` for automated deployment pipeline.

## 📝 Notes

- **Storage Class:** Change `storageClassName` in PVC based on your cloud provider
- **Domain:** Update `host` in `ingress.yaml` to your actual domain
- **TLS:** Uncomment TLS section in Ingress and configure cert-manager
- **Registry:** Update `image` in deployments to your container registry
- **Resources:** Adjust resource requests/limits based on your workload

## ✅ Production Checklist

Before deploying to production:

- [ ] Replace `your-registry` with actual registry
- [ ] Set real `FPT_API_KEY` in secrets
- [ ] Configure domain in Ingress
- [ ] Setup TLS certificates
- [ ] Configure external secret management
- [ ] Setup monitoring (Prometheus + Grafana)
- [ ] Configure log aggregation
- [ ] Setup backup strategy for PVCs
- [ ] Configure network policies
- [ ] Setup resource quotas
- [ ] Configure pod security policies
- [ ] Test disaster recovery procedures
- [ ] Document runbooks

## 📊 Cost Estimation

**Minimum resources (3 backend + 2 Qdrant + 1 Redis):**
- CPU: 5 cores
- Memory: 10Gi
- Storage: 200Gi

**Cost varies by cloud provider. Example AWS:**
- 3x t3.medium nodes: ~$90/month
- 200Gi EBS: ~$20/month
- Load Balancer: ~$20/month
- **Total: ~$130/month**

## License

MIT

