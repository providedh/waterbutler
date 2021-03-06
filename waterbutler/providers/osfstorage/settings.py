import hashlib

from waterbutler import settings

config = settings.child('OSFSTORAGE_PROVIDER_CONFIG')


FILE_PATH_PENDING = config.get('FILE_PATH_PENDING', '/tmp/pending')
FILE_PATH_COMPLETE = config.get('FILE_PATH_COMPLETE', '/tmp/complete')

RUN_TASKS = config.get_bool('RUN_TASKS', False)

HMAC_ALGORITHM = getattr(hashlib, config.get('HMAC_ALGORITHM', 'sha256'))

HMAC_SECRET = config.get_nullable('HMAC_SECRET', None)

if not settings.DEBUG:
    assert HMAC_SECRET, 'HMAC_SECRET must be specified when not in debug mode'
HMAC_SECRET = (HMAC_SECRET or 'changeme').encode('utf-8')

# Retry options
UPLOAD_RETRY_ATTEMPTS = int(config.get('UPLOAD_RETRY_ATTEMPTS', 1))
UPLOAD_RETRY_INIT_DELAY = int(config.get('UPLOAD_RETRY_INIT_DELAY', 30))
UPLOAD_RETRY_MAX_DELAY = int(config.get('UPLOAD_RETRY_MAX_DELAY', 60 * 60))
UPLOAD_RETRY_BACKOFF = int(config.get('UPLOAD_RETRY_BACKOFF', 2))
UPLOAD_RETRY_WARN_IDX = int(config.get('UPLOAD_RETRY_WARN_IDX', 5))

HOOK_RETRY_ATTEMPTS = int(config.get('HOOK_RETRY_ATTEMPTS ', 1))
HOOK_RETRY_INIT_DELAY = int(config.get('HOOK_RETRY_INIT_DELAY', 30))
HOOK_RETRY_MAX_DELAY = int(config.get('HOOK_RETRY_MAX_DELAY', 60 * 60))
HOOK_RETRY_BACKOFF = int(config.get('HOOK_RETRY_BACKOFF', 2))
HOOK_RETRY_WARN_IDX = config.get_nullable('HOOK_RETRY_WARN_IDX', None)

PARITY_RETRY_ATTEMPTS = int(config.get('PARITY_RETRY_ATTEMPTS', 1))
PARITY_RETRY_INIT_DELAY = int(config.get('PARITY_RETRY_INIT_DELAY', 30))
PARITY_RETRY_MAX_DELAY = int(config.get('PARITY_RETRY_MAX_DELAY', 60 * 60))
PARITY_RETRY_BACKOFF = int(config.get('PARITY_RETRY_BACKOFF', 2))
PARITY_RETRY_WARN_IDX = config.get_nullable('PARITY_RETRY_WARN_IDX', None)

# Parity options
PARITY_CONTAINER_NAME = config.get_nullable('PARITY_CONTAINER_NAME', None)
PARITY_REDUNDANCY = int(config.get('PARITY_REDUNDANCY', 5))
PARITY_PROVIDER_NAME = config.get('PARITY_PROVIDER_NAME', 'cloudfiles')
PARITY_PROVIDER_CREDENTIALS = config.get_object('PARITY_PROVIDER_CREDENTIALS', {})
PARITY_PROVIDER_SETTINGS = config.get_object('PARITY_PROVIDER_SETTINGS', {})

# POST-TASK CLEANUP OPTIONS
#
# Task cleanup happens after the tasks have successfully finished.  A chord is used to monitor
# the status of the tasks.  If either task fails, the chord will check on their status after
# waiting the interval set below.  Chord retries are linear, while task retries are exponential.
# It is possible for a task to succeed after the chord has given up.  In this case, the cleanup
# will not be run, and the temp dir will need to be cleaned manually.  This is not expected to
# happen frequently, so the default settings are arbitrary and simplisitic.  A more complex
# calculation involving the task backoff parameters defined above could be done, but will not be
# investigated until need is proven.

TASK_CLEANUP_MAX_RETRIES = int(config.get('TASK_CLEANUP_MAX_RETRIES', 10))
TASK_CLEANUP_INTERVAL = int(config.get('TASK_CLEANUP_INTERVAL', 60))
