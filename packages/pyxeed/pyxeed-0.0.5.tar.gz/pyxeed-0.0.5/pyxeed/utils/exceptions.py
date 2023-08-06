"""
Xeed Module Error Code Description:
XED-000001: Extractor Type Error
XED-000002: Sender Type Error
XED-000003: Translator Type Error
XED-000004: No translator Error
XED-000005: Listener Type Error
XED-000006: Decoder Destination Error
XED-000007: Decoder Source Error
XED-000008: List Format Error
XED-000009: Record Format Error
XED-000010: Format Souorce Error
XED-000011: Format Destination Error
XED-000012: Decoder Type Error
XED-000013: Formatter Type Error
XED-000014: X-I-A Header Error
XED-000015: Pusher Type Error
"""
class XeedTypeError(Exception): pass
class XeedDataSpecError(Exception): pass
class XeedDecodeError(Exception): pass
class XeedFormatError(Exception): pass