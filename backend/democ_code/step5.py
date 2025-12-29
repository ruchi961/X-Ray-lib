def rank_and_select(candidates, reference_product):
    max_reviews = max(c["reviews"] for c in candidates)
    ref_price = reference_product["price"]

    ranked = []

    for c in candidates:
        review_score = c["reviews"] / max_reviews
        rating_score = c["rating"] / 5.0
        price_proximity_score = 1 - abs(c["price"] - ref_price) / ref_price

        total_score = round(
            0.5 * review_score +
            0.3 * rating_score +
            0.2 * price_proximity_score, 2
        )

        ranked.append({
            "asin": c["asin"],
            "title": c["title"],
            "metrics": {
                "price": c["price"],
                "rating": c["rating"],
                "reviews": c["reviews"]
            },
            "score_breakdown": {
                "review_count_score": round(review_score, 2),
                "rating_score": round(rating_score, 2),
                "price_proximity_score": round(price_proximity_score, 2)
            },
            "total_score": total_score
        })

    ranked.sort(key=lambda x: x["total_score"], reverse=True)

    for idx, r in enumerate(ranked, start=1):
        r["rank"] = idx

    winner = ranked[0]

    return {
        "step": "rank_and_select",
        "input": {
            "candidates_count": len(candidates),
            "reference_product": reference_product
        },
        "ranking_criteria": {
            "primary": "review_count",
            "secondary": "rating",
            "tertiary": "price_proximity"
        },
        "ranked_candidates": ranked,
        "selection": {
            "asin": winner["asin"],
            "title": winner["title"],
            "reason": (
                f"Highest overall score ({winner['total_score']}) "
                f"with strong reviews and rating"
            )
        },
        "output": {
            "selected_competitor": {
                "asin": winner["asin"],
                "title": winner["title"],
                "price": winner["metrics"]["price"],
                "rating": winner["metrics"]["rating"],
                "reviews": winner["metrics"]["reviews"]
            }
        }
    }
