# IBM AI Enterprise Workflow Capstone
This is a time series prediction application for the IBM AI Enterprise Workflow Capstone project. 
The application utilized Facebook's Prophet algorithm, as well as datasets provided by the course.

This project contains 
* Unit tests for API, logging, and model
* run_tests.py for running all tests with a single script
* monitoring.py for performance monitoring
* teste_api.py validate endpoints API
* Baseline.ipynb for baseline model 
* EDA_data.ipynb for data analysis
* Model_Validation.ipynb model tuning
* dashboards_AVAAIL_POC.pbix Power BI - dashboard POC power BI with demand revenue forecast
* dashboard_poc.py Dash - dashboard  POC with demand revenue forecast

* export_postgresql.ipynb  example for export data for postgresql

* Docker deployment

Usage notes
===============

All commands are from this directory.

To test app.py
---------------------

    ~$ python app.py
    
To test the model directly
----------------------------

see the code at the bottom of `prophet_model.py`

    ~$ python prophet_model.py

To build the docker container
--------------------------------

    ~$ docker build --tag forecast_appIBM .

Check that the image is there.

    ~$ docker image ls
    
You may notice images that you no longer use. You may delete them with

    ~$ docker image rm IMAGE_ID_OR_NAME

And every once and a while if you want clean up you can

    ~$ docker system prune


Run the unittests
-------------------

Before running the unit tests launch the `app.py`.

To run only the api tests

    ~$ python unittests/ApiTests.py

To run only the model tests

    ~$ python unittests/ModelTests.py


To run all of the tests

    ~$ python run-tests.py

Run the container to test that it is working
----------------------------------------------    

    ~$ docker run -p 4000:8080 forecast_appIBM


