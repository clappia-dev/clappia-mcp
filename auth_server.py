from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from datetime import datetime, timedelta
from jose import jwt
import secrets
import uvicorn
import hashlib
import base64

ISSUER = "https://clappia-auth.loca.lt"
AUDIENCE = "https://clappia-mcp.loca.lt"
SECRET_KEY = "your-secret-key-min-32-chars-long!!"
ALGORITHM = "HS256"

users_db = {"user@example.com": {"password": "password123", "name": "Demo User"}}
auth_codes = {}
tokens = {}

app = FastAPI()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": ISSUER,
        "aud": AUDIENCE
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_pkce(code_verifier: str, code_challenge: str) -> bool:
    verifier_hash = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return verifier_hash == code_challenge


async def handle_authorize_get(client_id, redirect_uri, response_type, state=None,
                               code_challenge=None, code_challenge_method=None,
                               scope=None, resource=None):
    if resource and resource.rstrip('/') != AUDIENCE.rstrip('/'):
        raise HTTPException(400, f"Invalid resource. Expected {AUDIENCE}")
    
    return HTMLResponse(f"""
    <html><head><title>Clappia MCP Login</title><style>
        body{{font-family:Arial;max-width:400px;margin:50px auto;padding:20px}}
        form{{background:#f5f5f5;padding:20px;border-radius:8px}}
        input{{width:100%;padding:8px;margin:5px 0 15px;border:1px solid #ddd;border-radius:4px}}
        button{{width:100%;padding:10px;background:#007bff;color:white;border:none;border-radius:4px;cursor:pointer}}
    </style></head><body>
        <h2>🔐 Clappia MCP Login</h2>
        <form method="post" action="/authorize">
            <input type="hidden" name="client_id" value="{client_id}">
            <input type="hidden" name="redirect_uri" value="{redirect_uri}">
            <input type="hidden" name="response_type" value="{response_type}">
            <input type="hidden" name="state" value="{state or ''}">
            <input type="hidden" name="code_challenge" value="{code_challenge or ''}">
            <input type="hidden" name="code_challenge_method" value="{code_challenge_method or ''}">
            <input type="hidden" name="scope" value="{scope or ''}">
            <input type="hidden" name="resource" value="{resource or ''}">
            <label>Email:</label><input type="email" name="username" value="user@example.com" required>
            <label>Password:</label><input type="password" name="password" value="password123" required>
            <button type="submit">Login</button>
        </form>
        <p style="text-align:center;color:#666;font-size:12px">Demo: user@example.com / password123</p>
    </body></html>
    """)


async def handle_authorize_post(username: str = Form(...), password: str = Form(...),
                                client_id: str = Form(...), redirect_uri: str = Form(...),
                                response_type: str = Form(...), state: str = Form(None),
                                code_challenge: str = Form(None),
                                code_challenge_method: str = Form(None),
                                scope: str = Form(None), resource: str = Form(None)):
    if username not in users_db or users_db[username]["password"] != password:
        raise HTTPException(400, "Invalid credentials")
    
    if code_challenge and code_challenge_method != "S256":
        raise HTTPException(400, "Only S256 supported")
    
    code = secrets.token_urlsafe(32)
    auth_codes[code] = {
        "username": username,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
        "scope": scope or "mcp:tools mcp:resources",
        "resource": resource or AUDIENCE,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    
    redirect_url = f"{redirect_uri}?code={code}"
    if state:
        redirect_url += f"&state={state}"
    return RedirectResponse(redirect_url, status_code=303)


@app.get("/authorize")
async def authorize(client_id: str, redirect_uri: str, response_type: str,
                   state: str = None, code_challenge: str = None,
                   code_challenge_method: str = None, scope: str = None,
                   resource: str = None):
    return await handle_authorize_get(client_id, redirect_uri, response_type,
                                     state, code_challenge, code_challenge_method,
                                     scope, resource)


@app.post("/authorize")
async def authorize_post(username: str = Form(...), password: str = Form(...),
                        client_id: str = Form(...), redirect_uri: str = Form(...),
                        response_type: str = Form(...), state: str = Form(None),
                        code_challenge: str = Form(None),
                        code_challenge_method: str = Form(None),
                        scope: str = Form(None), resource: str = Form(None)):
    return await handle_authorize_post(username, password, client_id, redirect_uri,
                                      response_type, state, code_challenge,
                                      code_challenge_method, scope, resource)


@app.get("/oauth/authorize")
async def authorize_legacy(client_id: str, redirect_uri: str, response_type: str,
                          state: str = None, code_challenge: str = None,
                          code_challenge_method: str = None, scope: str = None,
                          resource: str = None):
    return await handle_authorize_get(client_id, redirect_uri, response_type,
                                     state, code_challenge, code_challenge_method,
                                     scope, resource)


@app.post("/oauth/authorize")
async def authorize_post_legacy(username: str = Form(...), password: str = Form(...),
                               client_id: str = Form(...), redirect_uri: str = Form(...),
                               response_type: str = Form(...), state: str = Form(None),
                               code_challenge: str = Form(None),
                               code_challenge_method: str = Form(None),
                               scope: str = Form(None), resource: str = Form(None)):
    return await handle_authorize_post(username, password, client_id, redirect_uri,
                                      response_type, state, code_challenge,
                                      code_challenge_method, scope, resource)


async def handle_token(grant_type: str = Form(...), code: str = Form(None),
                      redirect_uri: str = Form(None), client_id: str = Form(None),
                      client_secret: str = Form(None), code_verifier: str = Form(None),
                      refresh_token: str = Form(None), resource: str = Form(None)):
    if grant_type == "authorization_code":
        if code not in auth_codes:
            raise HTTPException(400, "Invalid code")
        
        code_data = auth_codes[code]
        if datetime.utcnow() > code_data["expires"]:
            del auth_codes[code]
            raise HTTPException(400, "Code expired")
        
        if code_data.get("code_challenge"):
            if not code_verifier or not verify_pkce(code_verifier, code_data["code_challenge"]):
                raise HTTPException(400, "Invalid PKCE")
        
        if resource and resource.rstrip('/') != code_data.get("resource", "").rstrip('/'):
            raise HTTPException(400, "Resource mismatch")
        
        access_token = create_access_token({
            "sub": code_data["username"],
            "scope": code_data["scope"],
            "client_id": client_id
        })
        refresh_token_value = secrets.token_urlsafe(32)
        tokens[refresh_token_value] = {
            "username": code_data["username"],
            "client_id": client_id,
            "scope": code_data["scope"]
        }
        del auth_codes[code]
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token_value,
            "scope": code_data["scope"]
        }
    
    elif grant_type == "refresh_token":
        if refresh_token not in tokens:
            raise HTTPException(400, "Invalid refresh token")
        
        token_data = tokens[refresh_token]
        access_token = create_access_token({
            "sub": token_data["username"],
            "scope": token_data["scope"],
            "client_id": token_data["client_id"]
        })
        new_refresh = secrets.token_urlsafe(32)
        tokens[new_refresh] = token_data
        del tokens[refresh_token]
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": new_refresh,
            "scope": token_data["scope"]
        }
    
    raise HTTPException(400, "Unsupported grant")


@app.post("/token")
async def token(grant_type: str = Form(...), code: str = Form(None),
               redirect_uri: str = Form(None), client_id: str = Form(None),
               client_secret: str = Form(None), code_verifier: str = Form(None),
               refresh_token: str = Form(None), resource: str = Form(None)):
    return await handle_token(grant_type, code, redirect_uri, client_id,
                             client_secret, code_verifier, refresh_token, resource)


@app.post("/oauth/token")
async def token_legacy(grant_type: str = Form(...), code: str = Form(None),
                      redirect_uri: str = Form(None), client_id: str = Form(None),
                      client_secret: str = Form(None), code_verifier: str = Form(None),
                      refresh_token: str = Form(None), resource: str = Form(None)):
    return await handle_token(grant_type, code, redirect_uri, client_id,
                             client_secret, code_verifier, refresh_token, resource)


@app.get("/.well-known/oauth-authorization-server")
async def oauth_metadata(request: Request):
    return {
        "issuer": ISSUER,
        "authorization_endpoint": f"{ISSUER}/authorize",
        "token_endpoint": f"{ISSUER}/token",
        "registration_endpoint": f"{ISSUER}/register",
        "jwks_uri": f"{ISSUER}/.well-known/jwks.json",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["none"],
        "scopes_supported": ["mcp:tools", "mcp:resources"],
    }


@app.get("/.well-known/jwks.json")
async def jwks():
    return {"keys": []}


@app.post("/register")
async def register_client(request: Request):
    body = await request.json()
    client_id = f"client_{secrets.token_urlsafe(16)}"
    return {
        "client_id": client_id,
        "client_name": body.get("client_name", "MCP Client"),
        "redirect_uris": body.get("redirect_uris", []),
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }


if __name__ == "__main__":
    print(f"Auth Server: {ISSUER}")
    print(f"For MCP: {AUDIENCE}")
    print(f"Login: user@example.com / password123")
    uvicorn.run(app, host="0.0.0.0", port=9000)