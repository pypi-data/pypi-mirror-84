# version of localstack-ext
VERSION = '0.11.44.3'

# TODO: fix this. Also, not sure which timezone AWS uses - should be UTC, but there
# have been examples of AccessToken validation failure because of local time comparison
TOKEN_EXPIRY_SECONDS = 24 * 60 * 60

# name of Docker registry for Lambda images
DEFAULT_LAMBDA_DOCKER_REGISTRY = 'localstack/lambda'
