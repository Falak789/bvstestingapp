pipeline {
	agent any

	environment {
		IMAGE_NAME = "bvstestingwebhookapp"
		CONTAINER_NAME = "bvstestingwebhookapp-container"
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

		stage('Docker Login') {
			steps {
				script {
					bat "docker login -u falak26 -p FIFI-taf-321"
				}
			}
		}

		stage('Push Docker Image') {
			steps {
				script {
					bat "docker tag bvstestingwebhookapp:latest falak26/bvstestingwebhookapp:latest"
					bat "docker push falak26/${IMAGE_NAME}:latest"
				}
			}
		}

		stage('Run Container') {
			steps {
				script {
					// Stop & remove if already running
					bat "docker rm -f ${CONTAINER_NAME} || echo 'No container to remove'"

					// Start a new container (mapping port 8081 -> 5000 inside container)
					bat "docker run -d --name ${CONTAINER_NAME} -p 8082:5000 ${IMAGE_NAME}:latest"
				}
			}
		}
	}
}
