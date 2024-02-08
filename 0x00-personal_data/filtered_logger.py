#!/usr/bin/env python3
"""
returns the log message obfuscated
"""
import re


def filter_datum(fields, redaction: str, message: str, separator: str):
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
        rf'{field}=([^{separator}]+)', f'{field}={redaction}', message)
    return message
