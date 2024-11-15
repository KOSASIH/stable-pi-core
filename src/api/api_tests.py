import pytest
from flask import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.data == b'Welcome to the Blockchain API!'

def test_mint_tokens(client):
    response = client.post('/mint', json={'recipient': '0xRecipientAddress', 'amount': 100})
   assert response.status_code == 200
    assert response.json['message'] == "Tokens minted successfully."

def test_burn_tokens(client):
    response = client.post('/burn', json={'amount': 50})
    assert response.status_code == 200
    assert response.json['message'] == "Tokens burned successfully."

def test_create_proposal(client):
    response = client.post('/create_proposal', json={'description': 'Increase token supply'})
    assert response.status_code == 200
    assert response.json['message'] == "Proposal created successfully."

def test_vote(client):
    response = client.post('/vote', json={'proposal_id': 1})
    assert response.status_code == 200
    assert response.json['message'] == "Vote cast successfully."

def test_execute_proposal(client):
    response = client.post('/execute_proposal', json={'proposal_id': 1})
    assert response.status_code == 200
    assert response.json['message'] == "Proposal executed successfully."
