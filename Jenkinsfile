pipeline {
    agent {
        kubernetes {
            yamlFile 'pod.yaml'
        }
    }
    environment {
        // Define environment variables if needed
        DOCKER_REGISTRY = 'eladjerbi'
        IMAGE_NAME = 'weather'
        KUBE_NAMESPACE = 'testing'
        GITOPS_REPO = 'https://github.com/EladJerbi/gitops-weather.git'
    }
    stages {
        stage('Build with Kaniko for Main branch') {
            when {
                expression {
                    // Execute this stage only if the branch is 'main'
                    return env.GIT_BRANCH == 'origin/main'
                }
            }
            steps {
                script {
                    // Run version.sh and capture the output
                    env.IMAGE_TAG = sh(script: './version.sh', returnStdout: true).trim()
                }
                // Build the Docker image with Kaniko in the kaniko container
                container(name: 'kaniko', shell: '/busybox/sh') {
                    sh '''
                    echo "Building Docker image for the main branch, IMAGE_TAG created from version.sh script"
                    /kaniko/executor --context `pwd` --cache=true --cache-dir=/workspace/cache --destination $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
        stage('Build with Kaniko for feature branches') {
            when {
                expression {
                    // Execute this stage for any branch other than 'main'
                    return env.GIT_BRANCH != 'origin/main'
                }
            }
            steps {
                container(name: 'kaniko', shell: '/busybox/sh') {
                    script {
                        def imageTag = "${BUILD_NUMBER}-${GIT_COMMIT}"
                        echo "Branch Name: ${env.GIT_BRANCH}"
                        echo "Image imageTag : ${imageTag}"
                        echo "Building Docker image for ${env.GIT_BRANCH} branch"
                        sh "/kaniko/executor --context `pwd` --destination $DOCKER_REGISTRY/${IMAGE_NAME}-testing:$imageTag"
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                expression {
                    // Execute this stage for any branch
                    return true
                }
            }
            steps {
                container('argo') {
                    sh 'echo "Deploying to Kubernetes cluster"'
                    script {
                        if (env.GIT_BRANCH == 'origin/main') {
                            echo "Deploying to weather-prod"
                            // sh "argocd app set weather-app --repo $GITOPS_REPO --path . --dest-namespace $KUBE_NAMESPACE"
                            // sh "argocd app sync weather-app"
                            argocd -h
                        } else {
                            echo "Deploying to weather-testing"
                            // def imageTag = "${BUILD_NUMBER}-${GIT_COMMIT}"
                            // sh "kubectl run weather${BUILD_NUMBER} --image=eladjerbi/$IMAGE_NAME-testing:${imageTag} -n testing"
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            script {
                // Login to Git
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    sh '''
                    git config --global user.name "$GIT_USERNAME"
                    git config --global user.email "$GIT_USERNAME@gmail.com"
                    git remote set-url origin https://github.com/EladJerbi/weather.git
                    '''
                }
                // Push tags
                sh 'git push --tags'
            }
        }
    }
}


