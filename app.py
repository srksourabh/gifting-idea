"""
GiftingGenie API
FastAPI backend for Indian personal shopper and gifting concierge
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from gifting_engine import GiftingEngine
import os

app = FastAPI(
    title="GiftingGenie API",
    description="Expert Indian Personal Shopper & Gifting Concierge",
    version="1.0.0"
)

# Enable CORS for mobile app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the gifting engine
gifting_engine = GiftingEngine()

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


class GiftRequest(BaseModel):
    """Request model for gift recommendations"""
    relationship: str = Field(
        ...,
        description="Relationship type (e.g., 'Saali', 'Boss', 'Mother', 'Friend')",
        example="Saali"
    )
    occasion: str = Field(
        ...,
        description="Occasion (e.g., 'Raksha Bandhan', 'Wedding', 'Birthday')",
        example="Raksha Bandhan"
    )
    age_group: Optional[str] = Field(
        "Adult",
        description="Age group of the recipient (e.g., 'Child', 'Teenager', 'Adult', 'Senior')",
        example="Adult"
    )
    vibe: Optional[str] = Field(
        "Traditional",
        description="Gift vibe/style (e.g., 'Traditional', 'Modern', 'Personalized', 'Luxury')",
        example="Traditional"
    )
    budget: int = Field(
        ...,
        description="Budget in INR",
        example=2000,
        ge=100,
        le=1000000
    )


@app.get("/")
async def root():
    """Serve the main landing page"""
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {
        "status": "active",
        "service": "GiftingGenie API",
        "version": "1.0.0",
        "description": "Expert Indian Personal Shopper & Gifting Concierge",
        "web_ui": "Visit /static/index.html for the web interface"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


@app.post("/api/v1/recommend")
async def recommend_gifts(request: GiftRequest):
    """
    Generate gift recommendations based on relationship, occasion, and budget

    Returns 5 culturally-appropriate gift suggestions with purchase links
    """
    try:
        recommendations = gifting_engine.generate_recommendations(
            relationship=request.relationship,
            occasion=request.occasion,
            age_group=request.age_group or "Adult",
            vibe=request.vibe or "Traditional",
            budget=request.budget
        )

        return recommendations

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@app.get("/api/v1/occasions")
async def list_occasions():
    """List all supported occasions"""
    return {
        "occasions": list(gifting_engine.OCCASION_CONTEXT.keys())
    }


@app.get("/api/v1/relationships")
async def list_relationships():
    """List all supported relationship types"""
    return {
        "relationships": list(gifting_engine.RELATIONSHIP_CONTEXT.keys())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
