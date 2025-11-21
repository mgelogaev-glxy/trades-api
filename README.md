# Trades & Positions API

Enterprise-grade FastAPI application with full CI/CD pipeline.

## 🏗️ Architecture

```
Developer → GitHub → Jenkins → ECR → EKS → Production
```

## 🚀 Features

- ✅ FastAPI REST API
- ✅ Docker containerization
- ✅ Automated CI/CD with Jenkins
- ✅ AWS ECR (Private Docker Registry)
- ✅ AWS EKS (Kubernetes)
- ✅ High Availability (3 pods, 2 AZs)
- ✅ Zero-downtime deployments
- ✅ Auto-rollback on failure
- ✅ Load balancer with health checks

## 📋 Prerequisites

- Python 3.11+
- Docker
- AWS CLI
- kubectl
- Access to AWS account

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api:app --reload

# Access API
http://localhost:8000
http://localhost:8000/docs
```

## 🐳 Docker

```bash
# Build image
docker build -t trades-api .

# Run container
docker run -p 8000:8000 trades-api

# Test
curl http://localhost:8000
```

## ☁️ AWS Deployment

### Jenkins Pipeline

The CI/CD pipeline automatically:
1. Pulls code from GitHub
2. Builds Docker image
3. Runs tests
4. Pushes to ECR
5. Deploys to EKS

### Manual Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get service
```

## 📊 API Endpoints

- `GET /` - Health check
- `GET /trades` - Get trades data
- `GET /positions` - Get positions data
- `GET /version` - API version info
- `GET /docs` - Interactive API documentation

## 🔒 Security

- IAM roles for authentication (no hardcoded keys)
- Private ECR registry
- Environment variables for configuration
- Secrets managed via AWS Secrets Manager (production)

## 📈 Monitoring

- Kubernetes health checks (liveness & readiness probes)
- Load balancer health checks
- CloudWatch logs (optional)

## 🛠️ Infrastructure

- **Jenkins**: CI/CD automation
- **ECR**: Docker image registry
- **EKS**: Kubernetes cluster (2 nodes, t3.small)
- **Load Balancer**: AWS Classic Load Balancer
- **Networking**: VPC with public subnets in 2 AZs

## 📝 Environment Variables

See `.env.example` for required environment variables.

**NEVER commit `.env` to git!**

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Push to GitHub
4. Jenkins automatically deploys!

## 📚 Documentation

See `/learning/ci-cd/` for detailed documentation:
- `jenkins-docker-ecr-complete-guide.md` - CI/CD setup
- `eks-basics.md` - Kubernetes fundamentals
- `k8s.md` - Complete project walkthrough

## 👨‍💻 Author

Built with ❤️ using modern DevOps practices
