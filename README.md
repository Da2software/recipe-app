# RECIPE APP (WIP)
This project is focused on improving my skills with GraphQL and FastAPI.

## API
there are two APIs that we need to start recipes_api and users_api, each one requires a python environment, you will need to run the next commands to setup the environment.
>required python 3.10.10+

```bash
# inside recipes_api/ or users_api/
# creating the environment
python -m venv venv

# starting the environment
source venv/bin/activate # for linux
# or
venv\Scripts\activate    # for windows
```

## Databases in DEV mode
### users_api databases
for dev mode I'm using SQLite, no configuration needed.

### recipes_api databases
> required docker
install the mongodb using the next command
```bash
docker pull mongodb/mongodb-community-server:latest
```
then we can run the container
```bash
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:5.0-ubuntu2004
```