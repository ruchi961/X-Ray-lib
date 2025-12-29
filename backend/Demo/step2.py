from make_requests import *

url = "http://localhost:5000/log"

def candidate_search():
    # dummy input data
    input_data = {
        "keyword": "stainless steel water bottle insulated",
        "limit": 50
    }

    # dummy output data
    output_data = {
        "total_results": 2847,
        "candidates_fetched": 50,
        "candidates": [
            {
                "asin": "B0COMP01",
                "title": "HydroFlask 32oz Wide Mouth",
                "price": 44.99,
                "rating": 4.5,
                "reviews": 8932
            },
            {
                "asin": "B0COMP02",
                "title": "Yeti Rambler 26oz",
                "price": 34.99,
                "rating": 4.4,
                "reviews": 5621
            },
            {
                "asin": "B0COMP03",
                "title": "Generic Water Bottle",
                "price": 8.99,
                "rating": 3.2,
                "reviews": 45
            }
        ]
    }

    request_payload = {
        "project": "Ranking_response",
        "query_id": "1",
        "component": "step_3_candidate_search",
        "data": {
            "input": input_data,
            "output": output_data
        }
    }


    ans =make_post_request(url, request_payload)
    print(ans)
candidate_search()
