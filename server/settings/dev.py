SECRET_KEY = '^@ggu(8q(b%+-2!i3er3n!#eck!3cl+n60($5!3&-r)u$h(xol'

DEBUG = True

ALLOWED_HOSTS = [
    '10.0.0.216', 
    '127.0.0.1', 
    'localhost', 
    'arcadeartbox-server.local',
    '10.0.0.241'
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost',
)

CSRF_TRUSTED_ORIGINS = (
    'http://localhost:3000',
    'http://localhost',
    'http://arcadeartbox-server.local'
)