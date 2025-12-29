from make_requests import *

url = "http://localhost:5000/log"

def llm_relevance_evaluation():
    input_data = {
        "candidates_count": 12,
        "reference_product": {
            "asin": "B0XYZ123",
            "title": "ProBrand Steel Bottle 32oz Insulated",
            "category": "Sports & Outdoors > Water Bottles"
        },
        "model": "gpt-4"
    }

    metadata = {
        "prompt_template": "Given the reference product '{title}', determine if each candidate is a true competitor (same product type) or a false positive (accessory, replacement part, bundle, etc.)",
        "evaluations": [
            {
                "asin": "B0COMP01",
                "title": "HydroFlask 32oz Wide Mouth",
                "is_competitor": True,
                "confidence": 0.95
            },
            {
                "asin": "B0COMP02",
                "title": "Yeti Rambler 26oz",
                "is_competitor": True,
                "confidence": 0.92
            },
            {
                "asin": "B0COMP05",
                "title": "Replacement Lid for HydroFlask",
                "is_competitor": False,
                "confidence": 0.98
            },
            {
                "asin": "B0COMP06",
                "title": "Water Bottle Carrier Bag with Strap",
                "is_competitor": False,
                "confidence": 0.97
            }
        ]
    }

    output_data = {
        "total_evaluated": 12,
        "confirmed_competitors": 8,
        "false_positives_removed": 4
    }

    make_post_request(
        url,
        {
            "project": "Ranking_response",
            "query_id": "1",
            "component": "step_4_llm_relevance_evaluation",
            "data": {
                "input": input_data,
                "metadata": metadata,
                "output": output_data
            }
        }
    )
llm_relevance_evaluation()
