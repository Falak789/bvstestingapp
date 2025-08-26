pipeline {
    agent any

    environment {
        IMAGE_NAME = "bvstestingec2app"
        DOCKER_USER = "falak789"
        DOCKER_PASS = "FIFI-taf-321"
        CONTAINER_NAME = "bvstestingec2app-container"
        DOCKER_CREDENTIALS = 'docker-hub-creds'    // Jenkins credentials ID for Docker Hub
        SSH_CREDENTIALS = 'ec2-ssh-creds'          // Jenkins credentials ID for EC2 SSH
        EC2_HOST = "ubuntu@54.89.241.89"      // Replace with your EC2 user & IP
    }

    triggers {
        // This will trigger the pipeline when GitHub webhook fires (on push)
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Falak789/bvstestingapp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                        bat "docker tag ${IMAGE_NAME}:latest %DOCKER_USER%/${IMAGE_NAME}:latest"
                        bat "docker push %DOCKER_USER%/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                sshagent(credentials: ["${SSH_CREDENTIALS}"]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_HOST} \\
                        "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS} && \\
                         docker pull ${DOCKER_USER}/${IMAGE_NAME}:latest && \\
                         docker rm -f ${CONTAINER_NAME} || true && \\
                         docker run -d --name ${CONTAINER_NAME} -p 8000:5000 ${DOCKER_USER}/${IMAGE_NAME}:latest"
                    """
                }
            }
        }
    }
}
