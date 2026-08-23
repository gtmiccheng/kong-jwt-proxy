#!/usr/bin/env python3
"""
JWT Token Generator for Kong Gateway Testing
"""
import jwt
import datetime
import sys
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

CONSUMERS = {
    "app-user": {
        "key": os.getenv("APP_USER_JWT_KEY", "app-user-key"),
        "secret": os.getenv("APP_USER_JWT_SECRET", "app-user-secret")
    },
}

def generate_token(consumer: str, expiry_hours: int = 1) -> str:
    if consumer not in CONSUMERS:
        raise ValueError(f"Unknown consumer: {consumer}. Available: {list(CONSUMERS.keys())}")
    
    creds = CONSUMERS[consumer]
    payload = {
        "sub": "felix",
        "iss": creds["key"],
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=expiry_hours)
    }
    token = jwt.encode(payload, creds["secret"], algorithm="HS256")
    return token

def main():
    parser = argparse.ArgumentParser(description="Generate JWT tokens for Kong Gateway testing")
    parser.add_argument("consumer", choices=list(CONSUMERS.keys()), help="Consumer name")
    parser.add_argument("--expiry", "-e", type=int, default=1, help="Token expiry in hours")
    args = parser.parse_args()
    
    try:
        token = generate_token(args.consumer, args.expiry)
        print(token)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()