import os
import pytest
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, os.getcwd())
from app import app
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'TEST'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<h1>Welcome to our server !!</h1>' in rv.data

def test_getmsg_empty(client):
    rv = client.get('/getmsg/')
    assert rv.status_code == 200
    assert b'{"ERROR":"no name found, please send a name."}' in rv.data

def test_getmsg_name(client):
    rv = client.get('getmsg/?name=Mark')
    assert rv.status_code == 200
    assert b'{"MESSAGE":"Welcome Mark to our awesome platform!!"}\n' in rv.data

def test_getmsg_numeric_name(client):
    rv = client.get('getmsg/?name=123')
    assert rv.status_code == 200
    assert b'{"ERROR":"name can\'t be numeric."}\n' in rv.data