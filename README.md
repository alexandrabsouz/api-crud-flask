
 API developed for an [`IZA.com.vc`](https://iza.com.vc/) Junior backend developer.
The api consists of a simple CRUD that contains database relationship types, GET, POST, PUT and DELETE, for registration of clients and their users.
<br><br><br><br>

<img src="https://github.com/alexandrabsouz/api-crud-flask/blob/main/img/flask_frasco.png" min-width="200px" max-width="300px" width="200px" align="center" alt="frasco img">
<br><br><br>

## Requirements

* [SQLAlchemy](https://docs.sqlalchemy.org/en/14/);
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/);
* [Flask_httpauth](https://flask-httpauth.readthedocs.io/en/latest/);
* [Python3-pip](https://pypi.org/project/pip/);


## Dependencies

* [Python](https://www.python.org/downloads/release/python-397/) - Programming language used;
* [Flask](https://flask.palletsprojects.com/en/2.0.x/) - Framework web used;



## Run API:

1 - Clone the repository:

```sh
$ git clone https://github.com/alexandrabsouz/api-crud-flask
$ cd api-crud-flask
```

2 - Create a virtual environment to install dependencies and activate it:

```sh
$ pip install python3-venv 
$ python -m venv venv 
$ source venv/bin/activate
```

3 - Install requirements:

```sh
(env)$ pip install -r dev-requirements.txt
```
Note the `(venv)` in front of the prompt. This shows that the virtual environment was created by `python3-venv`.

4 - Once `pip` has finished downloading dependencies:

    To migrate the database:
        ```sh
        (venv)$ flask db init    --> to init the db
        (venv)$ flask db migrate --> to migrate the db
        (venv)$ flask db upgrade --> to upgrade the db
        ```
    To run the application:
        ```sh
        (venv)$ flask run
        ```
5 - And browse by `http://localhost:5000/api/v1/`.


## Endpoints:

You will find all endpoint documentation at: [POSTMAN Documentation](https://documenter.getpostman.com/view/14862182/UUy3A7Re)


## Questions:

If in doubt, ask in the [Issue](https://github.com/alexandrabsouz/api-crud-flask/issues) section. In case of errors, post the reason and the log for a better response.


