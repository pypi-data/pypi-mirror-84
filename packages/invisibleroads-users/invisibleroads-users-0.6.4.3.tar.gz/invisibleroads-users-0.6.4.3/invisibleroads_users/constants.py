from invisibleroads_macros_configuration import Settings
from invisibleroads_macros_log import get_log


DEFAULT_SECRET = 'ESwOdBHt5L6lRNLHLwsFVy6gjqFmlx6r5E9seaqlra4='


S = Settings({
    'mock': True,
    'storage': 'session',
    'cookie_secure': False,
    'cookie_httponly': True,
    'verify_tls': True,
    'auth_state_length': 64,
    'public_attributes': ['name', 'email', 'imageUrl'],
    'image_url': (
        'http://3.bp.blogspot.com/_D_Z-D2tzi14/TMkHEi7p6CI/AAAAAAAAEA4/'
        'UyhnLtpt4hM/s400/drunk11.png'),
    'secret': DEFAULT_SECRET,
    'default_permission': 'see',
    'require_csrf': True,
    'target_url': '/',
    'check_authorization': 'invisibleroads_users.routines.check_authorization',
    'redis.user_tickets.key': 'user.{user_id}.tickets',
})
L = get_log('invisibleroads-users')


INVISIBLEROADS_USERS_SETTINGS_PREFIX = 'invisibleroads_users.'


REDIS_SESSIONS_SETTINGS_PREFIX = 'redis.sessions.'
REDIS_SESSIONS_SECRET_LENGTH = 128
REDIS_SESSIONS_TIMEOUT_IN_SECONDS = 43200  # 12 hours
REDIS_SESSIONS_COOKIE_NAME = 's'
REDIS_SESSIONS_PREFIX = 'session.'


USER_DEFINITION = {
    'email': 'user@example.com',
}
DEFAULT_SECRET_ERROR_MESSAGE = f'''
\033[31m\033[5m\
!!! DEFAULT_SECRET is being used !!!\
\033[0m

python -c "
from miscreant.aes.siv import SIV
from base64 import b64encode
print(b64encode(SIV.generate_key()).decode('utf-8'))"

{INVISIBLEROADS_USERS_SETTINGS_PREFIX}secret = YOUR-SECRET
'''.strip()
