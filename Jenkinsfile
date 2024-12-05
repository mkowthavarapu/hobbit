pipeline {
    agent any
    
    environment {
        // Define Python and Node versions if needed
        PYTHON_VERSION = '3.10'
        NODE_VERSION = '16'
    }
    
    stages {
        
        // Stage 1: Clone the repository
        stage('Checkout') {
            steps {
                git 'https://github.com/yourusername/hobbit.git'
            }
        }
        
        // Stage 2: Set up backend (FastAPI)
        stage('Setup Backend (FastAPI)') {
            steps {
                script {
                    // Set up Python environment
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install -r api/requirements.txt'
                }
            }
        }
        
        // Stage 3: Run backend tests
        stage('Test Backend') {
            steps {
                script {
                    sh '. venv/bin/activate && pytest api/tests'
                }
            }
        }

        // Stage 4: Build frontend (ReactJS)
        stage('Build Frontend (ReactJS)') {
            steps {
                script {
                    // Install NodeJS dependencies and build
                    sh 'npm install --prefix frontend'
                    sh 'npm run build --prefix frontend'
                }
            }
        }
        
        // Stage 5: Run frontend tests (Optional)
        stage('Test Frontend') {
            steps {
                script {
                    sh 'npm test --prefix frontend'
                }
            }
        }
        
        // Stage 6: Build Docker Images (Optional)
        stage('Build Docker Images') {
            steps {
                script {
                    // Build backend Docker image
                    sh 'docker build -t fastapi-backend backend/'

                    // Build frontend Docker image
                    sh 'docker build -t react-frontend frontend/'
                }
            }
        }

        // Stage 7: Deploy (Optional, you can deploy to a cloud service)
        stage('Deploy') {
            steps {
                script {
                    // Example of deploying to a cloud (e.g., AWS, Heroku)
                    sh 'docker run -d -p 8000:8000 fastapi-backend'
                    sh 'docker run -d -p 3000:3000 react-frontend'
                }
            }
        }
    }

    post {
        success {
            echo 'Build and deployment successful.'
        }
        failure {
            echo 'Build or deployment failed.'
        }
    }
}
