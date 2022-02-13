## Using the project in local environment

1. Clone the repository.
2. Run the following commands:

```bash
cd docker
cat >.env <<EOF
SECRET_KEY=9999
DEBUG=True
EOF
docker-compose up
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

3. Check if project is successfully running by going into `http://localhost:8001/admin/` or `http://localhost:8001/swagger/`.
4. To populate DB in local environment download dataset (a CSV file) from [here](http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv1) and place it inside root directory. Don't change its name. Run the following command:

```
docker-compose exec web python manage.py load_data
```

5. Due to the necessity to parse a CSV file with a size of ~4.6GB this process might take up to 10 hours. This is what it took on my machine.
6. After the process is complete (this can also be done while loading of data is still in progress) send `GET` requests to the `http://localhost:8001/api/v1/transactions/prices/` and `http://localhost:8001/api/v1/transactions/number/` (I pasted selected elements of Postman collection to make it easier to get familiar with those endpoints). Make sure that parameters sent in body of the request are in correct format (according to the schema below) as well that you provide correct TokenAuthentication credentials (refer to step 7 below):

```json
{
  "item": [
    {
      "name": "/transactions/prices",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Token a100c1059c3f103320c816df6661a0512dd1bdf3",
            "type": "text"
          }
        ],
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "location",
              "value": "SW18",
              "type": "text"
            },
            {
              "key": "from",
              "value": "2015-01",
              "type": "text"
            },
            {
              "key": "to",
              "value": "2015-12",
              "type": "text"
            }
          ]
        },
        "url": {
          "raw": "http://localhost:8001/api/v1/transactions/prices/"
        }
      }
    },
    {
      "name": "/transactions/number",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Token a100c1059c3f103320c816df6661a0512dd1bdf3",
            "type": "text"
          }
        ],
        "body": {
          "mode": "urlencoded",
          "urlencoded": [
            {
              "key": "date",
              "value": "2002-01",
              "type": "text"
            },
            {
              "key": "location",
              "value": "SW18",
              "type": "text"
            }
          ]
        },
        "url": {
          "raw": "http://localhost:8001/api/v1/transactions/number/"
        }
      }
    }
  ]
}
```

7. We are using Django Rest Framework's `TokenAuthentication`. In order to generate token necessary to send correct header within each request use following commnands:

```
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

## Main libraries used to build the project

- django
- djangorestframework
- pandas
- drf-yasg
- python-decouple
- psycopg2-binary
- dj-database-url

## API Documentation

API documentation is available at `http://localhost:8001/swagger/`. In order to view it you must be logged in. Go to `http://localhost:8001/admin/` and login to Django-Admin using the previously obtained credentials (the `createsuperuser` command).

It is a very basic documentation presenting examples of schema of response from each endpoint.

The in-built Django Rest Framework Browsable API is disabled.
