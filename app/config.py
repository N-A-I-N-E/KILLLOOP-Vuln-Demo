"""Hardcoded secrets — Gitleaks / Semgrep should flag these."""

DATABASE_URL = "postgresql://admin:SuperSecretP@ssw0rd123!@localhost/killloop_demo"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
GITHUB_PAT = "ghp_0000000000000000000000000000000000ABCD"


def load_settings():
    return {
        "app_name": "killloop-vuln-demo",
        "database_url": DATABASE_URL,
        "aws_key": AWS_ACCESS_KEY_ID,
    }
