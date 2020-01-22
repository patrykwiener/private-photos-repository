# Private Photos Repository
A virtual time capsule providing a private photos repository. The application allows users to create their own set of memorable moments by uploading and widely describing the most precious images.

## Key Features
* Face recognition on a newly uploaded image
* Location where a picture was taken extracted from the image file
* Tag system allowing to find a group of images with similar content
* Image sharing system enabling the users to enjoy memories with their friends

## Site
### Repository Main Page
To enable filtering by tags or people click one of the bagdes.

![image](https://user-images.githubusercontent.com/22658583/72931381-064ab180-3d5e-11ea-85c3-14593999179e.png)

### Create Post
* Face recognition on upload
* Post description supporting Markdown language and emoji picker
* Custom tags
* GPS coordinates read from image file and marked on Google Maps

![image](https://user-images.githubusercontent.com/22658583/72933827-d0f49280-3d62-11ea-9785-67a4ef3f2b72.png)

### Post Details
Image post can be shared via e-mail of another user.

![image](https://user-images.githubusercontent.com/22658583/72933663-74917300-3d62-11ea-9920-82b948f5ea07.png)

### Sharing system
Also supports filtering.

#### Shared by User

![image](https://user-images.githubusercontent.com/22658583/72934795-90961400-3d64-11ea-8e5f-fe599d3647ff.png)

#### Shared with User

![image](https://user-images.githubusercontent.com/22658583/72934719-6d6b6480-3d64-11ea-853a-c75781f24b4d.png)

## Technologies
* [Python 3.6](https://www.python.org/downloads/)
* [Django 3.0.1](https://www.djangoproject.com/)
* [PostgreSQL 12.0](https://www.postgresql.org/)
* JavaScript/jQuery
* HTML5/CSS3
* [Bootstrap 4](https://getbootstrap.com/)

## Setup
You need to have installed:
* [Python 3.6](https://www.python.org/downloads/) or higher,
* [Visual C++ Build Tools](https://visualstudio.microsoft.com/downloads/),
* [PostgreSQL 12.0](https://www.postgresql.org/) or higher.

To setup database open SQL Shell (psql), login and type:

```sql
-- Create user
CREATE USER private_photos_repository WITH PASSWORD ’root’;

-- Create database
CREATE DATABASE sample_private_photos_repository OWNER private_photos_repository;
```

Clone or download the repo. From your command line pointing to the project root directory:

```bash
# Install virtualenv
$ pip install virtualenv

# Create virtual environment
$ virtualenv venv

# Activate environment
$ venv\Scripts\activate.bat

# Install requirements
$ pip install -r requirements.txt

# Migrate tabels
$ python manage.py migrate
```

To load sample data with default users `testuser` and `testadmin` with password `test` type:
```bash
$ python manage.py loaddata fixtures/sample_data.json
```

## Run server

To run server open command line pointing to the project root directory:

```bash
python manage.py runserver
```

You are now able to access `localhost:8000` in your browser.


## Tests

Implemented 86 unit tests validating:
* URL routing,
* Forms,
* Models,
* Views.

To run all tests type in command line pointing to the project root directory:

```bash
python manage.py test
```
## Contact
Created by [@patrykwiener](https://github.com/patrykwiener). 

Feel free to contact me on [My LinkedIn](https://www.linkedin.com/in/patryk-wiener-439074182/)!
