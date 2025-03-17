# src/generative_ai/dao_voting.py

import logging

# Set up logging for the DAO voting module
logger = logging.getLogger(__name__)

class DAOVoting:
    def __init__(self, voting_system):
        """
        Initialize the DAO Voting system.

        Parameters:
        - voting_system (str): The name of the voting system to be used (e.g., a smart contract address).
        """
        self.voting_system = voting_system
        self.proposals = []  # List to hold feature proposals
        logger.info(f"DAO Voting initialized with voting system: {self.voting_system}")

    def propose_feature(self, feature):
        """
        Propose a new feature for community voting.

        Parameters:
        - feature (str): The feature description to be proposed.

        Raises:
        - Exception: If the proposal fails.
        """
        try:
            logger.info(f"Proposing feature for voting: {feature}")
            proposal_id = len(self.proposals) + 1  # Simple ID generation
            self.proposals.append({
                'id': proposal_id,
                'feature': feature,
                'votes': {'yes': 0, 'no': 0}
            })
            logger.info(f"Feature proposed successfully with ID: {proposal_id}")
            return proposal_id
        except Exception as e:
            logger.error(f"Error proposing feature: {e}")
            raise

    def vote(self, proposal_id, user_vote):
        """
        Cast a vote on a feature proposal.

        Parameters:
        - proposal_id (int): The ID of the proposal to vote on.
        - user_vote (str): The user's vote ('yes' or 'no').

        Raises:
        - Exception: If the voting process fails.
        """
        try:
            logger.info(f"Casting vote for proposal ID {proposal_id}: {user_vote}")
            proposal = next((p for p in self.proposals if p['id'] == proposal_id), None)
            if proposal is None:
                logger.warning(f"Proposal ID {proposal_id} not found.")
                raise ValueError("Proposal not found.")

            if user_vote not in ['yes', 'no']:
                logger.warning("Invalid vote. Must be 'yes' or 'no'.")
                raise ValueError("Vote must be 'yes' or 'no'.")

            proposal['votes'][user_vote] += 1
            logger.info(f"Vote cast successfully for proposal ID {proposal_id}. Current votes: {proposal['votes']}")
        except Exception as e:
            logger.error(f"Error during voting process: {e}")
            raise

    def get_results(self, proposal_id):
        """
        Get the voting results for a specific proposal.

        Parameters:
        - proposal_id (int): The ID of the proposal to get results for.

        Returns:
        - dict: The voting results for the specified proposal.

        Raises:
        - Exception: If retrieving results fails.
        """
        try:
            logger.info(f"Retrieving results for proposal ID {proposal_id}")
            proposal = next((p for p in self.proposals if p['id'] == proposal_id), None)
            if proposal is None:
                logger.warning(f"Proposal ID {proposal_id} not found.")
                raise ValueError("Proposal not found.")

            logger.info(f"Results for proposal ID {proposal_id}: {proposal['votes']}")
            return proposal['votes']
        except Exception as e:
            logger.error(f"Error retrieving results: {e}")
            raise
