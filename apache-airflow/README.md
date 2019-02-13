### Overview 

This is a simple test environment for exercising Apache Airflow in A Jupyter Lab environemt.

It contains the example in the [Tutorial](https://airflow.apache.org/tutorial.html) with all of the commands in notebooks for ease of execution and annotation.

### Getting started

Install Docker & Docker Compose, latest ATOW Feb 2019.

`docker-compose up` 

Will start up the jupyter notebooks server and build the image with Airflow installed.

There are two folders which contain the files as follows

* `/books` - the notebooks which contain the commands.
* `/dags` - the dag definitons for Airflow


These will be mounted in the container in the appropriate places for Airflow and Jupyter to pick them up.

* `/books/AirflowExec.ipynb` contains the tutorial book
* `/books/AirflowUI.ipynb` contains the UI startup commands

Once started Jupyter is :

http://localhost:8888

If you start the AirflowUI in the workbook, it'll be here:

http://localhost:8080