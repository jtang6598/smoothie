# Requires mock server set up on localhost:3000
# Try out Mockoon for this: https://github.com/mockoon/mockoon
# They even provide sample responses for each API: https://github.com/mockoon/mock-samples

from settings.prod import SPOTIFY_AUTH_API


SPOTIFY_WEB_API = "http://localhost:3000/v1"
SPOTIFY_AUTH_API = "http://localhost:3000/v1/auth"

