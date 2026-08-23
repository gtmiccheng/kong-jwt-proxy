# Kong Gateway with JWT Authentication

A complete setup for Kong Gateway with JWT plugin for authentication.

## Quick Start

```bash
# Copy env file and customize (optional)
cp .env.example .env

# Start all services
docker-compose up -d

# Wait for Kong to be ready (check logs)
docker-compose logs -f kong
```

## Architecture

- **Kong Gateway** (port 8000) - API Gateway with JWT auth (DB-less mode)
- **Kong Admin API** (port 8001) - Management interface (read-only in DB-less)
- **Upstream App** (port 8080) - FastAPI app that inspects and displays all request headers

> **Note**: Running in DB-less mode - no PostgreSQL required. All config loaded from `kong.yml`.

## Testing

### 1. Generate JWT Token

```bash
# Install dependencies
pip install -r requirements.txt

# Generate token for app-user (valid 1 hour)
python generate_jwt.py app-user

# Generate token for admin-user (valid 24 hours)
python generate_jwt.py admin-user --expiry 24
```

### 2. Test Protected Endpoint

```bash
# Get token
TOKEN=$(python generate_jwt.py app-user)

# Call protected API through Kong
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api

# Without token (should return 401)
curl http://localhost:8000/api
```

### 3. Test Health Endpoint (No Auth)

```bash
curl http://localhost:8000/health
```

### 4. Inspect Headers Directly on Upstream

```bash
# Direct access to upstream (bypassing Kong)
curl http://localhost:8080/api

# JSON response with all headers
curl http://localhost:8080/json
```

## Upstream App Endpoints

All endpoints return JSON.

| Endpoint | Description |
|----------|-------------|
| `GET /` | JSON with all request headers + Kong-injected headers separated |
| `GET /api` | Protected resource - auth status + Kong headers + all headers |
| `GET /json` | JSON with all headers + client info |
| `GET /health` | Health check |

Response structure includes:
- `all_headers` - Complete request headers
- `kong_injected_headers` - Only headers added by Kong (X-*, Authorization)
- `authentication` - Parsed auth info (at `/api`)

## Kong Admin API

```bash
# List services
curl http://localhost:8001/services

# List routes
curl http://localhost:8001/routes

# List consumers
curl http://localhost:8001/consumers

# List plugins
curl http://localhost:8001/plugins
```

## Configuration Details

### JWT Plugin Config (`kong.yml`)

- **Key claim**: `iss` (issuer) - matches consumer's JWT key
- **Verified claims**: `exp` (expiration)
- **Algorithm**: HS256

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_USER_JWT_KEY` | `app-user-key` | JWT key (iss claim) for app-user |
| `APP_USER_JWT_SECRET` | `app-user-secret` | JWT secret for app-user |

Set via `.env` file or export in shell:
```bash
export APP_USER_JWT_SECRET="your-secure-secret"
docker-compose up -d
```

### Generating Secure JWT Secrets

**JWT Key (iss claim):** Any unique string identifier for the consumer
- Example: `my-app-prod`, `service-a`, `client-123`

**JWT Secret:** Cryptographically secure random string (256+ bits for HS256)
```bash
# Generate secure 256-bit secret for HS256
openssl rand -base64 32
```

**Example .env with generated secrets:**
```env
APP_USER_JWT_KEY=my-app-prod
APP_USER_JWT_SECRET=K7gNuZsE4bLp9qR2vX8yM3nB6cF1hJ5kL8pQ2wR4tY7uI9oP0aS3dF6gH8jK1l
ADMIN_USER_JWT_KEY=admin-service
ADMIN_USER_JWT_SECRET=X9mN2bV5cX8zL1kJ4hG7fD3sA6qW9eR2tY5uI8oP1aS4dF7gH0jK3lZ6xC9vB
```

> **Security Note**: The default secrets in `.env.example` are insecure. Always generate new secrets for production using `openssl rand -base64 32`. Never commit real secrets to version control.

### Consumers

| Username | Key (iss) | Secret |
|----------|-----------|--------|
| app-user | `${APP_USER_JWT_KEY}` | `${APP_USER_JWT_SECRET}` |

## Stop Services

```bash
docker-compose down
```