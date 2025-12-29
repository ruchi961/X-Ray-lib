import json
from typing import List, Dict


def apply_filters(candidates: List[Dict], reference_product: Dict):
    # Rules
    min_price = round(reference_product["price"] * 0.5, 2)
    max_price = round(reference_product["price"] * 2, 2)
    min_rating = 3.8
    min_reviews = 100

    evaluations = []
    passed_count = 0

    for c in candidates:
        price_pass = min_price <= c["price"] <= max_price
        rating_pass = c["rating"] >= min_rating
        reviews_pass = c["reviews"] >= min_reviews

        qualified = price_pass and rating_pass and reviews_pass

        if qualified:
            passed_count += 1

        evaluations.append({
            "asin": c["asin"],
            "title": c["title"],
            "metrics": {
                "price": c["price"],
                "rating": c["rating"],
                "reviews": c["reviews"]
            },
            "filter_results": {
                "price_range": {
                    "passed": price_pass,
                    "detail": (
                        f"${c['price']} is within ${min_price}-${max_price}"
                        if price_pass else
                        f"${c['price']} is outside ${min_price}-${max_price}"
                    )
                },
                "min_rating": {
                    "passed": rating_pass,
                    "detail": (
                        f"{c['rating']} >= {min_rating}"
                        if rating_pass else
                        f"{c['rating']} < {min_rating} threshold"
                    )
                },
                "min_reviews": {
                    "passed": reviews_pass,
                    "detail": (
                        f"{c['reviews']} >= {min_reviews}"
                        if reviews_pass else
                        f"{c['reviews']} < {min_reviews} minimum"
                    )
                }
            },
            "qualified": qualified
        })

    result = {
        "step": "apply_filters",
        "input": {
            "candidates_count": len(candidates),
            "reference_product": reference_product
        },
        "filters_applied": {
            "price_range": {
                "min": min_price,
                "max": max_price,
                "rule": "0.5x - 2x of reference price"
            },
            "min_rating": {
                "value": min_rating,
                "rule": "Must be at least 3.8 stars"
            },
            "min_reviews": {
                "value": min_reviews,
                "rule": "Must have at least 100 reviews"
            }
        },
        "evaluations": evaluations,
        "output": {
            "total_evaluated": len(candidates),
            "passed": passed_count,
            "failed": len(candidates) - passed_count
        },
        "reasoning": (
            f"Applied price range (${min_price}-${max_price}), "
            f"minimum rating ({min_rating}), and minimum review count "
            f"({min_reviews}) filters to reduce "
            f"{len(candidates)} candidates to {passed_count} qualified results"
        )
    }

    return result
