from conjur.config import config


def pytest_runtest_setup(item):
    config.url = 'http://possum.test'
