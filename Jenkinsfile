pipeline {
  agent {
    kubernetes {
        yamlFile 'buildah-pod.yaml'
    }
  }
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    durabilityHint('PERFORMANCE_OPTIMIZED')
    disableConcurrentBuilds()
  }
  environment {
    DH_CREDS=credentials('dockerhub')
  }
  stages {
    stage('Build with Buildah') {
      steps {
        container('buildah') {
          sh 'buildah build -t eladjerbi/weather:buildah-test .'
        }
      }
    }
    stage('Login to Docker Hub') {
      steps {
        container('buildah') {
          sh 'echo $DH_CREDS_PSW | buildah login -u $DH_CREDS_USR --password-stdin docker.io'
        }
      }
    }
    stage('tag image') {
      steps {
        container('buildah') {
          sh 'buildah tag eladjerbi/weather:buildah-test eladjerbi/weather:buildah-test-taged'
        }
      }
    }
    stage('push image') {
      steps {
        container('buildah') {
          sh 'buildah push eladjerbi/weather:buildah-test'
          sh 'buildah push eladjerbi/weather:buildah-test-taged'
        }
      }
    }
  }
  post {
    always {
      container('buildah') {
        sh 'buildah logout docker.io'
      }
    }
  }
}