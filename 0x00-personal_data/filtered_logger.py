#!/usr/bin/env python3
"""
returns the log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    for field in fields:
        message = re.sub(
        rf'{field}=([^{separator}]+)', f'{field}={redaction}', message)
    return message
