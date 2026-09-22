from difflib import SequenceMatcher


def similarity_score(text1: str, text2: str):
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()

    if not text1 or not text2:
        return 0

    score = SequenceMatcher(None, text1, text2).ratio()
    return round(score * 100, 2)


def check_impersonation(original_username, suspicious_username, original_bio, suspicious_bio):
    username_score = similarity_score(original_username, suspicious_username)
    bio_score = similarity_score(original_bio, suspicious_bio)

    risk_score = 0
    reasons = []

    if username_score > 80:
        risk_score += 40
        reasons.append("Username is highly similar to original account")

    elif username_score > 60:
        risk_score += 25
        reasons.append("Username has moderate similarity")

    if bio_score > 75:
        risk_score += 30
        reasons.append("Bio is highly similar to original account")

    elif bio_score > 50:
        risk_score += 15
        reasons.append("Bio has moderate similarity")

    if risk_score >= 60:
        decision = "HIGH IMPERSONATION RISK"
    elif risk_score >= 30:
        decision = "SUSPICIOUS"
    else:
        decision = "LOW RISK"

    return {
        "username_similarity": username_score,
        "bio_similarity": bio_score,
        "impersonation_risk_score": risk_score,
        "decision": decision,
        "reasons": reasons
    }