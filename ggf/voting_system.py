# ggf/voting_system.py

import logging
import time
import random

class VotingSystem:
    def __init__(self):
        """Initialize the Voting System."""
        self.proposals = {}
        self.votes = {}
        logging.info("Voting System initialized.")

    def propose(self, proposal_id, proposal_details):
        """
        Submit a new proposal.
        :param proposal_id: Unique identifier for the proposal.
        :param proposal_details: Details of the proposal.
        """
        if proposal_id in self.proposals:
            logging.warning(f"Proposal '{proposal_id}' already exists.")
            return
        
        self.proposals[proposal_id] = {
            "details": proposal_details,
            "votes": [],
            "status": "pending",
            "created_at": time.time()
        }
        logging.info(f"Proposal '{proposal_id}' submitted.")

    def vote(self, proposal_id, voter_id, vote):
        """
        Cast a vote on a proposal.
        :param proposal_id: Unique identifier for the proposal.
        :param voter_id: Identifier for the voter.
        :param vote: Vote value (e.g., True for yes, False for no).
        """
        if proposal_id not in self.proposals:
            logging.error(f"Proposal '{proposal_id}' not found.")
            return
        
        if voter_id in self.votes.get(proposal_id, []):
            logging.warning(f"Voter '{voter_id}' has already voted on proposal '{proposal_id}'.")
            return
        
        self.votes.setdefault(proposal_id, []).append({"voter_id": voter_id, "vote": vote})
        logging.info(f"Voter '{voter_id}' voted on proposal '{proposal_id}'.")

    def tally_votes(self, proposal_id):
        """
        Tally votes for a proposal.
        :param proposal_id: Unique identifier for the proposal.
        :return: Result of the voting.
        """
        if proposal_id not in self.proposals:
            logging.error(f"Proposal '{proposal_id}' not found.")
            return None
        
        votes = self.votes.get(proposal_id, [])
        yes_votes = sum(1 for v in votes if v["vote"] is True)
        no_votes = sum(1 for v in votes if v["vote"] is False)
        result = {
            "yes": yes_votes,
            "no": no_votes,
            "total": len(votes)
        }
        logging.info(f"Votes tallied for proposal '{proposal_id}': {result}")
        return result

    def decide(self, proposal_id, result):
        """
        Make a decision based on the voting result.
        :param proposal_id: Unique identifier for the proposal.
        :param result: Result of the voting.
        """
        if proposal_id not in self.proposals:
            logging.error(f"Proposal '{proposal_id}' not found.")
            return
        
        if result["yes"] > result["no"]:
            self.proposals[proposal_id]["status"] = "approved"
            logging.info(f"Proposal '{proposal_id}' approved.")
        else:
            self.proposals[proposal_id]["status"] = "rejected"
            logging.info(f"Proposal '{proposal_id}' rejected.")

    def get_proposal_status(self, proposal_id):
        """
        Get the status of a proposal.
        :param proposal_id: Unique identifier for the proposal.
        :return: Status of the proposal.
        """
        if proposal_id not in self.proposals:
            logging.error(f"Proposal '{proposal_id}' not found.")
            return None
        
        return self.proposals[proposal_id]["status"]

    def simulate_voting(self, proposal_id, num_voters):
        """
        Simulate voting on a proposal.
        :param proposal_id: Unique identifier for the proposal.
        :param num_voters: Number of voters to simulate.
        """
        for i in range(num_voters):
            voter_id = f"Voter-{i}"
            vote = random.choice([True, False])
            self.vote(proposal_id, voter_id, vote)

    def display_proposals(self):
        """
        Display all proposals.
        """
        logging.info("Proposals:")
        for proposal_id, proposal in self.proposals.items():
            logging.info(f"Proposal '{proposal_id}': {proposal['details']}")
