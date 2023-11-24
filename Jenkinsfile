pipeline {
  agent {
    kubernetes {
      yamlFile 'pod.yaml'
    }
   }
  stages {
    stage('Build with Kaniko') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''#!/busybox/sh
            /kaniko/executor --context `pwd` --cache=true --cache-dir=/workspace/cache --destination $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG
          '''
        }
     }
   }
    stage('Deploy with kubectl') {
      steps {
        container('kubectl') {
          sh '''
            kubectl run weather-testing --image=eladjerbi/weather:kaniko-test -n testing
          '''
        }
      }
    }
  }
}
