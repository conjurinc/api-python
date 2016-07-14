from conjur.config import config


def pytest_runtest_setup(item):
    config.appliance_url = 'https://example.com/api'
