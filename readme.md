## Test application for parsing hacker news.

#### How to start

To run all services:

    docker-compose -f /test_parser/docker-compose.yml up
    
To run tests:
    
    docker-compose -f /test_parser/docker-compose.yml run tests

### To run locally:

PostgreSQL and Redis should be up and running

At conf folder in .env file fill the required parameters:
    
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    REDIS_URL=

#### Install requirements:

    >> python3 -m venv <env_name>
    >> <env_name>/bin/activate
    >> pip install -r requirements
    # run migrations
    >> python manage.py migrate

#### Running services locally:
       
    # To run tests
    >> pytest -v
    
    # To run server
    >> python manage.py runserver
    
    # To run scheduler
    >> python manage.py articles_scheduler  
    
    # To run dramatiq
    >> python manage.py rundramatiq

#### Main routes:

/posts - GET

params:

    limit = valid values (0, 100) not required
    offset = valid values >=0 not required
    order = valid values ( id, url, title)
    order_direction = valid values (asc, desc)

/_srv/admin - admin panel

Default login/pass: mainadmin/admin

To fetch new posts use button "Refresh posts" located here _srv/admin/articles/article/

To change refresh rate change POSTS_CRON variable in docker_compose.yml or in .env file

Main app code is located here -> /apps/articles:
    
      /dto - data transfer object to simplify object transfer between app layers
      /management - manage.py commands
      /models - data structure + repository layer
      /services - services layer
      /tasks - dramatiq tasks
      /templates - admin templates
      views.py - rest api layer

 
