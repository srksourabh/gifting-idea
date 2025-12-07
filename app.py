"""
GiftingGenie API
FastAPI backend for Indian personal shopper and gifting concierge
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
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


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main landing page"""
    static_file = os.path.join(os.path.dirname(__file__), "static", "index.html")
    try:
        with open(static_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="""
            <html><body>
            <h1>GiftingGenie API</h1>
            <p>API is running. Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body></html>
        """, status_code=200)


@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to prevent 404 errors"""
    # Return a simple SVG emoji favicon
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <text y=".9em" font-size="90">🎁</text>
    </svg>"""
    return Response(content=svg_content, media_type="image/svg+xml")


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
