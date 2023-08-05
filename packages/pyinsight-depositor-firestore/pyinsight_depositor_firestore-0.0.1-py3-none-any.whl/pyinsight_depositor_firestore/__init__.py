# Module Import
from pyinsight_depositor_firestore import firestore_depositor

# Object Import
from pyinsight_depositor_firestore.firestore_depositor import FirestoreDepositor

# Element Listing
__all__ = ['FirestoreDepositor']

VERSION = (0, 0, 1)

def get_version():
    """Return the VERSION as a string.
    For example, if `VERSION == (0, 10, 7)`, return '0.10.7'.
    """
    return ".".join(map(str, VERSION))

__version__ = get_version()