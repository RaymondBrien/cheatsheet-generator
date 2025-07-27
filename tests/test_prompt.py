import dotenv
import pytest

def test_prompt_values():
    # TODO define some test cases
    # add a pyproject.toml file and config pytest to read from . and add test paths
    assert prompt is not None
    assert prompt.args is not "default"

def test_api_connection(env):
    """Should not be 401"""
    # TODO other test cases: prompt should never exceed limit, should catch before api call is ever sent. (num chars?)
    # assert all prompt class values are populated before being used in an API call
    
    # load env api key 
    # check still valid and http request (curl) does not fail

