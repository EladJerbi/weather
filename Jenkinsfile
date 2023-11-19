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
                    sh '/kaniko/executor --context `pwd` --destination eladjerbi/weather:kaniko-test'
                }
            }
        }
    }
}