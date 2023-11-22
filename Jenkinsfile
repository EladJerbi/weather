pipeline {
  agent {
    kubernetes {
      yamlFile 'kaniko-pod.yaml'
    }
  }
  stages {
    stage('Run unit tests') {
      steps {
        container('jnlp') {
          sh 'python3 -m unittest discover -s tests -p "test_*.py"'
        }
      }
    }
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