from make_requests import *

url = "http://localhost:5000/log"

def generate_keyword():
    # dummy input data
    input_data = {
        "product_title": "Stainless Steel Water Bottle 32oz Insulated",
        "category": "Sports & Outdoors"
    }

    # dummy output data
    output_data = {
        "keywords": [
            "stainless steel water bottle insulated",
            "vacuum insulated bottle 32oz"
        ],
        "model": "dummy-model-v1"
    }

    request_payload = {
        "project": "Ranking_response",
        "query_id": "1",
        "component": "step_1_keyword_generation",
        "data": {
            "input": input_data,
            "output": output_data,
        }
    }
    #response = requests.post(url,json=request_payload)
    #print(response)
    ans = make_post_request(url, request_payload)
    print(ans)
generate_keyword()
