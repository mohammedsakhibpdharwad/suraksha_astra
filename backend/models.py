from transformers import pipeline
from PIL import Image
import numpy as np
import hashlib

text_model = pipeline("text-classification", model="unitary/toxic-bert")
image_model = pipeline("image-classification", model="AdamCodd/vit-base-nsfw-detector")


def analyze_text(text: str):
    result = text_model(text)[0]

    label = result["label"].lower()
    score = float(result["score"])
    text_lower = text.lower()

    toxicity = score if "toxic" in label else score * 0.3

    insult_words = ["idiot", "stupid", "dumb", "loser", "useless"]
    insult = sum(0.3 for word in insult_words if word in text_lower)
    insult = min(insult + toxicity * 0.5, 1.0)

    threat_words = ["kill", "attack", "bomb", "shoot", "destroy", "die"]
    threat = sum(0.4 for word in threat_words if word in text_lower)

    if "i will" in text_lower or "i'm going to" in text_lower:
        threat += 0.3

    threat = min(threat + toxicity * 0.4, 1.0)

    scam_words = ["otp", "send money", "urgent", "account blocked", "kyc", "click link", "loan approved"]
    scam = sum(0.25 for word in scam_words if word in text_lower)
    scam = min(scam, 1.0)

    return {
        "toxicity": round(toxicity, 3),
        "insult": round(insult, 3),
        "threat": round(threat, 3),
        "scam": round(scam, 3)
    }


def calculate_skin_exposure(image):
    """
    Simple skin-color detector.
    This is not perfect, but useful for suspicious/manual-review cases.
    """
    img = image.resize((224, 224)).convert("RGB")
    arr = np.array(img)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    skin_mask = (
        (r > 95) &
        (g > 40) &
        (b > 20) &
        ((np.maximum.reduce([r, g, b]) - np.minimum.reduce([r, g, b])) > 15) &
        (r > g) &
        (r > b)
    )

    skin_ratio = np.sum(skin_mask) / skin_mask.size
    return round(float(skin_ratio), 3)


def analyze_image(image_path: str, image_bytes: bytes):
    image = Image.open(image_path).convert("RGB")

    results = image_model(image)
    scores = {r["label"].lower(): float(r["score"]) for r in results}

    nsfw_score = scores.get("nsfw", 0)

    img_np = np.array(image)
    variance = float(np.var(img_np))

    deepfake_score = 0.7 if variance < 300 else 0.2
    skin_exposure_score = calculate_skin_exposure(image)

    evidence_hash = hashlib.md5(image_bytes).hexdigest()[:10]

    return {
        "nudity_score": round(nsfw_score, 3),
        "skin_exposure_score": skin_exposure_score,
        "deepfake_score": round(deepfake_score, 3),
        "evidence_hash": evidence_hash
    }