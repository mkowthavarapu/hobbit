pipeline {
    agent any

    tools { 
        nodejs "node" // Define the Node.js version installed in Jenkins
    }

    environment {
        PYTHON_VERSION = '3.10' // Optional: Python version
        NODE_VERSION = '16'    // Optional: Node.js version

        // Define ports for each branch
        DEV_PORT = 8001
        QA_PORT = 8002
        UAT_PORT = 8003
        PREPROD_PORT = 8004
        PROD_PORT = 8005
    }

    stages {
        // Stage 1: Clone the repository
        stage('Checkout') {
            steps {
                echo 'Checking out the code...'
                git 'https://github.com/mkowthavarapu/hobbit.git'
            }
        }

        // Stage 2: Set up backend (FastAPI)
        stage('Setup Backend (FastAPI)') {
            steps {
                script {
                    echo 'Setting up Python environment for FastAPI...'
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate && pip install --upgrade pip
                        . venv/bin/activate && pip install -r api/requirements.txt
                    '''
                }
            }
        }

        // Stage 3: Build frontend (ReactJS)
        stage('Build Frontend (ReactJS)') {
            steps {
                script {
                    echo 'Installing Node.js dependencies and building the frontend...'
                    sh '''
                        npm install --prefix frontend
                        npm run build --prefix frontend
                    '''
                }
            }
        }

        // Stage 4: Build Docker Images
        stage('Build Docker Images') {
            steps {
                script {
                    echo 'Building Docker images for backend and frontend...'
                    sh '''
                        docker build -t fastapi-backend:${env.BRANCH_NAME} api/
                        docker build -t react-frontend:${env.BRANCH_NAME} frontend/
                    '''
                }
            }
        }

        // Stage 5: Deploy Based on Branch
        stage('Deploy') {
            steps {
                script {
                    echo "Determining deployment environment for branch: ${env.BRANCH_NAME}..."
                    
                    def port
                    switch (env.BRANCH_NAME) {
                        case 'dev':
                            port = DEV_PORT
                            break
                        case 'qa':
                            port = QA_PORT
                            break
                        case 'uat':
                            port = UAT_PORT
                            break
                        case 'preprod':
                            port = PREPROD_PORT
                            break
                        case 'master':
                            port = PROD_PORT
                            break
                        default:
                            error "Unknown branch: ${env.BRANCH_NAME}. No deployment configured."
                    }

                    echo "Deploying to port $port for branch ${env.BRANCH_NAME}..."

                    // Stop and remove existing containers before running new ones
                    sh '''
                        docker stop ${env.BRANCH_NAME}-fastapi || true
                        docker rm ${env.BRANCH_NAME}-fastapi || true
                        docker stop ${env.BRANCH_NAME}-frontend || true
                        docker rm ${env.BRANCH_NAME}-frontend || true

                        docker run -d --name ${env.BRANCH_NAME}-fastapi -p $port:8000 fastapi-backend:${env.BRANCH_NAME}
                        docker run -d --name ${env.BRANCH_NAME}-frontend -p $((port+1000)):3000 react-frontend:${env.BRANCH_NAME}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo "Build and deployment successful for branch: ${env.BRANCH_NAME}!"
        }
        failure {
            echo 'Build or deployment failed. Check logs for details.'
        }
    }
}
