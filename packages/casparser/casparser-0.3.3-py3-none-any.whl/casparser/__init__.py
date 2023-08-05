try:
    from .parsers.mupdf import read_cas_pdf
except (ImportError, ModuleNotFoundError):
    from .parsers.pdfminer import read_cas_pdf

from .types import CASParserDataType
from .__version__ import __version__

__all__ = [
    "read_cas_pdf",
    "__version__",
    "CASParserDataType",
]
