pipeline {
    agent {
        kubernetes {
            cloud 'minikube'
            label 'kubectl-pod'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: some-label-value
spec:
  containers:
  - name: kubectl
    image: lachlanevenson/k8s-kubectl
    command:
    - cat
    tty: true
"""
        }
    }
    stages {
        stage('Run kubectl command') {
            steps {
                container('kubectl') {
                    sh 'kubectl get pods'
                }
            }
        }
    }
}