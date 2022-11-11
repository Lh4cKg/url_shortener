from uuid import uuid4
from collections import namedtuple
from datetime import timedelta

import jwt
from jwt import InvalidAlgorithmError, InvalidTokenError
from django.conf import settings
from django.utils import timezone

from apps.utils import datetime_from_epoch, datetime_to_epoch
from .exceptions import TokenError, TokenBackendError


JwtSettings = namedtuple('JwtSettings', [
    'ALGORITHM', 'VERIFYING_KEY', 'AUDIENCE',
    'ISSUER', 'SECRET', 'ACCESS_TOKEN_LIFETIME',
    'AUTH_HEADER_TYPES', 'AUTH_TOKEN_CLASSES',
    'USER_ID_CLAIM', 'USER_ID_FIELD', 'TOKEN_TYPE_CLAIM',
    'JTI_CLAIM', 'LEEWAY', 'JSON_ENCODER'
])
jwt_settings = JwtSettings(**settings.JWT)


class TokenBackend:
    def __init__(self, algorithm, signing_key=None, verifying_key='',
                 audience=None, issuer=None, leeway=None, json_encoder=None):
        self.algorithm = algorithm
        self.signing_key = signing_key
        self.verifying_key = verifying_key
        self.audience = audience
        self.issuer = issuer
        self.leeway = leeway
        self.json_encoder = json_encoder

    def get_leeway(self):
        if self.leeway is None:
            return timedelta(seconds=0)
        elif isinstance(self.leeway, (int, float)):
            return timedelta(seconds=self.leeway)
        elif isinstance(self.leeway, timedelta):
            return self.leeway
        else:
            raise TokenBackendError(
                f"Unrecognized type '{type(self.leeway)}', "
                f"'leeway' must be of type int, float or timedelta."
            )

    def get_verifying_key(self):
        if self.algorithm.startswith('HS'):
            return self.signing_key

        return self.verifying_key

    def encode(self, payload):
        """
        Returns an encoded token for the given payload
        """
        jwt_payload = payload.copy()
        if self.audience is not None:
            jwt_payload['aud'] = self.audience
        if self.issuer is not None:
            jwt_payload['iss'] = self.issuer

        token = jwt.encode(
            jwt_payload,
            self.signing_key,
            algorithm=self.algorithm,
            json_encoder=self.json_encoder,
        )
        return token

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token
        """
        try:
            return jwt.decode(
                token,
                self.get_verifying_key(),
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                leeway=self.get_leeway(),
                options={
                    'verify_aud': self.audience is not None,
                    'verify_signature': verify,
                },
            )
        except InvalidAlgorithmError as ex:
            raise TokenBackendError('Invalid algorithm specified') from ex
        except InvalidTokenError:
            raise TokenBackendError('Token is invalid or expired')


class Token:
    token_type = None
    lifetime = None

    def __init__(self, token=None, verify=True, lifetime=None):
        if lifetime and isinstance(lifetime, int):
            self.lifetime = timedelta(days=lifetime)
        if self.token_type is None or self.lifetime is None:
            raise TokenError('Cannot create token with no type or lifetime')
        self.token = token
        self.current_time = timezone.now()
        if token is not None:
            token_backend = self.get_token_backend()
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except TokenBackendError:
                raise TokenError('Token is invalid or expired')

            if verify:
                self.verify()
        else:
            self.payload = {jwt_settings.TOKEN_TYPE_CLAIM: self.token_type}
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)
            self.set_jti()

    def __repr__(self):
        return repr(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def __str__(self):
        return self.get_token_backend().encode(self.payload)

    def verify(self):
        self.check_exp()
        if (
            jwt_settings.JTI_CLAIM is not None
            and jwt_settings.JTI_CLAIM not in self.payload
        ):
            raise TokenError('Token has no id')

        if jwt_settings.TOKEN_TYPE_CLAIM is not None:
            self.verify_token_type()

    def verify_token_type(self):
        try:
            token_type = self.payload[jwt_settings.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise TokenError('Token has no type')

        if self.token_type != token_type:
            raise TokenError('Token has wrong type')

    def set_jti(self):
        self.payload[jwt_settings.JTI_CLAIM] = uuid4().hex

    def set_exp(self, claim='exp', from_time=None, lifetime=None):
        if from_time is None:
            from_time = self.current_time

        if lifetime is None:
            lifetime = self.lifetime

        self.payload[claim] = datetime_to_epoch(from_time + lifetime)

    def set_iat(self, claim='iat', at_time=None):
        if at_time is None:
            at_time = self.current_time

        self.payload[claim] = datetime_to_epoch(at_time)

    def check_exp(self, claim='exp', current_time=None):
        if current_time is None:
            current_time = self.current_time
        try:
            claim_value = self.payload[claim]
        except KeyError:
            raise TokenError(f"Token has no '{claim}' claim")
        claim_time = datetime_from_epoch(claim_value)
        leeway = self.get_token_backend().get_leeway()
        if claim_time <= current_time - leeway:
            raise TokenError(f"Token '{claim}' claim has expired")

    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user
        """
        user_id = getattr(user, jwt_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[jwt_settings.USER_ID_CLAIM] = user_id

        return token

    @staticmethod
    def get_token_backend():
        token_backend = TokenBackend(
            jwt_settings.ALGORITHM,
            jwt_settings.SECRET,
            jwt_settings.VERIFYING_KEY,
            jwt_settings.AUDIENCE,
            jwt_settings.ISSUER,
            jwt_settings.LEEWAY,
            jwt_settings.JSON_ENCODER,
        )
        return token_backend


class AccessToken(Token):
    token_type = 'access'
    lifetime = jwt_settings.ACCESS_TOKEN_LIFETIME
