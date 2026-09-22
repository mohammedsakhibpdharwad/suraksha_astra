def calculate_text_score(text_result, current_score=100):
    score = current_score
    reasons = []

    if text_result["toxicity"] > 0.7:
        score -= 10
        reasons.append("High toxicity detected")

    if text_result["insult"] > 0.5:
        score -= 8
        reasons.append("Insulting language used")

    if text_result["threat"] > 0.6:
        score -= 15
        reasons.append("Threatening content detected")

    if text_result["scam"] > 0.5:
        score -= 20
        reasons.append("Scam or fraud-like message detected")

    if text_result["toxicity"] > 0.4:
        score -= 5
        reasons.append("Moderate toxicity found")

    score = max(score, 0)
    return score, reasons


def calculate_image_score(image_result, current_score=100):
    score = current_score
    reasons = []

    if image_result["nudity_score"] > 0.6:
        score -= 20
        reasons.append("Explicit NSFW / nudity content detected")

    elif image_result["skin_exposure_score"] > 0.30:
        score -= 8
        reasons.append("High skin exposure detected; manual review recommended")

    if image_result["deepfake_score"] > 0.6:
        score -= 10
        reasons.append("Possible manipulated or AI-generated image pattern detected")

    score = max(score, 0)
    return score, reasons