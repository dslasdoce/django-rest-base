# Installation
Install postgres
```
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

Install conda then create python env
```
conda create env -n env-name python==3.9
```

Install python requirements
```
pip install -r requirements.txt
```

# Local Development
## For Terminal Users
```
    conda activate env-name
    python manage.py migrate
    python manage.py runserver localhost:8080
```

# Deployment
## Google Cloud Run
* Visit https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build#new-service for instructions on how to start cloud run using DockerFile
* Make sure to select the gcloud_services/cloudbuild.yaml on your cloud build trigger settings
* To connect cloud run to cloud sql then make sure to add the SQL Client or SQL Admin role to the IAM Permission of projectID--compute@developer.gserviceaccount.com. Also Under Cloud Run connections, make sure the target Database is properly added
   * For sample django project you may visit https://cloud.google.com/python/django/run#cloning_the_django_app 
# GCloud SQL
To connect to sql server on gcloud using your local machine
1. Get the service account json file from devops admin
2. Go to gcloud_services dir
3. Start the sql_proxy_run script
4. Connect using the following options
    * DB_USER: postgres
    * DB_HOST: localhost
    * DB_PORT: 5480
    * DB_PASSWORD
    

# AWS ECS 
1. Create a container repository in Elastic Container Registry
2. Create a load balancer target group with port 80 
3. Create load balancer
4. Add listener to load balancer
    4.1. add listener to port 80 and forward to the target group
5. Create a task definition (use Fargate)
    5.1 Make sure to add the target container
6. go to the task definition then create a service
    5.1. When selecting the port mapping and load balancer, make sure to
         select the ones created in previous steps


# AWS Code Pipeline
1. Finish ECS Deployment
2. Create pipeline for every deployment branch(dev, staging, production)
3. In Deploy stage of pipeline, make sure to deploy to ALL services (api, worker, scheduler)
