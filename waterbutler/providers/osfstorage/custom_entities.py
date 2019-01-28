"""Custom character entity references, based on MUFI Character Database.
https://skaldic.abdn.ac.uk/db.php?if=mufi&table=mufi_char"""

__all__ = ['name2codepoint']


# maps the Medieval character entity name to the Unicode code point
name2codepoint = {
    'ndot': 0x001e45,   # latin small letter n with dot above
    'Ndot': 0x001e44,   # latin capital letter N with dot above
}
