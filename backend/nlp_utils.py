import os
import re
from typing import List, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "").strip()
HF_MODEL = os.getenv("HF_MODEL", "facebook/bart-large-cnn").strip()
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"


def split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def fallback_summary(email_text: str) -> str:
    sentences = split_sentences(email_text)

    if not sentences:
        return "No summary available."

    if len(sentences) == 1:
        return sentences[0]

    return " ".join(sentences[:2])


def summarize_email(email_text: str) -> str:
    """
    Uses Hugging Face summarization if the token works.
    If Hugging Face fails due to internet/token/model/certificate issues,
    it returns a safe fallback summary so the project still works for demo.
    """
    if not HF_API_TOKEN or HF_API_TOKEN == "hf_your_actual_token_here":
        return fallback_summary(email_text)

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }

    payload = {
        "inputs": email_text[:3000],
        "parameters": {
            "max_length": 120,
            "min_length": 25,
            "do_sample": False
        }
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        if response.status_code != 200:
            return fallback_summary(email_text)

        data = response.json()

        if isinstance(data, list) and data and isinstance(data[0], dict):
            return data[0].get("summary_text", fallback_summary(email_text))

        return fallback_summary(email_text)

    except Exception:
        return fallback_summary(email_text)


def extract_key_points(email_text: str) -> List[str]:
    keywords = [
        "important",
        "deadline",
        "meeting",
        "submit",
        "review",
        "attached",
        "required",
        "schedule",
        "update",
        "project",
        "report",
        "confirm",
        "tomorrow",
        "today",
        "friday",
        "monday",
        "final",
        "accepted",
        "workshop",
        "announcement",
        "optional",
        "participation"
    ]

    sentences = split_sentences(email_text)
    key_points = []

    for sentence in sentences:
        lower = sentence.lower()

        if any(keyword in lower for keyword in keywords):
            key_points.append(sentence)

    return key_points[:5] if key_points else sentences[:3]


def detect_action_items(email_text: str) -> List[str]:
    action_words = [
        "submit",
        "complete",
        "send",
        "review",
        "attend",
        "confirm",
        "reply",
        "upload",
        "join",
        "prepare",
        "finish",
        "check",
        "respond",
        "fill",
        "share",
        "call",
        "please submit",
        "please attend",
        "please confirm",
        "please review",
        "action required",
        "required"
    ]

    non_action_phrases = [
        "thanks for sharing",
        "thank you for sharing",
        "hope you are doing well",
        "happy to help",
        "general announcement",
        "newsletter",
        "optional",
        "participation is optional",
        "schedule will be shared later",
        "best,"
    ]

    sentences = split_sentences(email_text)
    actions = []

    for sentence in sentences:
        lower = sentence.lower()

        if any(phrase in lower for phrase in non_action_phrases):
            continue

        if any(word in lower for word in action_words):
            actions.append(sentence)

    return actions[:5] if actions else ["No specific action required."]


def classify_priority(email_text: str) -> Tuple[str, str]:
    text = email_text.lower()
    score = 0
    reasons = []

    high_keywords = {
        "urgent": "urgent keyword detected",
        "asap": "ASAP mentioned",
        "immediately": "immediate action requested",
        "deadline": "deadline mentioned",
        "today": "near deadline mentioned",
        "tomorrow": "near deadline mentioned",
        "final reminder": "final reminder detected",
        "action required": "action required mentioned",
        "required": "required action detected",
        "submit": "submission required",
        "late submissions": "late submission warning detected"
    }

    medium_keywords = {
        "meeting": "meeting mentioned",
        "schedule": "schedule mentioned",
        "follow up": "follow-up needed",
        "review": "review requested",
        "update": "update mentioned",
        "confirm": "confirmation requested",
        "response needed": "response needed",
        "workshop": "workshop mentioned"
    }

    low_keywords = {
        "newsletter": "newsletter type email",
        "announcement": "announcement type email",
        "optional": "optional information",
        "general": "general information",
        "participation is optional": "optional participation mentioned"
    }

    for keyword, reason in high_keywords.items():
        if keyword in text:
            score += 2
            reasons.append(reason)

    for keyword, reason in medium_keywords.items():
        if keyword in text:
            score += 1
            reasons.append(reason)

    for keyword, reason in low_keywords.items():
        if keyword in text:
            score -= 1
            reasons.append(reason)

    if score >= 4:
        priority = "High"
    elif score >= 2:
        priority = "Medium"
    else:
        priority = "Low"

    if not reasons:
        reasons.append("No strong urgency or deadline keywords detected")

    if priority == "Low":
        low_only_reasons = [
            "update mentioned",
            "general information",
            "optional information",
            "announcement type email",
            "newsletter type email",
            "optional participation mentioned"
        ]

        if all(reason in low_only_reasons for reason in reasons):
            return priority, "No urgent action or deadline detected."

    return priority, "; ".join(reasons[:5]) + "."


def detect_tone(email_text: str) -> str:
    text = email_text.lower()
    tones = []

    urgent_words = [
        "urgent",
        "asap",
        "immediately",
        "deadline",
        "important",
        "late submissions",
        "required"
    ]

    formal_words = [
        "dear",
        "regards",
        "sincerely",
        "respected",
        "kindly",
        "coordinator",
        "sir",
        "madam",
        "department office",
        "office"
    ]

    friendly_words = [
        "hi",
        "thanks",
        "thank you",
        "happy",
        "hope"
    ]

    info_words = [
        "notice",
        "announcement",
        "information",
        "newsletter",
        "workshop",
        "general",
        "optional",
        "participation is optional",
        "schedule will be shared",
        "will be shared",
        "hello everyone"
    ]

    is_urgent = any(word in text for word in urgent_words)
    is_formal = any(word in text for word in formal_words)
    is_friendly = any(word in text for word in friendly_words)
    is_informational = any(word in text for word in info_words)

    if is_urgent:
        tones.append("Urgent")

    if is_formal:
        tones.append("Formal")

    if is_friendly and not is_formal and not is_urgent and not is_informational:
        tones.append("Friendly")

    if is_informational and not is_urgent:
        tones.append("Informational")

    if not tones:
        return "Neutral"

    return " and ".join(tones)


def generate_reply(email_text: str, priority: str, tone: str) -> str:
    text = email_text.lower()

    if "meeting" in text or "attend" in text:
        return "Thank you for the information. I confirm that I will attend the meeting and complete the required action on time."

    if priority == "High":
        return "Thank you for the update. I have noted the urgency and will complete the required action as soon as possible."

    if "deadline" in text or "submit" in text:
        return "Thank you for the reminder. I will submit the required work before the deadline."

    if "announcement" in text or "newsletter" in text or "optional" in text or "workshop" in text:
        return "Thank you for sharing the information."

    if "thanks" in text or "thank you" in text or "hope" in text:
        return "Thank you for your message. I appreciate the update."

    return "Thank you for the update. I will review it and respond if any action is required."


def analyze_email(email_text: str) -> dict:
    summary = summarize_email(email_text)
    key_points = extract_key_points(email_text)
    action_items = detect_action_items(email_text)
    priority, priority_reason = classify_priority(email_text)
    tone = detect_tone(email_text)
    suggested_reply = generate_reply(email_text, priority, tone)

    return {
        "summary": summary,
        "key_points": key_points,
        "action_items": action_items,
        "priority": priority,
        "priority_reason": priority_reason,
        "tone": tone,
        "suggested_reply": suggested_reply
    }