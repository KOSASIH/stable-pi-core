# api/api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from wdb.logger import AsyncLogger

class API:
    def __init__(self):
        self.app = FastAPI()
        self.logger = AsyncLogger()

        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow all origins for simplicity; adjust as needed
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Include routes
        self.app.include_router(router)

    async def log_request(self, request):
        await self.logger.log('INFO', f"Request: {request.method} {request.url}")

    async def log_response(self, response):
        await self.logger.log('INFO', f"Response: {response.status_code}")
        return response

    def run(self, host="0.0.0.0", port=8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

# Example usage
if __name__ == "__main__":
    api = API()
    api.run()
