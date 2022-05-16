import os


def handler(event, context):
    version_to_test = os.getenv('NEW_VERSION')
    print(f'I should be testing version: {version_to_test}, but I don\'t have any code.....')
