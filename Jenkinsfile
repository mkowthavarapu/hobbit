pipeline {
    agent any

    tools { 
        nodejs "node" // Define the Node.js version installed in Jenkins
    }

    environment {
        PYTHON_VERSION = '3.10' // Python version (optional)
        NODE_VERSION = '16'    // Node.js version (optional)
        PROJECT = 'hobbit'

        // Define base ports for each branch
        DEV_BACKEND_PORT = 8001
        DEV_FRONTEND_PORT = 3001
        QA_BACKEND_PORT = 8002
        QA_FRONTEND_PORT = 3002
        UAT_BACKEND_PORT = 8003
        UAT_FRONTEND_PORT = 3003
        PREPROD_BACKEND_PORT = 8004
        PREPROD_FRONTEND_PORT = 3004
        PROD_BACKEND_PORT = 8005
        PROD_FRONTEND_PORT = 3005
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
                        docker build -t ${PROJECT}-api:${BRANCH_NAME} api/
                        docker build -t ${PROJECT}-frontend:${BRANCH_NAME} frontend/
                    '''
                }
            }
        }

        // Stage 5: Deploy Based on Branch
        stage('Deploy') {
            steps {
                script {
                    echo "Determining deployment environment for branch: ${env.BRANCH_NAME}..."

                    def backendPort
                    def frontendPort
                    switch (env.BRANCH_NAME) {
                        case 'dev':
                            backendPort = DEV_BACKEND_PORT
                            frontendPort = DEV_FRONTEND_PORT
                            break
                        case 'qa':
                            backendPort = QA_BACKEND_PORT
                            frontendPort = QA_FRONTEND_PORT
                            break
                        case 'uat':
                            backendPort = UAT_BACKEND_PORT
                            frontendPort = UAT_FRONTEND_PORT
                            break
                        case 'preprod':
                            backendPort = PREPROD_BACKEND_PORT
                            frontendPort = PREPROD_FRONTEND_PORT
                            break
                        case 'master':
                            backendPort = PROD_BACKEND_PORT
                            frontendPort = PROD_FRONTEND_PORT
                            break
                        default:
                            error "Unknown branch: ${env.BRANCH_NAME}. No deployment configured."
                    }

                    echo "Deploying backend to port $backendPort and frontend to port $frontendPort for branch ${env.BRANCH_NAME}..."

                    // Stop and remove existing containers before running new ones
                    sh """
                        docker stop ${BRANCH_NAME}-${PROJECT}-api || true
                        docker rm ${BRANCH_NAME}-${PROJECT}-api || true
                        docker stop ${BRANCH_NAME}-${PROJECT}-frontend || true
                        docker rm ${BRANCH_NAME}-${PROJECT}-frontend || true

                        docker run -d --name ${BRANCH_NAME}-${PROJECT}-api -p ${backendPort}:8000 ${PROJECT}-api${BRANCH_NAME}
                        docker run -d --name ${BRANCH_NAME}-${PROJECT}-frontend -p ${frontendPort}:3000 ${PROJECT}-frontend:${BRANCH_NAME}
                    """
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
