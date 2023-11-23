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
    stage('Deploy with kubectl') {
      steps {
        container('kubectl') {
          sh '''
            kubectl get pods -n testing
            kubectl get pods -n jenkins-agents
          '''
        }
      }
    }
  }
}