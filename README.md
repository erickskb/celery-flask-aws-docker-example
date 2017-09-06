Celery-Flask-AWS-Docker Example
=======

This app is an example of a Celery application using Flask as its entry point.  For kicks it uses AWS resources as backing and deploys via Docker

Config
-----
To run the app locally, you need a a config file at /config/local_config.cfg.  This file should be in the format
specified in /config/local_config_template.txt. 

Gunicorn
-----
The Workflow Engine runs using Gunicorn as its WSGI server in production environments. Outside of Production,
Flask's builtin server is used for development and testing.  Gunicorn options can be passed in as environment variables.
See the Gunicorn docs for details.  

To run the app with Gunicorn locally for testing purposes:
```
gunicorn -w 1 -b 127.0.0.1:8080 --timeout 180 workflow_engine_gunicorn:app

```
Celery
-----
This app uses Celery for distributed asynchronous processing.  The Celery worker should be started independently from 
the application.  Activate your virtualenv in a terminal, navigate to the root of this project, and run 
```
python start_celery.py

```
Celery uses SQS as its queue and DynamoDB as its results store.  Both can be managed via the AWS Console or CLI.
  
pyCurl
-----
This app uses pyCurl, which has an odd installation process.  See the pyCurl docs for more info.  
Basically if you install via pip and then get this error:

```
ImportError: pycurl: libcurl link-time ssl backend (nss) is different from compile-time ssl backend (none/other)

```
then follow this recipe:
```
pip uninstall pycurl
export PYCURL_SSL_LIBRARY=nss
pip install pycurl  --no-cache-dir

```

Docker
-----
This app is designed to deploy via Docker.  To run Docker locally, follow the instructions found at https://docs.docker.com/get-started
To exercise the Docker image locally, follow these basic steps: 
1. Install Docker per above instructions
2. Run the Docker daemon: 
```
dockerd
```
3. Build: 
```
docker build -t 3pi-workflow:latest .
```
4. Run: 
```
docker run -d -p 8000:8000 3pi-workflow
```
5. Verify by doing a GET against http://localhost:8000/status

Note that sudo may be required for the above commands, depending on setup.
