## House Intelligent Appraiser Project

This project demonstrates how to operationalize an API using a Blue-Green CI/CD Jenkins pipeline deploying to a Docker containers in a Kubernetes pod. It implements the microservice API architecture to interact with a pre-trained machine learning model predicting the price of houses in the Boston, MA market.

The `sklearn` model has been trained to predict housing prices in Boston according to several features, such as average rooms in a home and data about highway access, teacher-to-pupil ratios, and so on. You can read more about the data, which was initially taken from Kaggle, on [the data source site](https://www.kaggle.com/c/boston-housing).

This project could be extended to any pre-trained machine learning model, such as those for image recognition and data labeling.

## TL;DR

You will need an AWS account to run project:

* Create an ec2 instance
* install Jenkins
* install `Pipeline AWS: steps` and `Blue Ocean` plugins for jenkins
* install eksctl, docker, kubernetes, hadolint and pylint
* Create a dockerhub account
* Add the dockerhub credentials to Jenkins global credentials with id `dockerhub`
* Create both AWS IAM User and Role with the necessary permissions to create an EKS cluster and nodegroup
* Attach the role to the Jenkins server and add the IAM user credentials to Jenkins global credentials with id `aws-bg-kube-pipeline`
* In ec2, select the Oregon region, us-west-2, and create a ppk called `bg-pipeline`
* ssh into the server
* run the following command `eksctl create cluster --name prod --version 1.16 --region us-west-2 --nodegroup-name standard-workers --node-type t2.micro --nodes 1 --nodes-min 1 --nodes-max 1 --ssh-access --ssh-public-key bg-pipeline --managed`
* The command above takes about 15 minutes to run. You can navigate to CloudFormation to see all the resources it creates.
* Fork this repository to your Github Account
* Create a new pipeline in Blue Ocean and point it to this repository
* Trigger a build to deploy the `green` container with its environment settings
* Once the build is complete, run the following command from the terminal to get the URL of the Load Balancer `kubectl get all`
* Navigate to that URL to see an SPA with a green background
* Checkout the code
* in `Jenkinsfile`, update the COLOR environment variable from `green` to `blue`, commit and push to Github
* Trigger another run in Jenkins 
* Once the run is complete, refresh the your browser and this time the background will be blue


## What You're Getting
```bash
├── CONTRIBUTING.md
├── README.md
├── Dockerfile
├── Jenkinsfile
├── app.py # the API for querying the model, it uses Flask 
├── blue_controller.json # Kubernetes ReplicationController settings for the blue environment
├── blue_index.html
├── blue_service.json # LoadBalancer settings for the blue environment
├── green_controller.json # Kubernetes ReplicationController settings for the green environment
├── green_index.html
├── green_service.json # LoadBalancer settings for the green environment
├── requirements.txt # Python dependencies to be installed in each container via pip
├── model_data
    ├── boston_housing_prediction.joblib
    └── housing.csv
```

## Contributing

Do not hesitate to submit a pull request.

For details, check out [CONTRIBUTING.md](CONTRIBUTING.md).

