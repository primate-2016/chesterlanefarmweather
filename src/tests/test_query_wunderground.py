import pytest
import requests
from unittest.mock import patch, MagicMock
from src.query_wunderground import get_current_weather


def test_get_current_weather():
    '''
    thing
    '''

    assert True




'''
@patch('requests.get')
def thing(requests_get: MagicMock):
    
    requests.get.return_value.text = json.dumps({'some_key': 'some_value', 'errors':[]})
    response = get_current_weather('https://thing', 'hfd')
    assert response == {'some_key': 'some_value', 'errors':[]}
    assert type(response) is dict
    requests_get.assert_called_once_with('https://thing, params={}, headers={})
'''