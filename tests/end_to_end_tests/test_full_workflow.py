import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_full_workflow(client):
    # Step 1: Create a proposal
    response = client.post('/create_proposal', json={'description': 'Increase token supply'})
    assert response.status_code == 200

    # Step 2: Mint tokens
    response = client.post('/mint', json={'recipient': '0xRecipientAddress', 'amount': 100})
    assert response.status_code == 200

    # Step 3: Check balance
    response = client.get('/balance/0xRecipientAddress')
    assert response.status_code == 200
    assert response.json['balance'] == 100
