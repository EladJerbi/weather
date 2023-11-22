pipeline {
  agent {
    kubernetes {
      yamlFile 'pod.yaml'
    }
   }
  stages {
    stage('Run unit tests') {
      steps {
        container('python') {
          sh 'export PYTHONPATH=/home/jenkins/agent/workspace:$PYTHONPATH'
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