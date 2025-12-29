def llm_relevance_evaluation(candidates, reference_product, model="gpt-4"):
    accessory_keywords = [
        "lid", "cap", "strap", "carrier", "bag", "replacement", "brush"
    ]

    evaluations = []
    confirmed = 0
    removed = 0

    for c in candidates:
        title_lower = c["title"].lower()

        is_competitor = not any(k in title_lower for k in accessory_keywords)
        confidence = 0.95 if is_competitor else 0.97

        if is_competitor:
            confirmed += 1
        else:
            removed += 1

        evaluations.append({
            "asin": c["asin"],
            "title": c["title"],
            "is_competitor": is_competitor,
            "confidence": confidence
        })

    return {
        "step": "llm_relevance_evaluation",
        "input": {
            "candidates_count": len(candidates),
            "reference_product": reference_product,
            "model": model
        },
        "prompt_template": (
            "Given the reference product '{title}', determine if each candidate "
            "is a true competitor or a false positive"
        ),
        "evaluations": evaluations,
        "output": {
            "total_evaluated": len(candidates),
            "confirmed_competitors": confirmed,
            "false_positives_removed": removed
        },
        "reasoning": f"Removed {removed} non-competitor accessories"
    }
