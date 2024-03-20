# FERO.AI Ecommerce

## Index

- [FERO.AI](#FERO.AI)
  - [Index](#index)
    - [Introduction](#introduction)
    - [Installation](#installation)

### Introduction

- Build an e-commerce API using Django Rest Framework to manage
customers, orders, and products.
- No Authentication provided all apis are public.
- CRUD operations available.
- Filters available on Order Items.
- Supports latest version of Python i.e. Python 3.10.13 along with Django 4.1.11:

| Package | **Version** |
|--------|-------------|
| pip    | 23.2.1      |
| Python | 3.10.13     |
| Poetry | 1.4.2       |

### Installation

> ##### 1. Clone repository

```sh
git clone https://github.com/bhargavsonagara/fero-ecommerce.git
```

> ##### 2. If you not having pip, Django let's install

```sh
sudo easy_install pip
```

> ##### 3. Setup The Project

- Install poetry with python version (3.9 <= version < 3.11)

then run this command in your project terminal to install all dependancies using poetry

```sh
poetry install
```
Add .env file in the main DIR folder.

.env file contains the below necessary things to start project.

```sh
DB_NAME=DATABASE_NAME
DB_USER=DATABASE_USER
DB_PASSWORD=DATABASE_PASSWORD
DB_HOST=HOST_NAME
DB_PORT=PORT_NUMBER

SECRET_KEY=secretkey
DEBUG=True
SWAGGER_SERVER=http://127.0.0.1:8000/
```

Run this command in your project folder to activate your environment

```sh
poetry shell
```


> ##### 4. Create Database Manuanlly in PgAdmin

```sh
CREATE DATABASE <database_name>
```

> ##### 5. Setting up your database details and email config in .env

```sh
DB_NAME=DATABASE_NAME
DB_USER=DATABASE_USER
DB_PASSWORD=DATABASE_PASSWORD
DB_HOST=HOST_NAME
DB_PORT=PORT_NUMBER

```

> ##### 6. Create tables by Django migration

```sh
python manage.py makemigrations

python manage.py migrate
```

> ##### 7. All API available on @ `http://127.0.0.1:8000/api/`

```
customer create, list, update - http://127.0.0.1:8000/api/customers/
order list, create - http://127.0.0.1:8000/api/orders/
products list, create - http://127.0.0.1:8000/api/products/
```

> ##### 8. Swagger UI URL: http://127.0.0.1:8000/swagger-ui/

> ##### 9. Extra functionality

- Added drf spectacular for swagger generate Open API schema.
- Add coma seperated filter on orders.
<br />
