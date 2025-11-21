pipeline {
    agent any
    
    environment {
        AWS_ACCOUNT_ID = '465915553437'
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '465915553437.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'trades-api'
        IMAGE_TAG = "${BUILD_NUMBER}"
        EKS_CLUSTER = 'trades-api-cluster'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Pulling code from GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${ECR_REPOSITORY}:${IMAGE_TAG} .
                    docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REPOSITORY}:latest
                    echo "✅ Image built: ${ECR_REPOSITORY}:${IMAGE_TAG}"
                '''
            }
        }
        
        stage('Test Image') {
            steps {
                echo '🧪 Testing Docker image...'
                sh '''
                    echo "Running basic container test..."
                    docker run --rm ${ECR_REPOSITORY}:${IMAGE_TAG} python --version
                    echo "✅ Container can run Python"
                '''
            }
        }
        
        stage('Push to ECR') {
            steps {
                echo '☁️ Pushing to AWS ECR...'
                sh '''
                    # Login to ECR
                    echo "Logging into ECR..."
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    
                    # Tag images with ECR registry
                    docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                    docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                    
                    # Push images
                    echo "Pushing image with tag: ${IMAGE_TAG}"
                    docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                    
                    echo "Pushing image with tag: latest"
                    docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                    
                    echo "✅ Images pushed successfully!"
                '''
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                sh '''
                    # Update kubeconfig
                    aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER}
                    
                    # Verify connection
                    echo "Verifying connection to EKS..."
                    kubectl get nodes
                    
                    # Update deployment with new image
                    echo "Updating deployment to use image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
                    kubectl set image deployment/trades-api \
                        trades-api=${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} \
                        --record
                    
                    # Wait for rollout to complete (timeout 5 minutes)
                    echo "Waiting for rollout to complete..."
                    kubectl rollout status deployment/trades-api --timeout=5m
                    
                    # Show deployment status
                    echo "Current deployment status:"
                    kubectl get deployment trades-api
                    kubectl get pods -l app=trades-api
                    
                    echo "✅ Deployed version ${IMAGE_TAG} to EKS!"
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 Pipeline completed successfully!'
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
            echo "Deployed to EKS cluster: ${EKS_CLUSTER}"
            sh '''
                LB_URL=$(kubectl get service trades-api-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
                echo "API accessible at: http://${LB_URL}"
            '''
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        }
        failure {
            echo '❌ Pipeline failed!'
            echo 'Rolling back to previous version...'
            sh '''
                kubectl rollout undo deployment/trades-api || true
                echo "Rollback initiated. Check deployment status:"
                kubectl get deployment trades-api
            '''
        }
        always {
            echo '🧹 Cleaning up unused Docker resources...'
            sh 'docker system prune -f || true'
        }
    }
}