pipeline {
	agent any
    environment {
        COLOR = 'blue'
    }
	stages {

		stage('Linting') {
			steps {
				sh 'tidy -q -e *.html'
                sh 'hadolint Dockerfile'
			}
		}

		stage('copy green') {

            when {
                expression { env.COLOR == 'green' }
            }
            steps {
					sh '''
						cp green_index.html index.html
					'''
            }

		}

		stage('copy blue') {

            when {
                expression { env.COLOR == 'blue' }
            }
            steps {
					sh '''
						cp blue_index.html index.html
					'''
            }

		}

		stage('Docker Image Build') {
			steps {
				withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
					sh '''
						docker build -t rdaf16/api .
					'''
				}
			}
		}
		stage('Push Image To Dockerhub') {
			steps {
				withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
					sh '''
						docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
						docker push rdaf16/api
					'''
				}
			}
		}

		stage('Configure Kubernetes cluster') {
			steps {
				withAWS(region:'us-west-2', credentials:'aws-bg-kube-pipeline') {
					sh '''
						aws eks --region us-west-2 update-kubeconfig --name prod
					'''
				}
			}
		}
		stage('Set current kubectl context') {
			steps {
				withAWS(region:'us-west-2', credentials:'aws-bg-kube-pipeline') {
					sh '''
						kubectl config use-context arn:aws:eks:us-west-2:${env.AWS_ACCOUNT_ID}:cluster/prod
					'''
				}
			}
		}

		stage('Deploy container to cluster using green settings and redirect to it') {

            when {
                expression { env.COLOR == 'green' }
            }
            steps {
				withAWS(region:'us-west-2', credentials:'aws-bg-kube-pipeline') {
					sh '''
						kubectl apply -f ./green_controller.json
						kubectl apply -f ./green_service.json
					'''

				}
            }

		}
		stage('Deploy container to cluster using blue settings and redirect to it') {

            when {
                expression { env.COLOR == 'blue' }
            }
            steps {
				withAWS(region:'us-west-2', credentials:'aws-bg-kube-pipeline') {
					sh '''
						kubectl apply -f ./blue_controller.json
						kubectl apply -f ./blue_service.json
					'''
				}
            }

		}
		
	}
}

