import pytest
import os
from utils.logger import setup_logger

def test_logger_setup():
    log_file = 'test.log'
    logger = setup_logger('test_logger', log_file)
    logger.info('Testing logger setup.')
    
    assert os.path.exists(log_file)
    
    with open(log_file, 'r') as f:
        logs = f.readlines()
    
    assert len(logs) > 0
    assert 'Testing logger setup.' in logs[-1]
    
    os.remove(log_file)  # Clean up
