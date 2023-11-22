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
          sh 'ls /home/jenkins/agent/workspace/weather'
          sh 'export PYTHONPATH=/home/jenkins/agent/workspace:$PYTHONPATH'
          sh 'python3 -m unittest discover -s tests -p "test_*.py"'
        }
      }
    }
    stage('Build with Kaniko') {
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh 'ls /home/jenkins/agent/workspace/weather'
          sh '''#!/busybox/sh
            /kaniko/executor --context /home/jenkins/agent/workspace/weather --cache=true --cache-dir=/workspace/cache --destination eladjerbi/weather:kaniko-test
          '''
        }
      }
    }
  }
}