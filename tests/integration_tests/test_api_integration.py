import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_mint_tokens_integration(client):
    response = client.post('/mint', json={'recipient': '0xRecipientAddress', 'amount': 100})
    assert response.status_code == 200
    assert response.json['message'] == "Tokens minted successfully."

def test_create_proposal_integration(client):
    response = client.post('/create_proposal', json={'description': 'Increase token supply'})
    assert response.status_code == 200
    assert response.json['message'] == "Proposal created successfully."
