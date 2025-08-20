pipeline {
    agent any

    environment {
        IMAGE_NAME = "bvstestingwhapp"
        CONTAINER_NAME = "bvstestingwhapp-container"
    }

    triggers {
        // This will trigger the pipeline when GitHub webhook fires (on push)
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Falak789/bvstestingapp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Stop & remove if already running
                    bat "docker rm -f ${CONTAINER_NAME} || echo 'No container to remove hello world'"

                    // Start a new container (mapping port 8000 -> 5000 inside container)
                    bat "docker run -d --name ${CONTAINER_NAME} -p 8000:5000 ${IMAGE_NAME}:latest"
                }
            }
        }
    }
}
