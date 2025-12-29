import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from reasoning_system_prompt import reasoning_system_prompt
from config_system_prompt import config_system_prompt
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from typing import Any, Optional
load_dotenv()  # loads .env into environment variables

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL= os.getenv("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

if not GEMINI_MODEL:
    raise ValueError("GEMINI_MODEL not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)


def get_reasoning(data: str) -> str:
    """
    Calls Gemini Flash model with a prompt and returns text response
    """

    response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="json file is :\n"+str(data),
    config=types.GenerateContentConfig(
        system_instruction=reasoning_system_prompt),
    )
    print(response.text)


    # return text output
    return response.text



class Output_json(BaseModel):
    input: Optional[Any] = Field(
        default=None,
        description="Input for the component. Can be string, dict, or nested dict."
    )
    output: Optional[Any] = Field(
        default=None,
        description="Output for the component. Can be string, dict, or nested dict."
    )
    metadata: Optional[Any] = Field(
        default=None,
        description="Metadata for the component. Can be string, dict, or nested dict."
    )





def get_config_json(data: str) -> dict:
    """
    Calls Gemini Flash and enforces JSON-only output
    """
    print(data)
    response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Return the json file for function: "+str(data),
    config=types.GenerateContentConfig(
        system_instruction=config_system_prompt,
        response_mime_type="application/json",
        response_json_schema=Output_json.model_json_schema(),
    )
    )

    Output_json_value = Output_json.model_validate_json(response.text)
    print(Output_json_value)

    print(Output_json_value.model_dump())

    # Gemini already returns JSON text, just parse it
    return Output_json_value.model_dump()


if __name__ == "__main__":
    prompt = """{
  "step": "candidate_search",
  "input": {
    "keyword": "stainless steel water bottle insulated",
    "limit": 50
  },
  "output": {
    "total_results": 2847,
    "candidates_fetched": 50,
    "candidates": [
      {"asin": "B0COMP01", "title": "HydroFlask 32oz Wide Mouth", "price": 44.99, "rating": 4.5, "reviews": 8932},
      {"asin": "B0COMP02", "title": "Yeti Rambler 26oz", "price": 34.99, "rating": 4.4, "reviews": 5621},
      {"asin": "B0COMP03", "title": "Generic Water Bottle", "price": 8.99, "rating": 3.2, "reviews": 45}
    ]
  },
  "reasoning": "Fetched top 50 results by relevance; 2847 total matches found"
}"""

    #answer = get_reasoning(prompt)
    #sprint(answer)
    prompt='''def candidate_search(keyword: str, limit: int):
    """
    Simulates a candidate search step.
    Returns a JSON-like dictionary with:
    - input
    - output (dummy candidates)
    - reasoning
    """

    # simulate total results found
    total_results = random.randint(1000, 5000)

    # generate dummy candidates
    candidates = []
    for i in range(1, min(limit, 10) + 1):  # limit to 10 for example
        candidates.append({
            "asin": f"B0COMP{str(100+i).zfill(2)}",
            "title": f"{keyword.title()} Variant {i}",
            "price": round(random.uniform(10, 50), 2),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "reviews": random.randint(10, 10000)
        })

   
    return result'''
    answer2 = get_config_json(prompt)
    print(answer2)
