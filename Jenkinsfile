pipeline {
    agent {
        kubernetes {
            yamlFile 'pipeline-pod.yaml'
        }
    }
    stages {
        stage('Build Docker Image') {
            steps {
                container('kaniko') {
                    sh 'ls /workspace/dockerfile'
                    sh 'ls ./*'
                    sh 'ls'
                    sh '/kaniko/executor --context `pwd` --destination eladjerbi/weather:kaniko-test'
                }
                container('jnlp') {
                    sh 'ls /workspace/dockerfile'
                    sh 'ls ./*'
                    sh 'ls'
                }
            }
        }
    }
}
