# AI Shield Auditor - Deployment Guide

## Table of Contents
- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
  - [Streamlit Cloud](#streamlit-cloud)
  - [AWS (ECS/Fargate)](#aws-ecsfargate)
  - [Google Cloud Run](#google-cloud-run)
  - [Azure Container Instances](#azure-container-instances)
  - [Railway](#railway)
  - [Render](#render)
- [Environment Variables](#environment-variables)
- [Production Checklist](#production-checklist)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)
- Git

### Local Setup

```bash
# Clone repository
cd ai-shield-auditor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## Local Development

### Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dev dependencies (if any)
pip install -r requirements.txt

# Run with auto-reload
streamlit run app.py --server.runOnSave=true
```

### Testing Changes

```bash
# Test with different LLM providers
export LLM_PROVIDER=openai
streamlit run app.py

# Test without LLM (checklist mode only)
export LLM_PROVIDER=none
streamlit run app.py
```

---

## Docker Deployment

### Build and Run Locally

```bash
# Build image
docker build -t ai-shield-auditor:latest .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  -e LLM_PROVIDER=openai \
  -v $(pwd)/reports:/app/reports \
  ai-shield-auditor:latest
```

### Using Docker Compose

```bash
# Start application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

### Docker Compose with Environment File

Create `.env` file:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=openai
LOG_LEVEL=INFO
```

Then run:
```bash
docker-compose up -d
```

---

## Cloud Deployment

### Streamlit Cloud

**Easiest option for quick deployment**

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`
6. Add secrets in "Advanced settings":
   ```toml
   OPENAI_API_KEY = "sk-..."
   ANTHROPIC_API_KEY = "sk-ant-..."
   LLM_PROVIDER = "openai"
   ```
7. Deploy!

**Pros:**
- Free tier available
- Automatic HTTPS
- Easy updates via Git push
- Managed infrastructure

**Cons:**
- Resource limits on free tier
- Public by default (Enterprise for private apps)

---

### AWS (ECS/Fargate)

**For enterprise-grade deployment**

#### Step 1: Build and Push to ECR

```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name ai-shield-auditor

# Build and tag
docker build -t ai-shield-auditor .
docker tag ai-shield-auditor:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-shield-auditor:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-shield-auditor:latest
```

#### Step 2: Create ECS Task Definition

Create `task-definition.json`:

```json
{
  "family": "ai-shield-auditor",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "ai-shield-auditor",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-shield-auditor:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LLM_PROVIDER",
          "value": "openai"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:openai-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-shield-auditor",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Step 3: Create Service

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster your-cluster \
  --service-name ai-shield-auditor \
  --task-definition ai-shield-auditor \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

**Cost:** ~$30-50/month for basic setup

---

### Google Cloud Run

**Serverless, auto-scaling deployment**

```bash
# Build and deploy in one command
gcloud run deploy ai-shield-auditor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LLM_PROVIDER=openai \
  --set-secrets OPENAI_API_KEY=openai-key:latest \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 0 \
  --max-instances 10
```

**Pros:**
- Pay-per-use (free tier available)
- Auto-scaling
- HTTPS included
- Easy rollbacks

**Cost:** ~$5-20/month with typical usage

---

### Azure Container Instances

```bash
# Create resource group
az group create --name ai-shield-rg --location eastus

# Create container instance
az container create \
  --resource-group ai-shield-rg \
  --name ai-shield-auditor \
  --image <your-registry>/ai-shield-auditor:latest \
  --dns-name-label ai-shield-auditor \
  --ports 8501 \
  --environment-variables \
    LLM_PROVIDER=openai \
  --secure-environment-variables \
    OPENAI_API_KEY=sk-... \
  --cpu 2 \
  --memory 4
```

---

### Railway

**Modern, developer-friendly platform**

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

3. Add environment variables in Railway dashboard

**Cost:** Free tier available, then $5/month+

---

### Render

**Simple deployment from Git**

1. Create `render.yaml`:

```yaml
services:
  - type: web
    name: ai-shield-auditor
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: LLM_PROVIDER
        value: openai
      - key: OPENAI_API_KEY
        sync: false
    healthCheckPath: /_stcore/health
```

2. Connect your GitHub repo to Render
3. Deploy automatically on push

**Cost:** Free tier available, then $7/month+

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider to use | `openai`, `anthropic`, `none` |

### Optional (for LLM mode)

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
| `LOG_LEVEL` | Logging level | `INFO`, `DEBUG`, `WARNING` |

### Setting Environment Variables

#### Local (.env file)
```env
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
LOG_LEVEL=INFO
```

#### Docker
```bash
docker run -e OPENAI_API_KEY=sk-... ai-shield-auditor
```

#### Kubernetes
```yaml
env:
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: ai-shield-secrets
        key: openai-api-key
```

---

## Production Checklist

### Security
- [ ] API keys stored in secrets manager (not in code)
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Input validation enabled
- [ ] Security headers configured
- [ ] Container runs as non-root user
- [ ] Secrets rotation policy in place

### Performance
- [ ] Resource limits configured (CPU, memory)
- [ ] Caching enabled where appropriate
- [ ] Auto-scaling configured
- [ ] Health checks enabled
- [ ] Load balancer configured (if multi-instance)

### Monitoring
- [ ] Application logs centralized
- [ ] Error tracking configured (e.g., Sentry)
- [ ] Uptime monitoring enabled
- [ ] Performance metrics tracked
- [ ] Alerts configured for critical issues

### Backup & Recovery
- [ ] Reports directory backed up
- [ ] Database backups (if using persistence)
- [ ] Disaster recovery plan documented
- [ ] Rollback procedure tested

### Compliance
- [ ] Data retention policy defined
- [ ] Privacy policy published
- [ ] GDPR compliance reviewed (if applicable)
- [ ] Audit logging enabled

---

## Monitoring & Logging

### Health Check Endpoint

Streamlit provides a built-in health check:
```
GET http://your-app/_stcore/health
```

Returns 200 OK if healthy.

### Application Logs

View logs based on deployment:

**Docker:**
```bash
docker logs -f <container-id>
```

**Docker Compose:**
```bash
docker-compose logs -f
```

**Kubernetes:**
```bash
kubectl logs -f deployment/ai-shield-auditor
```

**Cloud Run:**
```bash
gcloud run services logs read ai-shield-auditor --limit=50
```

### Custom Monitoring

Add to your app:
```python
from core.health import get_health_status, check_dependencies

# In sidebar or admin page
if st.button("Health Check"):
    status = get_health_status()
    st.json(status)
```

---

## Troubleshooting

### Application won't start

**Symptom:** Container exits immediately

**Solutions:**
1. Check logs: `docker logs <container-id>`
2. Verify environment variables are set
3. Check Python version compatibility
4. Ensure all dependencies installed

### Import errors

**Symptom:** `ModuleNotFoundError`

**Solutions:**
```bash
# Rebuild with no cache
docker build --no-cache -t ai-shield-auditor .

# Verify requirements.txt includes all dependencies
pip install -r requirements.txt
```

### Port conflicts

**Symptom:** `Address already in use`

**Solutions:**
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process or use different port
docker run -p 8502:8501 ai-shield-auditor
```

### Out of memory

**Symptom:** Container crashes, OOM errors

**Solutions:**
1. Increase memory limit in docker-compose.yml
2. Reduce concurrent requests
3. Optimize data processing
4. Use smaller model if using LLM mode

### API key errors

**Symptom:** Authentication errors with LLM providers

**Solutions:**
1. Verify API key format
2. Check key is not expired
3. Ensure correct provider selected
4. Test key directly with provider's API

### Slow performance

**Solutions:**
1. Enable caching in Streamlit
2. Reduce scan frequency
3. Optimize database queries (if using persistence)
4. Scale horizontally (add more instances)

---

## Support

- **Issues:** [GitHub Issues](https://github.com/your-repo/ai-shield-auditor/issues)
- **Documentation:** Check README.md and QUICKSTART.md
- **Community:** [Discussions](https://github.com/your-repo/ai-shield-auditor/discussions)

---

## Next Steps

After successful deployment:
1. Configure monitoring and alerts
2. Set up automated backups
3. Document your deployment architecture
4. Plan for scaling strategy
5. Implement CI/CD pipeline
6. Review security hardening checklist

**Ready to deploy? Start with Docker locally, then move to your preferred cloud platform!**
