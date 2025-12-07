"""
Test script for GiftingGenie API
Run this to test the recommendation engine
"""
from gifting_engine import GiftingEngine
import json


def test_recommendation_engine():
    """Test the gifting engine with various scenarios"""

    engine = GiftingEngine()

    test_cases = [
        {
            "name": "Raksha Bandhan for Saali",
            "relationship": "Saali",
            "occasion": "Raksha Bandhan",
            "age_group": "Adult",
            "vibe": "Traditional",
            "budget": 2000
        },
        {
            "name": "Boss Birthday (Professional)",
            "relationship": "Boss",
            "occasion": "Birthday",
            "age_group": "Adult",
            "vibe": "Formal",
            "budget": 5000
        },
        {
            "name": "Mother on Diwali",
            "relationship": "Mother",
            "occasion": "Diwali",
            "age_group": "Senior",
            "vibe": "Traditional",
            "budget": 3000
        },
        {
            "name": "Girlfriend Valentine's Day",
            "relationship": "Girlfriend",
            "occasion": "Valentine's Day",
            "age_group": "Adult",
            "vibe": "Romantic",
            "budget": 4000
        },
        {
            "name": "Friend's Wedding",
            "relationship": "Friend",
            "occasion": "Wedding",
            "age_group": "Adult",
            "vibe": "Modern",
            "budget": 10000
        }
    ]

    print("=" * 80)
    print("GiftingGenie API - Test Results")
    print("=" * 80)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\nTest Case {i}: {test_case['name']}")
        print("-" * 80)

        result = engine.generate_recommendations(
            relationship=test_case["relationship"],
            occasion=test_case["occasion"],
            age_group=test_case["age_group"],
            vibe=test_case["vibe"],
            budget=test_case["budget"]
        )

        print(f"\nThinking Trace: {result['thinking_trace']}\n")
        print("Recommendations:")

        for rec in result["recommendations"]:
            print(f"\n  {rec['id']}. {rec['title']}")
            print(f"     Price: {rec['approx_price_inr']}")
            print(f"     Why: {rec['description']}")
            print(f"     Amazon: {rec['purchase_links']['amazon_in']}")
            print(f"     Flipkart: {rec['purchase_links']['flipkart']}")

        print(f"\n💡 Pro Tip: {result['pro_tip']}")
        print("-" * 80)

    print("\n\n✅ All test cases completed successfully!")


def test_json_output():
    """Test that output matches the required JSON schema"""
    engine = GiftingEngine()

    result = engine.generate_recommendations(
        relationship="Mother",
        occasion="Birthday",
        age_group="Senior",
        vibe="Traditional",
        budget=2500
    )

    print("\n" + "=" * 80)
    print("JSON Schema Validation Test")
    print("=" * 80)
    print("\nOutput JSON:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Validate schema
    assert "thinking_trace" in result, "Missing thinking_trace"
    assert "recommendations" in result, "Missing recommendations"
    assert "pro_tip" in result, "Missing pro_tip"
    assert len(result["recommendations"]) == 5, "Should have 5 recommendations"

    for rec in result["recommendations"]:
        assert "id" in rec, "Missing id"
        assert "title" in rec, "Missing title"
        assert "description" in rec, "Missing description"
        assert "approx_price_inr" in rec, "Missing approx_price_inr"
        assert "purchase_links" in rec, "Missing purchase_links"
        assert "amazon_in" in rec["purchase_links"], "Missing amazon_in link"
        assert "flipkart" in rec["purchase_links"], "Missing flipkart link"

    print("\n✅ JSON schema validation passed!")


if __name__ == "__main__":
    test_recommendation_engine()
    test_json_output()
