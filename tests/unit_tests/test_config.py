import pytest
import json
import os
from utils.config import Config

def test_load_config():
    config = Config('tests/test_config.json')
    assert config.get('api_key') == 'test_api_key'
    assert config.get('db_uri') == 'test_db_uri'

def test_load_nonexistent_config():
    with pytest.raises(FileNotFoundError):
        Config('nonexistent_config.json')
