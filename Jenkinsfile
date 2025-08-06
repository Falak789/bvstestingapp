pipeline {
    agent {
        docker { image 'python:3.10' }
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Falak789/bvstestingapp.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t bvs-api-tester .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 bvs-api-tester'
            }
        }
    }
}
