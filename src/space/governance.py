import logging
from collections import defaultdict
from cryptography.fernet import Fernet
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GalacticGovernanceFramework:
    def __init__(self, quorum_percentage=0.6):
        """
        Initialize the Galactic Governance Framework.

        :param quorum_percentage: Minimum percentage of votes required for a proposal to be valid.
        """
        self.proposals = {}
        self.votes = defaultdict(list)
        self.key = Fernet.generate_key()  # Generate a key for encryption
        self.cipher = Fernet(self.key)
        self.quorum_percentage = quorum_percentage
        logging.info("Galactic Governance Framework initialized.")

    def create_proposal(self, proposal_id, description, proposer, expiration_time=3600):
        """
        Create a new governance proposal.

        :param proposal_id: Unique identifier for the proposal.
        :param description: Description of the proposal.
        :param proposer: The entity proposing the governance change.
        :param expiration_time: Time in seconds until the proposal expires.
        """
        if proposal_id in self.proposals:
            logging.error("Proposal ID already exists.")
            return False

        self.proposals[proposal_id] = {
            'description': description,
            'proposer': proposer,
            'votes_for': 0,
            'votes_against': 0,
            'status': 'pending',
            'expiration_time': time.time() + expiration_time
        }
        logging.info(f"Proposal created: {proposal_id} - {description} by {proposer}")
        return True

    def vote(self, proposal_id, voter, vote):
        """
        Cast a vote on a proposal.

        :param proposal_id: The ID of the proposal to vote on.
        :param voter: The entity casting the vote.
        :param vote: 'for' or 'against' the proposal.
        """
        if proposal_id not in self.proposals:
            logging.error("Proposal does not exist.")
            return False

        if time.time() > self.proposals[proposal_id]['expiration_time']:
            logging.error("Proposal has expired.")
            return False

        if vote not in ['for', 'against']:
            logging.error("Invalid vote. Must be 'for' or 'against'.")
            return False

        # Encrypt the vote for security
        encrypted_vote = self.cipher.encrypt(vote.encode('utf-8'))
        self.votes[proposal_id].append((voter, encrypted_vote))

        if vote == 'for':
            self.proposals[proposal_id]['votes_for'] += 1
        else:
            self.proposals[proposal_id]['votes_against'] += 1

        logging.info(f"Vote cast: {voter} voted {vote} on proposal {proposal_id}")
        return True

    def finalize_proposal(self, proposal_id):
        """
        Finalize a proposal after voting is complete.

        :param proposal_id: The ID of the proposal to finalize.
        :return: The result of the proposal.
        """
        if proposal_id not in self.proposals:
            logging.error("Proposal does not exist.")
            return None

        proposal = self.proposals[proposal_id]
        total_votes = proposal['votes_for'] + proposal['votes_against']
        if total_votes == 0:
            logging.error("No votes have been cast.")
            return None

        if total_votes < (self.quorum_percentage * (total_votes + 1)):
            proposal['status'] = 'quorum not reached'
            logging.info(f"Proposal {proposal_id} did not reach quorum.")
            return 'quorum not reached'

        if proposal['votes_for'] > proposal['votes_against']:
            proposal['status'] = 'approved'
            logging.info(f"Proposal {proposal_id} approved.")
            return 'approved'
        else:
            proposal['status'] = 'rejected'
            logging.info(f"Proposal {proposal_id} rejected.")
            return 'rejected'

    def get_proposal_status(self, proposal_id):
        """
        Get the status of a proposal.

        :param proposal_id: The ID of the proposal.
        :return: The status of the proposal.
        """
        if proposal_id in self.proposals:
            return self.proposals[proposal_id]['status']
        else:
            logging.error("Proposal does not exist.")
            return None

    def decrypt_votes(self, proposal_id):
        """
        Decrypt the votes for a proposal.

        :param proposal_id: The ID of the proposal.
        :return: List of decrypted votes.
        """
        if proposal_id not in self.votes:
            logging.error("No votes found for this proposal.")
            return []

        decrypted_votes = []
        for voter, encrypted_vote in self.votes[proposal_id]:
            decrypted_vote = self.cipher.decrypt(encrypted_vote).decode('utf-8')
            decrypted_votes.append((voter, decrypted_vote))
        return decrypted_votes

# Example usage
if __name__ == "__main__":
    governance = GalacticGovernanceFramework()

    # Create a proposal with a 1-hour expiration time
    governance.create_proposal("P001", "Establish a new colony on Mars", "Council of Elders", expiration_time=3600)

    # Cast votes
    governance.vote("P001", "Node_A", "for")
    governance.vote("P001", "Node_B", "against")
    governance.vote("P001", "Node_C", "for")

    # Finalize the proposal
    result = governance.finalize_proposal("P001")
    logging.info(f"Final result of proposal P001: {result}")

    # Get proposal status
    status = governance.get_proposal_status("P001")
    logging.info(f"Status of proposal P001: {status}")

    # Decrypt votes
    decrypted_votes = governance.decrypt_votes("P001")
    logging.info(f"Decrypted votes for proposal P001: {decrypted_votes}")

    # Attempt to vote on an expired proposal
    time.sleep(3601)  # Wait for the proposal to expire
    governance.vote("P001", "Node_D", "for")  # This should fail due to expiration
