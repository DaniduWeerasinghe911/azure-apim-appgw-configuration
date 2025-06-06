# Azure AD JWT validation for FastAPI
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os
import jwt

class AzureADBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AzureADBearer, self).__init__(auto_error=auto_error)
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.audience = os.getenv("AZURE_CLIENT_ID")
        self.jwks_uri = f"https://login.microsoftonline.com/{self.tenant_id}/discovery/v2.0/keys"
        self.jwks = requests.get(self.jwks_uri).json()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            try:
                token = credentials.credentials
                unverified_header = jwt.get_unverified_header(token)
                for key in self.jwks["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                        payload = jwt.decode(
                            token,
                            public_key,
                            algorithms=["RS256"],
                            audience=self.audience,
                            options={"verify_exp": True},
                        )
                        return payload
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token signature.")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token validation error: {str(e)}")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")
