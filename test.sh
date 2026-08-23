#!/bin/bash

TOKEN=$(python3 ./jwt/generate_jwt.py --expiry 1 app-user)
curl -v -H "Authorization: Bearer $TOKEN" http://localhost:8000/api | jq