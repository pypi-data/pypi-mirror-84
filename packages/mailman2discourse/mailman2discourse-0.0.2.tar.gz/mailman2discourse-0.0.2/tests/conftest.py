import argparse
import pytest
import logging

for lib in ('urllib3', 'pydiscourse'):
    logger = logging.getLogger(lib)
    logger.setLevel(logging.WARNING)
    logger.propagate = False


@pytest.fixture
def test_options():
    api_key = open('discourse_docker/apikey').read().strip()
    ip = open('discourse_docker/ip').read().strip()
    url = f'http://{ip}'
    return argparse.Namespace(debug=True,
                              api_key=api_key,
                              api_user='api',
                              url=url,
                              mailman_encoding='UTF-8')
