Usage:
  
Clone repository

docker build -t webapp1 .
docker run -p 8000:8000 webapp1


go to http://127.0.0.1:8000/




create user:
requests.post('http://localhost:8000/user/', json={'name': 'Alice'})

create account for existing user:
requests.post('http://localhost:8000/user/1/account/', json={'name': 'basic account'})

create an address for existing user:
requests.post('http://localhost:8000/user/1/address/', json={'name': 'home address', 'content': 'address content'})

assign existing address to existing user:
requests.post('http://localhost:8000/user/1/assign_address/2/')

show database content:
requests.get('http://localhost:8000/').json()


Running tests:
docker run -e SQLALCHEMY_DATABASE_URL="sqlite:////tmp/db.sqlite3" webapp1 behave

or (inside running container):
 
docker ps | grep webapp
docker exec -t <CONTAINER_ID> /bin/bash
SQLALCHEMY_DATABASE_URL="sqlite:////tmp/db.sqlite3" behave
