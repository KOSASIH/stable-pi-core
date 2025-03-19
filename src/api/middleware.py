import time
import logging
from fastapi import Request, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from jwt import PyJWTError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("stable_pi_core.middleware")

# JWT Configuration
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start timing the request
        start_time = time.time()

        # Log request details
        logger.info(f"Request: {request.method} {request.url.path}")

        # Check for authentication token
        token = request.headers.get("Authorization")
        if not token:
            logger.warning("Unauthorized access attempt: No token provided.")
            raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

        # Verify the token
        try:
            payload = self.verify_token(token)
            request.state.user = payload  # Store user info in request state
        except PyJWTError:
            logger.warning("Unauthorized access attempt: Invalid token.")
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

        # Process the request and get response
        response: Response = await call_next(request)

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000  # in milliseconds

        # Add a custom header for performance monitoring
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        # Log response details
        logger.info(f"Response: status_code={response.status_code} processed_in={process_time:.2f}ms")

        return response

    def verify_token(self, token: str):
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

# Example of how to add the middleware to your FastAPI app
from fastapi import FastAPI

app = FastAPI()

# Add the custom middleware to your app
app.add_middleware(AuthMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello, Stable-Pi-Core with authentication and logging!"}

@app.get("/secure-data")
async def secure_data(request: Request):
    user = request.state.user  # Access user info from request state
    return {"message": f"Secure data accessed by user: {user['sub']}"}

# Function to create JWT token (for demonstration purposes)
def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Example usage of token creation (for testing purposes)
if __name__ == "__main__":
    test_user_data = {"sub": "test_user"}
    token = create_token(test_user_data)
    print(f"Generated Token: {token}")
