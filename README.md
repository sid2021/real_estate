# Accessing API running on HEROKU

Application is hosted Heroku. You can access it from the browser under those URLs:

- [Django-Admin](https://the-real-estate.herokuapp.com/admin/) (username `super`, password `super`)
- [Swagger docs](https://the-real-estate.herokuapp.com/swagger/) (make sure to login to Django-Admin before accessing this URL)

To query API use following endpoints (before that make sure to warm up the Heroku environment by accessing the Django Admin interface):

### `POST /transactions/prices/`

This endpoint returns data to generate a time series chart of avarage prices for the given postcode and between the given from and to dates.

Example request using `requests` library:

```python
import requests
import json

url = "https://the-real-estate.herokuapp.com/api/v1/transactions/prices/"

payload = json.dumps({
  "location": "L1",
  "from": "1999-01",
  "to": "1999-12"
})
headers = {
  'Authorization': 'Token a100c1059c3f103320c816df6661a0512dd1bdf3',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

Response:

```python
{"L1":{"D":{"1999-03-29":100000,"1999-04-16":120000},"S":{"1999-01-21":499995,"1999-01-22":26622,"1999-02-05":30000,"1999-03-30":47500,"1999-03-31":40000},"T":{"1999-03-31":60000,"1999-07-16":100000,"1999-10-27":47500,"1999-11-08":132500},"F":{"1999-03-12":49950,"1999-04-30":63000,"1999-05-28":51500,"1999-07-29":39500,"1999-10-19":62000,"1999-11-09":62000,"1999-11-11":94000,"1999-11-12":89000,"1999-11-22":98000,"1999-11-30":86000,"1999-12-06":105000,"1999-12-23":72000}}}
```

### `POST /transactions/numbers/`

This endpoint returns data to generate a histogram showing the number of transactions at various price brackets.

Example request using `requests` library.

```python
import requests
import json

url = "https://the-real-estate.herokuapp.com/api/v1/transactions/numbers/"

payload = json.dumps({
  "date": "2012-01",
  "location": "SW18"
})
headers = {
  'Authorization': 'Token a100c1059c3f103320c816df6661a0512dd1bdf3',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

Response:

```python
{"SW18":{"(1243750.0, 1610000.0]":1,"(142070.0, 511250.0]":60,"(2708750.0, 3075000.0]":2,"(511250.0, 877500.0]":27,"(877500.0, 1243750.0]":6}}
```

# Using the project in local environment

1. Clone the repository.
2. Run the following commands:

```bash
cd docker
docker-compose up
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

3. Check if project is successfully running by going into `http://localhost:8001/admin/` or `http://localhost:8001/swagger/`.
4. To populate DB in local environment download dataset (a CSV file) from [here](http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv1) and place it inside root directory. Don't change its name (`pp-complete.csv`). Run the following command:

```
docker-compose exec web python manage.py load_data
```

5. Due to the necessity to parse a CSV file with a size of ~4.6GB this process might take up to 10 hours. This is what it took on my machine.
6. After the process is complete (this can also be done while loading of data is still in progress) send `POST` requests to the `http://localhost:8001/api/v1/transactions/prices/` and `http://localhost:8001/api/v1/transactions/numbers/` endpoints using proper header and payload (refer to examples of API queries given above). Make sure that you provide correct TokenAuthentication credentials (refer to step 7 below):
7. We are using Django Rest Framework's `TokenAuthentication`. In order to generate token necessary to send correct header within each request use the following commnands:

```bash
docker-compose exec web python manage.py shell
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
u = get_user_model().objects.first()
token = Token.objects.create(user=u)
```

Copy the token obtained above to the authorization header which should look like that:

```
Authorization: Token a100c1059c3f103320c816df6661a0512dd1bdf3
```

## Running tests locally

```
cd docker
docker-compose run --rm web test
```

# Main libraries used to build the project

- django
- djangorestframework
- pandas
- drf-yasg
- python-decouple
- psycopg2-binary
- dj-database-url
- pip-tools
- whitenoise
- pytest

# API Documentation

API documentation is available at `http://localhost:8001/swagger/`. In order to view it you must be logged in. Go to `http://localhost:8001/admin/` and login to Django-Admin using the previously obtained credentials (the `createsuperuser` command).

It is a very basic documentation presenting examples of schema of response from each endpoint.

The in-built Django Rest Framework Browsable API is disabled.

# Production setup

Application is hosted on Heroku and is being deployed using Docker containers (config is stored in `heroku.yml`):

- Free `dyno` running `gunicorn`,
- PostgreSQL `Hobby Dev` tier (DB has ~**26 million** of rows and was imported to Heroku from Amazon S3 bucket (1.1GB dump file) after being initially seeded in local environment (using Django management command `load_data`)).
- Static files are served directly from Heroku using `whitenoise` package (while it might be not a good choice for larger apps in our case it's a totally feasible solution).

# API Performance

Due to the size of the dataset (~ 26 million of rows) querying for data spanning over long time ranges takes a considerable amount of time. To address it further steps would be required like:

- caching,
- scaling hardware (the project is hosted on `free` Heroku dyno),
- code improvements (e.g. using `pandas` dataframes in `/transactions/prices/` endpoint),
- pre-calculating common queries from frontend and storing their results in DB (so that we don't have to perform costly calculations for each request).
