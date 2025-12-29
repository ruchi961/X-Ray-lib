from make_requests import *

url = "http://localhost:5000/log"

def apply_filters():
    input_data = {
        "candidates_count": 50,
        "reference_product": {
            "asin": "B0XYZ123",
            "title": "ProBrand Steel Bottle 32oz Insulated",
            "price": 29.99,
            "rating": 4.2,
            "reviews": 1247
        }
    }

    metadata = {
        "filters_applied": {
            "price_range": {"min": 14.99, "max": 59.98, "rule": "0.5x - 2x of reference price"},
            "min_rating": {"value": 3.8, "rule": "Must be at least 3.8 stars"},
            "min_reviews": {"value": 100, "rule": "Must have at least 100 reviews"}
        },
        "evaluations": [
            {
                "asin": "B0COMP01",
                "title": "HydroFlask 32oz Wide Mouth",
                "metrics": {"price": 44.99, "rating": 4.5, "reviews": 8932},
                "filter_results": {
                    "price_range": {"passed": True, "detail": "$44.99 is within $14.99-$59.98"},
                    "min_rating": {"passed": True, "detail": "4.5 >= 3.8"},
                    "min_reviews": {"passed": True, "detail": "8932 >= 100"}
                },
                "qualified": True
            },
            {
                "asin": "B0COMP02",
                "title": "Yeti Rambler 26oz",
                "metrics": {"price": 34.99, "rating": 4.4, "reviews": 5621},
                "filter_results": {
                    "price_range": {"passed": True, "detail": "$34.99 is within $14.99-$59.98"},
                    "min_rating": {"passed": True, "detail": "4.4 >= 3.8"},
                    "min_reviews": {"passed": True, "detail": "5621 >= 100"}
                },
                "qualified": True
            },
            {
                "asin": "B0COMP03",
                "title": "Generic Water Bottle",
                "metrics": {"price": 8.99, "rating": 3.2, "reviews": 45},
                "filter_results": {
                    "price_range": {"passed": False, "detail": "$8.99 is below minimum $14.99"},
                    "min_rating": {"passed": False, "detail": "3.2 < 3.8 threshold"},
                    "min_reviews": {"passed": False, "detail": "45 < 100 minimum"}
                },
                "qualified": False
            },
            {
                "asin": "B0COMP04",
                "title": "Bottle Cleaning Brush Set",
                "metrics": {"price": 12.99, "rating": 4.6, "reviews": 3421},
                "filter_results": {
                    "price_range": {"passed": False, "detail": "$12.99 is below minimum $14.99"},
                    "min_rating": {"passed": True, "detail": "4.6 >= 3.8"},
                    "min_reviews": {"passed": True, "detail": "3421 >= 100"}
                },
                "qualified": False
            }
        ]
    }

    output_data = {
        "total_evaluated": 50,
        "passed": 12,
        "failed": 38
    }

    make_post_request(
        url,
        {
            "project": "Ranking_response_two",
            "query_id": "1",
            "component": "step_3_apply_filters",
            "data": {
                "input": input_data,
                "metadata": metadata,
                "output": output_data
            }
        }
    )
apply_filters()
