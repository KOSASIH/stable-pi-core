# tests/test_generative_ai/test_dao_voting.py

import unittest
from src.generative_ai.dao_voting import DAOVoting

class TestDAOVoting(unittest.TestCase):
    def setUp(self):
        """Set up the DAOVoting instance for testing."""
        self.voting_system = "dummy_voting_system"
        self.dao_voting = DAOVoting(voting_system=self.voting_system)

    def test_propose_feature(self):
        """Test the feature proposal functionality."""
        feature = "New AI-driven analytics"
        
        # Propose a feature
        proposal_id = self.dao_voting.propose_feature(feature)
        
        # Assert that the proposal was added correctly
        self.assertEqual(len(self.dao_voting.proposals), 1)
        self.assertEqual(self.dao_voting.proposals[0]['feature'], feature)
        self.assertEqual(self.dao_voting.proposals[0]['votes'], {'yes': 0, 'no': 0})
        self.assertEqual(proposal_id, 1)  # Check that the proposal ID is correct

    def test_vote(self):
        """Test the voting functionality."""
        feature = "New AI-driven analytics"
        proposal_id = self.dao_voting.propose_feature(feature)
        
        # Cast a vote
        self.dao_voting.vote(proposal_id, 'yes')
        
        # Assert that the vote was counted correctly
        self.assertEqual(self.dao_voting.proposals[0]['votes']['yes'], 1)
        self.assertEqual(self.dao_voting.proposals[0]['votes']['no'], 0)

    def test_vote_invalid_proposal(self):
        """Test voting on a non-existent proposal."""
        with self.assertRaises(ValueError) as context:
            self.dao_voting.vote(999, 'yes')  # Non-existent proposal ID
        self.assertEqual(str(context.exception), "Proposal not found.")

    def test_vote_invalid_choice(self):
        """Test voting with an invalid choice."""
        feature = "New AI-driven analytics"
        proposal_id = self.dao_voting.propose_feature(feature)
        
        with self.assertRaises(ValueError) as context:
            self.dao_voting.vote(proposal_id, 'maybe')  # Invalid vote choice
        self.assertEqual(str(context.exception), "Vote must be 'yes' or 'no'.")

    def test_get_results(self):
        """Test retrieving voting results for a proposal."""
        feature = "New AI-driven analytics"
        proposal_id = self.dao_voting.propose_feature(feature)
        
        # Cast some votes
        self.dao_voting.vote(proposal_id, 'yes')
        self.dao_voting.vote(proposal_id, 'no')
        
        # Get results
        results = self.dao_voting.get_results(proposal_id)
        
        # Assert that the results are correct
        self.assertEqual(results, {'yes': 1, 'no': 1})

    def test_get_results_invalid_proposal(self):
        """Test getting results for a non-existent proposal."""
        with self.assertRaises(ValueError) as context:
            self.dao_voting.get_results(999)  # Non-existent proposal ID
        self.assertEqual(str(context.exception), "Proposal not found.")

if __name__ == '__main__':
    unittest.main()
