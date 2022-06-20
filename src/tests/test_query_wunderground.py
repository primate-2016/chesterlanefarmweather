import pytest
import json
from unittest.mock import patch, MagicMock
from src.query_wunderground import get_current_weather


@patch('requests.request')
def test_get_current_weather(requests_get: MagicMock):
    '''
    Ensure we get the expected return format and that we are
    calling the current weather API with the right args
    '''

    requests_get.return_value.text = json.dumps({'some_key': 'some_value', 'errors':[]})
    response = get_current_weather()

    # the function returns the requests response.text object, so it should match the above return
    # exactly
    assert response == {'some_key': 'some_value', 'errors':[]}
    assert type(response) is dict
    requests_get.assert_called_once_with('GET', 'https://api.weather.com/v2/pws/observations/current', params={'stationId': None, 'format': 'json', 'units': 'h', 'apiKey': None})


@patch('requests.request')
def test_get_current_weather_bad_response(requests_get: MagicMock, caplog):
    '''
    Wunderground API doesn't return JSON if there is an error
    check that we handle this
    '''

    # make the call to requests return text rather than JSON
    requests_get.return_value.text = 'something has gone wrong'
    with pytest.raises(json.decoder.JSONDecodeError):
        get_current_weather()
    assert 'something has gone wrong' in caplog.text
