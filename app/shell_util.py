import os


def run_unsafe_command(filename: str) -> str:
    # CWE-78 — command injection
    os.system(f"echo processing {filename}")
    return f"ran: cat {filename}"
