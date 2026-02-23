"""
Enterprise SQL Safety Layer
Author: Usman Sharif

Purpose:
---------
Provides validation and sanitization of SQL queries before execution.
Prevents destructive operations and enforces read-only policy.

Enterprise Rules:
-----------------
- Only SELECT statements allowed
- No DDL (DROP, ALTER)
- No DML (INSERT, UPDATE, DELETE)
- Optional: restrict multi-statement execution
"""

import re


class SQLSafetyValidator:
    """
    Enterprise-level SQL safety validator.
    """

    FORBIDDEN_KEYWORDS = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "ATTACH",
        "DETACH"
    ]

    def __init__(self, allow_select_only: bool = True):
        self.allow_select_only = allow_select_only

    def validate(self, query: str) -> bool:
        """
        Validate incoming SQL query.
        Raises ValueError if unsafe.
        """

        if not query or not query.strip():
            raise ValueError("Empty SQL query is not allowed.")

        normalized_query = query.strip().upper()

        # Rule 1: Only SELECT allowed (if enabled)
        if self.allow_select_only:
            if not normalized_query.startswith("SELECT"):
                raise ValueError(
                    "Only SELECT queries are permitted in this mode."
                )

        # Rule 2: Block forbidden keywords
        for keyword in self.FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{keyword}\b", normalized_query):
                raise ValueError(
                    f"Forbidden SQL keyword detected: {keyword}"
                )

        # Rule 3: Block multiple statements (avoid injection chaining)
        if ";" in normalized_query[:-1]:
            raise ValueError(
                "Multiple SQL statements detected. Not allowed."
            )

        return True