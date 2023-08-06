"""Pattoo helper for data handling."""

# Standard libraries
import hashlib

# pattoo imports
from .constants import DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT


def hashstring(string, sha=256, utf8=False):
    """Create a UTF encoded SHA hash string.

    Args:
        string: String to hash
        length: Length of SHA hash
        utf8: Return utf8 encoded string if true

    Returns:
        result: Result of hash

    """
    # Initialize key variables
    listing = [1, 224, 384, 256, 512]

    # Select SHA type
    if sha in listing:
        index = listing.index(sha)
        if listing[index] == 1:
            hasher = hashlib.sha1()
        elif listing[index] == 224:
            hasher = hashlib.sha224()
        elif listing[index] == 384:
            hasher = hashlib.sha384()
        elif listing[index] == 512:
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

    # Encode the string
    hasher.update(bytes(string.encode()))
    target_hash = hasher.hexdigest()
    if utf8 is True:
        result = target_hash.encode()
    else:
        result = target_hash

    # Return
    return result


def is_numeric(val):
    """Check if argument is a number.

    Args:
        val: String to check

    Returns:
        True if a number

    """
    # Try edge case
    if val is True:
        return False
    if val is False:
        return False
    if val is None:
        return False

    # Try conversions
    try:
        float(val)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
    except:
        return False


def is_data_type_numeric(data_type):
    """Check if data_type argument is a number.

    Args:
        data_type: Value to check

    Returns:
        result: True if a number.

    """
    # Try edge case
    result = False not in [
        data_type in [DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT],
        is_numeric(data_type) is True]
    return result
