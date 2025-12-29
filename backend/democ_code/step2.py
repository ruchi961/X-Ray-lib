import re

# Example product catalog (could be DB / CSV / API in real life)
PRODUCT_CATALOG = [
    {
        "asin": "B0COMP01",
        "title": "HydroFlask 32oz Wide Mouth Stainless Steel Bottle",
        "price": 44.99,
        "rating": 4.5,
        "reviews": 8932
    },
    {
        "asin": "B0COMP02",
        "title": "Yeti Rambler 26oz Insulated Stainless Steel Bottle",
        "price": 34.99,
        "rating": 4.4,
        "reviews": 5621
    },
    {
        "asin": "B0COMP03",
        "title": "Generic Plastic Water Bottle",
        "price": 8.99,
        "rating": 3.2,
        "reviews": 45
    },
    {
        "asin": "B0COMP04",
        "title": "Insulated Stainless Steel Sports Bottle 32oz",
        "price": 27.99,
        "rating": 4.1,
        "reviews": 1203
    }
]

def candidate_search(input_data):
    """
    Step: candidate_search
    Searches a product catalog using keyword relevance
    """

    keyword = input_data.get("keyword", "").lower()
    limit = input_data.get("limit", 50)

    keyword_tokens = set(re.findall(r"\w+", keyword))

    scored_results = []

    # Relevance scoring
    for product in PRODUCT_CATALOG:
        title_tokens = set(re.findall(r"\w+", product["title"].lower()))
        relevance_score = len(keyword_tokens & title_tokens)

        if relevance_score > 0:
            scored_results.append((relevance_score, product))

    # Sort by relevance, rating, reviews
    scored_results.sort(
        key=lambda x: (x[0], x[1]["rating"], x[1]["reviews"]),
        reverse=True
    )

    # Apply limit
    candidates = [
        {
            "asin": p["asin"],
            "title": p["title"],
            "price": p["price"],
            "rating": p["rating"],
            "reviews": p["reviews"]
        }
        for _, p in scored_results[:limit]
    ]

    result = {
        "step": "candidate_search",
        "input": {
            "keyword": keyword,
            "limit": limit
        },
        "output": {
            "total_results": len(scored_results),
            "candidates_fetched": len(candidates),
            "candidates": candidates
        },
        "reasoning": (
            f"Fetched top {len(candidates)} results by keyword relevance; "
            f"{len(scored_results)} total matches found"
        )
    }

    return result
