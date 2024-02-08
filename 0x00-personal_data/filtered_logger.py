#!/usr/bin/env python3
"""
returns the log message obfuscated
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    fields - list od strings representing all fields to obfuscate
    redaction -  a string representing by what the field will be obfuscated
    message - a string representing the log line
    separator:string by which character is separating all fields in the lo
g
    """
    pattern = re.compile(r'password=(\w[a-z]+)|\d{2}\/\d{2}\/\d{4}')
    for mess in message:
        result = re.sub(pattern, lambda match: redaction if match.group(1) else redaction, message)
    return result
