from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Return refresh and access tokens for given user using simplejwt helper.

    Using token generation directly avoids depending on cleartext passwords
    in tests and is faster than calling the token endpoint.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
