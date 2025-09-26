# **Wikidata SPARQL Data Retrieval and Visualization**

This project serves as a demonstration of a data pipeline for retrieving information from the Wikidata SPARQL endpoint, storing it within a MongoDB database using the Djongo framework, and presenting the results on a dynamic web page. The architecture is built on the Django framework, which provides a robust and scalable solution for managing web-based applications.


## **Prerequisites**

The project requires the following components to be installed and operational:

- **Python 3.8+**: The project requires a Python environment of version 3.8 or higher.

- **pip**: A Python package installer for managing project dependencies.

- **MongoDB**: A running instance of the MongoDB database is required for data persistence.


## **Project Setup**

The following steps outline the process for setting up the project environment.


### **1. Repository Cloning**

The initial step involves cloning the project repository from GitHub. This can be accomplished by executing the following command in a terminal:

git clone \[https\://github.com/your-username/wikidata-project.git]\(https\://github.com/your-username/wikidata-project.git)\
cd wikidata-project


### **2. Dependency Installation**

Subsequently, it is necessary to install the required Python dependencies. The djongo package facilitates the connection to MongoDB, while SPARQLWrapper is utilized for executing SPARQL queries.

    pip install django
    pip install django-extensions
    pip install djongo
    pip install sparqlwrapper


### **3. Database Configuration**

The database connection must be configured within the wikidata/settings.py file. The provided default settings are configured to connect to a local MongoDB instance. The database name can be customized as needed.

```bash
DATABASES = {\
    'default': {\
        'ENGINE': 'djongo',\
        'NAME': 'my\_django\_db',  # The name of the MongoDB database\
        'HOST': 'localhost',\
        'PORT': 27017,\
    }\
}
```


### **4. Migration Application**

The final setup step involves applying the database migrations. These two commands instruct the Django framework to create the necessary collections within the MongoDB database for data storage.

```bash
python manage.py makemigrations\
python manage.py migrate
```

## **Application Usage**

The application's functionality is divided into two primary operations: data retrieval and data presentation.


### **1. Data Retrieval and Storage**

This view is responsible for the data retrieval process. It connects to the Wikidata SPARQL endpoint, executes a specified query, and stores the resulting data in the project's MongoDB database. To initiate this process, the Django development server must be started.

```bash
python manage.py runserver
```

Then, navigate to the following URL in a web browser:

**https\://www\.google.com/search?q=http\://127.0.0.1:8000/data/fetch-data/**

A confirmation message will be displayed upon the successful completion of the operation.


### **2. Data Presentation**

Once the data has been successfully stored in the database, it can be viewed in a formatted table. This is achieved by navigating to the following URL in a web browser:

**https\://www\.google.com/search?q=http\://127.0.0.1:8000/data/display-data/**


### **Query Customization**

The current SPARQL query is configured to retrieve data on painters and their birth dates. The query logic, located in data\_app/views.py, can be modified to fetch different or more specific datasets from Wikidata.


## **Project Structure**

A brief overview of the project's directory structure is provided to facilitate navigation.

- **wikidata/**: This directory serves as the root for the main Django project.

- **data\_app/**: This is the Django application responsible for data handling operations.

- **data\_app/models.py**: This file defines the SparqlResult model, which maps to the MongoDB collection.

- **data\_app/views.py**: The view functions that handle data fetching, storage, and display are located here.

- **data\_app/urls.py**: This file defines the URL patterns specific to the data\_app.

- **data\_app/templates/**: The HTML templates used for rendering web pages are stored within this directory.


## **Potential Enhancements**

Potential areas for future development and enhancement include:

- Enabling the execution of user-inputted SPARQL queries.

- Implementing a pagination system to handle large datasets more efficiently.

- Improving the front-end design and user interface.

- Integrating robust error handling for network failures or invalid queries.
