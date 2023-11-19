pipeline {
    agent {
        kubernetes {
            cloud 'minikube'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - sleep
    args:
    - 9999999
"""
        }
    }
    stages {
        stage('Build Docker Image') {
            steps {
                container('kaniko') {
                    sh '/kaniko/executor --context `pwd` --destination eladjerbi/weather:kaniko-test'
                }
            }
        }
    }
}