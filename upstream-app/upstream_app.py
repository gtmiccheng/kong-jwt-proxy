from fastapi import FastAPI, Request
import uvicorn
import base64
import json

def parse_jwt_payload(jwt_token):
    payload_b64 = jwt_token.split(".")[1]
    padded_payload = payload_b64 + "=" * (-len(payload_b64) % 4)
    decoded_bytes = base64.urlsafe_b64decode(padded_payload)

    return json.loads(decoded_bytes)

app = FastAPI(title="Upstream App - Header Inspector")

@app.get("/")
async def root(request: Request):
    headers = dict(request.headers)
    kong_headers = {k: v for k, v in headers.items() 
                    if k.lower().startswith("x-") or k.lower() == "authorization"}
    return {
        "endpoint": "/",
        "message": "Upstream App - Header Inspector",
        "all_headers": headers,
        "kong_injected_headers": kong_headers,
    }

@app.get("/api")
async def api_endpoint(request: Request):
    headers = dict(request.headers)
    
    auth = headers.get("authorization")
    jwt_payload = parse_jwt_payload(auth)
    
    kong_headers = {k: v for k, v in headers.items() 
                    if k.lower().startswith("x-") or k.lower() == "authorization"}
    
    return {
        "endpoint": "/api",
        "message": "Protected resource accessed",
        "authentication": {
            "authorization_present": auth is not None,
            "authorization": auth,
            "payload": jwt_payload
        },
        "kong_injected_headers": kong_headers,
        "all_headers": headers,
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/json")
async def json_response(request: Request):
    headers = dict(request.headers)
    kong_headers = {k: v for k, v in headers.items() 
                    if k.lower().startswith("x-") or k.lower() == "authorization"}
    return {
        "message": "JSON response from upstream",
        "all_headers": headers,
        "kong_injected_headers": kong_headers,
        "client_host": request.client.host if request.client else None,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)