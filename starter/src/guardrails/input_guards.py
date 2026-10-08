"""Input-side validators: prompt injection detection and PII redaction.

Lightweight regex/heuristic implementations chosen over Guardrails Hub
validators for capstone reliability. The Hub validators (e.g.
``hub://guardrails/detect_pii``) are the production upgrade path covered
in the Guardrails module's content; LLM Guard's ML-backed scanners (in
the sibling ``llm_guard/`` package) are a second upgrade path that runs
locally without external accounts.

To add a new injection pattern, append a ``re.compile(...)`` to
``INJECTION_PATTERNS``. To add a new PII type, add an entry to
``PII_PATTERNS`` and a matching redaction string in ``PII_REDACTIONS``.
"""

import re

INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bignore\s+(all\s+)?(previous|prior|above)\s+instructions?\b", re.IGNORECASE),
    re.compile(r"\bdisregard\s+(all\s+)?(previous|prior|above)\s+instructions?\b", re.IGNORECASE),
    re.compile(r"\byou\s+are\s+now\s+", re.IGNORECASE),
    re.compile(r"\bact\s+as\s+(an?\s+)?", re.IGNORECASE),
    re.compile(r"\bpretend\s+(to\s+be|you\s+are)\b", re.IGNORECASE),
    re.compile(r"^\s*system\s*[:>]", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*assistant\s*[:>]", re.IGNORECASE | re.MULTILINE),
    re.compile(r"<\s*\|?\s*im_start\s*\|?\s*>", re.IGNORECASE),
    re.compile(
        r"\b(reveal|show|print|leak|repeat|tell\s+me)\s+(your|the)\s+"
        r"(system|initial|original|hidden|secret)\s+(prompt|instructions?|rules?|message)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(bypass|override|turn\s+off|disable|ignore)\s+(your|the|all)?\s*"
        r"(safety|guardrails?|filters?|restrictions?|content\s+policy|policies)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(jailbreak\s+mode|DAN\s+mode|developer\s+mode|do\s+anything\s+now)\b",
        re.IGNORECASE,
    ),
    # Capstone additions -------------------------------------------------
    # Memory-wipe: "forget everything you were told", "erase all prior
    # instructions". Requires a quantifier (everything/all/any) followed by
    # an instruction noun, so "clear the dust off my paddle" passes.
    re.compile(
        r"\b(forget|erase|wipe|clear)\s+(everything|all|any)\s+(of\s+)?(your|the|my)?\s*"
        r"(previous|prior|earlier|above)?\s*"
        r"(instructions?|rules?|context|guidelines|you\s+(were|have\s+been)\s+told)\b",
        re.IGNORECASE,
    ),
    # Credential / config exfiltration: "print your API key", "dump the
    # environment variables", "show me the .env file". The seed
    # reveal-prompt rule only covers prompts; this covers secrets.
    re.compile(
        r"\b(reveal|show|print|leak|give|output|dump|send|list)\s+(me\s+)?(your|the)\s+"
        r"(openai\s+)?(api[\s_-]?keys?|secret\s+keys?|access\s+tokens?|credentials|"
        r"env(ironment)?\s+variables?|\.env(\s+file)?)(?!\w)",
        re.IGNORECASE,
    ),
    # Chat-template smuggling: Llama-style [INST]/<<SYS>> delimiters or a
    # markdown header that opens a fake "### Instructions:" / "## SYSTEM"
    # block. Complements the seed ChatML <|im_start|> rule.
    re.compile(
        r"(\[\s*/?\s*(INST|SYS)\s*\]|<<\s*/?\s*SYS\s*>>|"
        r"^\s*#{2,}\s*(system|instructions?|new\s+instructions?)\b)",
        re.IGNORECASE | re.MULTILINE,
    ),
]

_IPV4_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"

PII_PATTERNS: dict[str, re.Pattern] = {
    # IPv4 first so dotted quads are redacted whole before the phone and
    # card scanners see their digit runs. Lookarounds reject partial
    # matches inside longer dotted numbers (e.g. "999.1.1.1").
    "ip_address": re.compile(
        rf"(?<![\d.]){_IPV4_OCTET}(?:\.{_IPV4_OCTET}){{3}}(?!\.?\d)"
    ),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}

PII_REDACTIONS: dict[str, str] = {
    "ip_address": "[REDACTED_IP]",
    "email": "[REDACTED_EMAIL]",
    "phone": "[REDACTED_PHONE]",
    "ssn": "[REDACTED_SSN]",
    "credit_card": "[REDACTED_CARD]",
}


def detect_prompt_injection(text: str) -> str | None:
    """Return a reason string if the input looks like prompt injection, else None."""
    for pattern in INJECTION_PATTERNS:
        match = pattern.search(text)
        if match:
            return f"prompt_injection: matched pattern {pattern.pattern!r}"
    return None


def detect_pii(text: str) -> tuple[str, list[str]]:
    """Redact known PII kinds from ``text``. Returns ``(redacted, kinds_found)``."""
    found: list[str] = []
    redacted = text
    for kind, pattern in PII_PATTERNS.items():
        if pattern.search(redacted):
            found.append(kind)
            redacted = pattern.sub(PII_REDACTIONS[kind], redacted)
    return redacted, found
