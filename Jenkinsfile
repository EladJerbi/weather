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
                        env.IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT}"
                        echo "Branch Name: ${env.GIT_BRANCH}"
                        echo "Image imageTag : ${IMAGE_TAG}"
                        echo "Building Docker image for ${env.GIT_BRANCH} branch"
                        sh "/kaniko/executor --context `pwd` --destination $DOCKER_REGISTRY/${IMAGE_NAME}-testing:$IMAGE_TAG"
                    }
                }
            }
        }
        stage('Update Gitops repo Helm chart.') {
            steps {
                container('jnlp') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'gitops-weather', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                            sh '''
                            git config --global user.name "$GIT_USERNAME"
                            git config --global user.email "$GIT_USERNAME@gmail.com"
                            git clone https://$GIT_USERNAME:$GIT_PASSWORD@github.com/EladJerbi/gitops-weather.git
                            '''
                            def valuesPath = env.GIT_BRANCH == 'origin/main' ? 'weather-prod' : 'weather-dev'
                            sh """
                            cd ./gitops-weather/k8s/weather
                            ./version-chart.sh ${valuesPath} ${env.IMAGE_TAG}
                            git add .
                            git commit -m "Update image tag"
                            git push origin main
                            """
                        }
                    }
                }
            }
        }
    }
}
