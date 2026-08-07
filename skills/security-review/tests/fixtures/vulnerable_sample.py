"""DO NOT EXECUTE, IMPORT INTO PRODUCTION, OR DEPLOY.

This intentionally vulnerable, synthetic file exists only as static review input.
All values are fictional. The token marker below is NOT A REAL SECRET.
"""

import os

DEMO_API_TOKEN = "NOT_A_REAL_DEMO_TOKEN_VALUE_0000000000"


def load_tenant_record(requested_tenant: str, record: dict) -> dict:
    """Synthetic authorization flaw: requested_tenant is never checked."""
    return record


def build_user_query(user_name: str) -> str:
    """Synthetic SQL-injection flaw: untrusted input is concatenated."""
    return "SELECT * FROM users WHERE name = '" + user_name + "'"


def unsafe_shell(command: str) -> int:
    """Synthetic command-injection flaw: untrusted command reaches a shell."""
    return os.system(command)


def process_webhook(event_id: str, payload: dict) -> dict:
    """Synthetic replay flaw: event_id and signature are not validated."""
    return payload


def agent_execute(model_output: str) -> int:
    """Synthetic agentic flaw: model output crosses directly into authority."""
    return os.system(model_output)


if __name__ == "__main__":
    raise SystemExit("Synthetic security-review fixture: DO NOT EXECUTE")
