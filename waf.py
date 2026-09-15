import re


def analyze_request(user_input):
    patterns = {
        "SQL Injection": [
            r"(?i)\bunion\b.*\bselect\b",
            r"(?i)\bor\b\s+1\s*=\s*1",
            r"(?i)\bdrop\b\s+\btable\b",
            r"(?i)\bselect\b.*\bfrom\b",
        ],
        "Cross-Site Scripting (XSS)": [
            r"(?i)<script.*?>",
            r"(?i)javascript:",
            r"(?i)onerror\s*=",
            r"(?i)onload\s*=",
        ],
        "Path Traversal": [
            r"\.\./",
            r"\.\.\\",
        ],
    }

    for attack_type, attack_patterns in patterns.items():
        for pattern in attack_patterns:
            if re.search(pattern, user_input):
                return {
                    "status": "BLOCKED",
                    "attack": attack_type,
                }

    return {
        "status": "ALLOWED",
        "attack": None,
    }
