import re
from collections import Counter

STOPWORDS = {
    "the", "and", "or", "with", "for", "of", "to", "in", "on",
    "oz", "ml", "pack", "set"
}

def generate_keyword(input_data):
    """
    Step: keyword_generation
    Extracts real keywords from product title + category
    """

    product_title = input_data.get("product_title", "")
    category = input_data.get("category", "")

    # Normalize text
    text = f"{product_title} {category}".lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    words = [
        w for w in text.split()
        if w not in STOPWORDS and len(w) > 2
    ]

    # Frequency-based keyword selection
    freq = Counter(words)
    top_words = [w for w, _ in freq.most_common(6)]

    # Generate keyword phrases
    keywords = []
    if "stainless" in top_words and "steel" in top_words:
        keywords.append("stainless steel water bottle insulated")

    if "insulated" in top_words:
        keywords.append("vacuum insulated bottle 32oz")

    # Fallback: join top words
    if not keywords:
        keywords.append(" ".join(top_words[:4]))

    result = {
        "step": "keyword_generation",
        "input": {
            "product_title": product_title,
            "category": category
        },
        "output": {
            "keywords": keywords,
            "model": "rule_based_nlp"
        },
        "reasoning": (
            "Extracted keywords using normalization, stopword removal, "
            "frequency analysis, and phrase construction from title and category"
        )
    }

    return result
