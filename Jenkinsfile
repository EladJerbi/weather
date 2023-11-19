pipeline {
    agent {
        kubernetes {
            cloud 'minikube'
        }
    }
    stages {
        stage('checkout') {
            steps {
                container('jnlp') {
                    script {
                        try {
                            sh 'hostname'
                        } catch (Exception e) {
                            echo "Error building Docker image: ${e}"
                            throw e
                        }
                    }
                }
            }
        }
    }
}