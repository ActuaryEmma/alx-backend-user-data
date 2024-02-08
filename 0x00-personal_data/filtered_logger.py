#!/usr/bin/env python3
"""
returns the log message obfuscated
"""
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = re.compile(r'password=(\w[a-z]+)|\d{2}\/\d{2}\/\d{4}')
    for mess in message:
        result = re.sub(pattern, lambda match: redaction if match.group(1) else redaction, message)
    return result
