"""
Convenient tools that call gcloud or gsutil
or work with Google Cloud Platform
"""
import os
from IPython import get_ipython

sh = get_ipython().system

def config(project='kora-id'):
    os.system(f"gcloud config set project {project}")

def login():
    sh('gcloud auth login')

def list_projects():
    sh('gcloud projects list')

