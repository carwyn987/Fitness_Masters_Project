# RESTFul API + Web Application

The goal of this folder is to create a web application and backend server to support the application requests.


## Sources
 - https://realpython.com/api-integration-in-python/

# Experimental Directory

This directory is responsible for containing files regarding the experimentation and construction of algorithms to further the projects mission statement.

## Installation

This project is implemented in python 3.7 and torch 1.13.0. Follow these steps to setup your environment:

1. [Download and install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html "Download and install Conda")
2. Create a Conda environment with Python 3.7
```
conda create -n hypertrophy-app python=3.7
```
3. Activate the Conda environment. You will need to activate the Conda environment in each terminal in which you want to use this code.
```
conda activate hypertrophy-app
```
4. Install the requirements:
```
pip3 install -r requirements.txt
```
<!-- 5. Install ipykernel for running ipynb files
```
conda install -n hypertrophy-app ipykernel --update-deps --force-reinstall
``` -->

```
pip install flask requests
conda install -c conda-forge uwsgi
pip install -U flask-cors
sudo apt install nodejs       #v12.22.9
sudo apt install npm          #8.5.1
```

5. Optional Installation:
```
sudo add-apt-repository ppa:wireshark-dev/stable
sudo apt-get update
sudo apt-get install wireshark
sudo wireshark
```

# To Run Application:

## To Start BackEnd:

By running the command:
```
uwsgi --http-socket 127.0.0.1:5683 --mount /=server:app
```
in the BackThe server will be started up to handle requests. Uwsgi starts up a web server with a single process and a single thread.

The server is likely hosted from the address / port combination: http://localhost:5683/

## To Start FrontEnd:

Run
```
npm start
```
In WebApp folder.

View web application at http://localhost:8080/index.html

Setup via instructions at https://www.section.io/engineering-education/static-site-dynamic-nodejs-web-app/ 