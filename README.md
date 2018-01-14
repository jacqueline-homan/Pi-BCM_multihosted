
# Installation

## Perquisites

### Packages

  * brew install libjpeg
  * brew install imagemagick
  * brew install epstool

### Redis

  * brew install redis
  * brew services start redis

### Postgres

  * brew install postgres
  * /usr/local/opt/postgresql/bin/createuser -s postgres


## Setup code

   * cd BCM_multihosted
   * virtualenv venv3 --python=python3
   * . ../venv3/bin/activate
   * pip install -r ../requirements/requirements_dev.txt

## Setup DB

   * python manage.py migrate

## Run app

   * python manage.py runserver
   * http://localhost:8000/API/v1/AccountCreateOrUpdate/
   
   
```
   UUID: 53900011
   email: 53900011@test.com
   Prefix: 53900011,53900012
   Txn Ref: Test_1,Test_3,Test_2 (optional)
   Credits: 39:20,43:100,44:100 (optional)
```

## Staging URLs

 - http://master-gs1ie.cpgoods.com
 - http://master-gs1ie.cpgoods.com/API/v1/AccountCreateOrUpdate/
 - http://master-gs1ie.cpgoods.com/admin_login/helpdesk@gs1ie.org/helpdesk_01
 - http://master-gs1ie.cpgoods.com/admin_login/marketing@gs1ie.org/marketing_01
## 
