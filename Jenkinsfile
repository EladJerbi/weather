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
"""
        }
    }
    stages {
        stage('Run kubectl command') {
            steps {
                container('kubectl') {
                    script {
                        try {
                            sh 'kubectl get pods'
                        } catch (Exception e) {
                            echo "Error running kubectl get pods: ${e}"
                            throw e
                        }
                    }
                }
            }
        }
    }
}