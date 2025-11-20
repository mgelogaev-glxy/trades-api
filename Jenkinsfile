pipeline {
    agent any
    
    environment {
        AWS_ACCOUNT_ID = '465915553437'
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = '465915553437.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'trades-api'
        IMAGE_TAG = "${BUILD_NUMBER}"
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
                    # Login to ECR (uses EC2 instance role)
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
    }
    
    post {
        success {
            echo '🎉 Pipeline completed successfully!'
            echo "Image available at: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed! Check the logs above.'
        }
        always {
            echo '🧹 Cleaning up unused Docker resources...'
            sh 'docker system prune -f || true'
        }
    }
}