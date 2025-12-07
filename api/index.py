"""
Vercel serverless function entry point
"""
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the FastAPI app
from app import app
from mangum import Mangum

# Create the Mangum handler for AWS Lambda/Vercel
handler = Mangum(app, lifespan="off")

# Export app for direct access if needed
__all__ = ["handler", "app"]
