def generate_explanation(score, reasons):

    if score >= 80:
        status = "SAFE"
    elif score >= 50:
        status = "MONITOR"
    elif score >= 30:
        status = "SUSPICIOUS"
    else:
        status = "HIGH RISK"

    return {
        "score": score,
        "status": status,
        "reasons": reasons
    }