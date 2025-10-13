from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from datetime import datetime, timedelta
from jose import jwt
import secrets
import uvicorn

# Simple in-memory storage
users_db = {
    "user@example.com": {
        "password": "password123",
        "name": "Demo User"
    }
}

auth_codes = {}
tokens = {}

SECRET_KEY = "your-secret-key-min-32-chars-long!!"
ALGORITHM = "HS256"

app = FastAPI()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "iss": "http://localhost:9000",
        "aud": "https://nonblinding-supermechanically-katina.ngrok-free.dev"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/oauth/authorize")
async def authorize(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    state: str = None,
    code_challenge: str = None,
    code_challenge_method: str = None,
    scope: str = None,
    resource: str = None  # ← Add resource parameter
):
    return HTMLResponse(f"""
    <html>
        <body>
            <h2>Login to Clappia MCP</h2>
            <form method="post" action="/oauth/authorize">
                <input type="hidden" name="client_id" value="{client_id}">
                <input type="hidden" name="redirect_uri" value="{redirect_uri}">
                <input type="hidden" name="response_type" value="{response_type}">
                <input type="hidden" name="state" value="{state or ''}">
                <input type="hidden" name="code_challenge" value="{code_challenge or ''}">
                <input type="hidden" name="code_challenge_method" value="{code_challenge_method or ''}">
                <input type="hidden" name="scope" value="{scope or ''}">
                <input type="hidden" name="resource" value="{resource or ''}">
                
                <label>Email: <input type="email" name="username" value="user@example.com"></label><br>
                <label>Password: <input type="password" name="password" value="password123"></label><br>
                <button type="submit">Login</button>
            </form>
            <p><small>Default: user@example.com / password123</small></p>
        </body>
    </html>
    """)

@app.post("/oauth/authorize")
async def authorize_post(
    username: str = Form(...),
    password: str = Form(...),
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    response_type: str = Form(...),
    state: str = Form(None),
    code_challenge: str = Form(None),
    code_challenge_method: str = Form(None),
    scope: str = Form(None),
    resource: str = Form(None)
):
    if username not in users_db or users_db[username]["password"] != password:
        raise HTTPException(400, "Invalid credentials")
    
    code = secrets.token_urlsafe(32)
    auth_codes[code] = {
        "username": username,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
        "scope": scope or "",
        "resource": resource,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    
    redirect_url = f"{redirect_uri}?code={code}"
    if state:
        redirect_url += f"&state={state}"
    
    return RedirectResponse(redirect_url, status_code=303) 

# ← NEW: Add GET handler for callback
@app.get("/auth/callback")
async def auth_callback_get(code: str, state: str):
    """Handle OAuth callback - just show success page"""
    return HTMLResponse("""
    <html>
        <body>
            <h2>✅ Authorization Successful!</h2>
            <p>You can close this window and return to your application.</p>
            <script>
                setTimeout(() => window.close(), 2000);
            </script>
        </body>
    </html>
    """)

@app.post("/oauth/token")
async def token(
    grant_type: str = Form(...),
    code: str = Form(None),
    redirect_uri: str = Form(None),
    client_id: str = Form(None),
    client_secret: str = Form(None),
    code_verifier: str = Form(None)
):
    if grant_type == "authorization_code":
        if code not in auth_codes:
            raise HTTPException(400, "Invalid authorization code")
        
        code_data = auth_codes[code]
        
        if datetime.utcnow() > code_data["expires"]:
            del auth_codes[code]
            raise HTTPException(400, "Authorization code expired")
        
        if code_data.get("code_challenge"):
            import hashlib
            import base64
            
            verifier_hash = base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            ).decode().rstrip('=')
            
            if verifier_hash != code_data["code_challenge"]:
                raise HTTPException(400, "Invalid code verifier")
        
        access_token = create_access_token({
            "sub": code_data["username"],
            "scope": code_data["scope"],
            "client_id": client_id
        })
        
        refresh_token = secrets.token_urlsafe(32)
        
        tokens[refresh_token] = {
            "username": code_data["username"],
            "client_id": client_id,
            "scope": code_data["scope"]
        }
        
        del auth_codes[code]
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token,
            "scope": code_data["scope"]
        }
    
    raise HTTPException(400, "Unsupported grant type")

@app.get("/.well-known/jwks.json")
async def jwks():
    return {"keys": []}

@app.get("/.well-known/oauth-authorization-server")
async def oauth_metadata():
    return {
        "issuer": "http://localhost:9000",
        "authorization_endpoint": "http://localhost:9000/oauth/authorize",
        "token_endpoint": "http://localhost:9000/oauth/token",
        "jwks_uri": "http://localhost:9000/.well-known/jwks.json",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["client_secret_post", "none"]
    }

if __name__ == "__main__":
    print("🔐 Starting Auth Server on http://localhost:9000")
    print("📧 Demo credentials: user@example.com / password123")
    uvicorn.run(app, host="0.0.0.0", port=9000)