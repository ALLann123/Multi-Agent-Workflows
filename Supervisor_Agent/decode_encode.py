#!usr/bin/python3
import base64

#create the base64 conversion tool
def convert_from_b64(s):
    try:
        decoded = base64.b64decode(s, validate=True)
        if base64.b64encode(decoded).decode().rstrip('=') == s.rstrip('='):
            return decoded.decode(errors='ignore')
    except Exception as e:
    	return e
    
#convert_to_base64
def convert_to_b64(s):
	encoded = base64.b64encode(s.encode()).decode()
	return encoded

#identify the encoding
def detect_base(value: str) -> str:
    """
    Detect whether the given string is hex, binary, or decimal.
    Returns: 'hex', 'binary', 'decimal', or 'unknown'
    """
    value = value.strip().lower()
    if value.startswith("0x"):
        return "hex"
    if value.startswith("0b"):
        return "binary"
    if all(c in "01" for c in value):
        return "binary"
    if all(c in "0123456789abcdef" for c in value):
        try:
            int(value, 10)
            return "decimal"
        except ValueError:
            return "hex"
    return "unknown"

#from hex, deci and binary
def convert_number(value: str, source_format: str, target_format: str) -> str:
    """
    Convert a number from source_format ('hex', 'binary', 'decimal')
    to target_format ('hex', 'binary', 'decimal').
    """
    # Normalize the input
    value = value.strip().lower()

    # Convert to integer
    if source_format == "hex":
        num = int(value, 16)
    elif source_format == "binary":
        num = int(value, 2)
    elif source_format == "decimal":
        num = int(value)
    else:
        raise ValueError("Unknown source format.")

    # Convert to target format
    if target_format == "decimal":
        return str(num)
    elif target_format == "hex":
        return hex(num)
    elif target_format == "binary":
        return bin(num)
    else:
        raise ValueError("Unsupported target format.")

