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
            /kaniko/executor --context `pwd` --cache=true --cache-dir=/workspace/cache --destination eladjerbi/weather:kaniko-test
          '''
        }
     }
   }
  }
}