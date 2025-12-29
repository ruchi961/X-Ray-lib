import requests
import json


def make_get_request(url):
    response = requests.get(url)
    print("GET Status Code:", response.status_code)
    return json.dumps(response.json(), indent=2)


def make_post_request(url,data):
    

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data, headers=headers)

    print("POST Status Code:", response.status_code)
    return json.dumps(response.json(), indent=2)


if __name__ == "__main__":
    print("Running GET request...\n")
    make_get_request("https://httpbin.org/get")

    print("\nRunning POST request...\n")
    make_post_request("https://httpbin.org/post",{"data":"hello"})
