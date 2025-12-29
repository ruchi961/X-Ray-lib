from make_requests import *

url = "http://localhost:5000/log"

def rank_and_select():
    input_data = {
        "candidates_count": 8,
        "reference_product": {
            "asin": "B0XYZ123",
            "title": "ProBrand Steel Bottle 32oz Insulated",
            "price": 29.99,
            "rating": 4.2,
            "reviews": 1247
        }
    }

    metadata = {
        "ranking_criteria": {
            "primary": "review_count",
            "secondary": "rating",
            "tertiary": "price_proximity"
        },
        "ranked_candidates": [
            {
                "rank": 1,
                "asin": "B0COMP01",
                "title": "HydroFlask 32oz Wide Mouth",
                "metrics": {"price": 44.99, "rating": 4.5, "reviews": 8932},
                "score_breakdown": {
                    "review_count_score": 1.0,
                    "rating_score": 0.9,
                    "price_proximity_score": 0.7
                },
                "total_score": 0.92
            },
            {
                "rank": 2,
                "asin": "B0COMP02",
                "title": "Yeti Rambler 26oz",
                "metrics": {"price": 34.99, "rating": 4.4, "reviews": 5621},
                "score_breakdown": {
                    "review_count_score": 0.63,
                    "rating_score": 0.85,
                    "price_proximity_score": 0.85
                },
                "total_score": 0.74
            },
            {
                "rank": 3,
                "asin": "B0COMP07",
                "title": "Stanley Adventure Quencher",
                "metrics": {"price": 35.00, "rating": 4.3, "reviews": 4102},
                "score_breakdown": {
                    "review_count_score": 0.46,
                    "rating_score": 0.8,
                    "price_proximity_score": 0.84
                },
                "total_score": 0.65
            }
        ],
        "selection": {
            "asin": "B0COMP01",
            "title": "HydroFlask 32oz Wide Mouth",
            "reason": "Highest overall score (0.92) - top review count (8,932) with strong rating (4.5★)"
        }
    }

    output_data = {
        "selected_competitor": {
            "asin": "B0COMP01",
            "title": "HydroFlask 32oz Wide Mouth",
            "price": 44.99,
            "rating": 4.5,
            "reviews": 8932
        }
    }

    make_post_request(
        url,
        {
            "project": "Ranking_response",
            "query_id": "2",
            "component": "step_5_rank_and_select",
            "data": {
                "input": input_data,
                "metadata": metadata,
                "output": output_data
            }
        }
    )
rank_and_select()
