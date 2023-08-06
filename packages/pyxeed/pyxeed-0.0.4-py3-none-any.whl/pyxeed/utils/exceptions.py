"""
Xeed Module Error Code Description:
XED-000001: Extractor Type Error
XED-000002: Messager Type Error
XED-000003: Translator Type Error
XED-000004: No translator Error
XED-000005: Listener Type Error
"""
class XeedTypeError(Exception): pass
class XeedDataSpecError(Exception): pass