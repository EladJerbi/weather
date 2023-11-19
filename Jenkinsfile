podTemplate(cloud: 'minikube', containers: [
    containerTemplate(name: 'kubectl', image: 'lachlanevenson/k8s-kubectl', command: 'cat', ttyEnabled: true)
]) {
    node('kubectl') {
        stage('Run kubectl command') {
            container('kubectl') {
                sh 'kubectl get pods'
            }
        }
    }
}