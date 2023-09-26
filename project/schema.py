from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTScheme(OpenApiAuthenticationExtension):
    target_class = "dj_rest_auth.jwt_auth.JWTCookieAuthentication"
    name = "jwtAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token-based authentication with required prefix 'Bearer' -> `Authorization: Bearer <jwt-token>`",
        }
