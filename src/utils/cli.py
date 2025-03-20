import argparse
import json
import requests
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API URL from environment variable or default to localhost
API_URL = os.getenv("API_URL", "http://localhost:5000/proposals")

def create_proposal(proposal_id, description, proposer, expiration_time):
    data = {
        "proposal_id": proposal_id,
        "description": description,
        "proposer": proposer,
        "expiration_time": expiration_time
    }
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        logging.info("Proposal created successfully.")
        print(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error creating proposal: {e}")
        print(f"Error: {e}")

def vote(proposal_id, voter, vote):
    data = {
        "voter": voter,
        "vote": vote
    }
    try:
        response = requests.post(f"{API_URL}/{proposal_id}/vote", json=data)
        response.raise_for_status()
        logging.info(f"Vote cast successfully by {voter}.")
        print(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error voting on proposal: {e}")
        print(f"Error: {e}")

def finalize_proposal(proposal_id):
    try:
        response = requests.post(f"{API_URL}/{proposal_id}/finalize")
        response.raise_for_status()
        logging.info("Proposal finalized successfully.")
        print(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error finalizing proposal: {e}")
        print(f"Error: {e}")

def get_proposal_status(proposal_id):
    try:
        response = requests.get(f"{API_URL}/{proposal_id}/status")
        response.raise_for_status()
        logging.info("Proposal status retrieved successfully.")
        print(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving proposal status: {e}")
        print(f"Error: {e}")

def get_votes(proposal_id):
    try:
        response = requests.get(f"{API_URL}/{proposal_id}/votes")
        response.raise_for_status()
        logging.info("Votes retrieved successfully.")
        print(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving votes: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Galactic Governance CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Create proposal command
    create_parser = subparsers.add_parser('create', help='Create a new proposal')
    create_parser.add_argument('proposal_id', type=str, help='Unique proposal ID')
    create_parser.add_argument('description', type=str, help='Proposal description')
    create_parser.add_argument('proposer', type=str, help='Proposer name')
    create_parser.add_argument('--expiration_time', type=int, default=3600, help='Expiration time in seconds')

    # Vote command
    vote_parser = subparsers.add_parser('vote', help='Vote on a proposal')
    vote_parser.add_argument('proposal_id', type=str, help='Proposal ID to vote on')
    vote_parser.add_argument('voter', type=str, help='Voter name')
    vote_parser.add_argument('vote', type=str, choices=['for', 'against'], help='Vote choice')

    # Finalize proposal command
    finalize_parser = subparsers.add_parser('finalize', help='Finalize a proposal')
    finalize_parser.add_argument('proposal_id', type=str, help='Proposal ID to finalize')

    # Get proposal status command
    status_parser = subparsers.add_parser('status', help='Get the status of a proposal')
    status_parser.add_argument('proposal_id', type=str, help='Proposal ID to check status')

    # Get votes command
    votes_parser = subparsers .add_parser('votes', help='Get votes for a proposal')
    votes_parser.add_argument('proposal_id', type=str, help='Proposal ID to get votes for')

    args = parser.parse_args()

    if args.command == 'create':
        create_proposal(args.proposal_id, args.description, args.proposer, args.expiration_time)
    elif args.command == 'vote':
        vote(args.proposal_id, args.voter, args.vote)
    elif args.command == 'finalize':
        finalize_proposal(args.proposal_id)
    elif args.command == 'status':
        get_proposal_status(args.proposal_id)
    elif args.command == 'votes':
        get_votes(args.proposal_id)

if __name__ == '__main__':
    main()
