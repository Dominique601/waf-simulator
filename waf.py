import re


ATTACK_PATTERNS = {
    "SQL Injection": {
        "severity": "HIGH",
        "description": (
            "The request contains patterns commonly associated with "
            "SQL injection attempts."
        ),
        "patterns": [
            r"(?i)\bunion\b.*\bselect\b",
            r"(?i)\bor\b\s+1\s*=\s*1",
            r"(?i)\band\b\s+1\s*=\s*1",
            r"(?i)\bdrop\b\s+\btable\b",
            r"(?i)\bselect\b.*\bfrom\b",
            r"(?i)\binsert\b.*\binto\b",
            r"(?i)\bdelete\b.*\bfrom\b",
        ],
    },

    "Cross-Site Scripting (XSS)": {
        "severity": "HIGH",
        "description": (
            "The request contains script-related patterns that may "
            "attempt to execute code in a user's browser."
        ),
        "patterns": [
            r"(?i)<script.*?>",
            r"(?i)javascript:",
            r"(?i)onerror\s*=",
            r"(?i)onload\s*=",
            r"(?i)<iframe.*?>",
        ],
    },

    "Path Traversal": {
        "severity": "MEDIUM",
        "description": (
            "The request contains directory traversal patterns that "
            "may attempt to access files outside the intended directory."
        ),
        "patterns": [
            r"\.\./",
            r"\.\.\\",
            r"(?i)%2e%2e%2f",
            r"(?i)%2e%2e/",
        ],
    },

    "Command Injection": {
        "severity": "CRITICAL",
        "description": (
            "The request contains operating-system command patterns "
            "that may indicate a command injection attempt."
        ),
        "patterns": [
            r"(?i);\s*(cat|ls|whoami|id|uname)\b",
            r"(?i)&&\s*(cat|ls|whoami|id|uname)\b",
            r"(?i)\|\s*(cat|ls|whoami|id|uname)\b",
            r"(?i)\$\(",
        ],
    },

    "Sensitive File Access": {
        "severity": "HIGH",
        "description": (
            "The request appears to target a sensitive system or "
            "configuration file."
        ),
        "patterns": [
            r"(?i)/etc/passwd",
            r"(?i)/etc/shadow",
            r"(?i)\.env\b",
            r"(?i)wp-config\.php",
        ],
    },
}


def analyze_request(user_input):
    for attack_type, details in ATTACK_PATTERNS.items():

        for pattern in details["patterns"]:

            if re.search(pattern, user_input):

                return {
                    "status": "BLOCKED",
                    "attack": attack_type,
                    "severity": details["severity"],
                    "description": details["description"],
                }

    return {
        "status": "ALLOWED",
        "attack": None,
        "severity": "NONE",
        "description": "No known malicious pattern was detected.",
    }
