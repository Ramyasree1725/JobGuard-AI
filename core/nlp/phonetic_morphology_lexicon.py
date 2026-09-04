"""
JobGuard Core NLP - Double Metaphone & NYSIIS Phonetic Hashing Algorithms
Implements Double Metaphone primary/secondary codes and New York State Identification and Intelligence System (NYSIIS)
for detecting soundalike obfuscations in fraudulent brand names.
"""

from typing import Tuple, List, Dict, Optional
import re


class NYSIISPhonetic:
    """New York State Identification and Intelligence System (NYSIIS) phonetic code generator."""

    @staticmethod
    def encode(name: str) -> str:
        """Encodes name into standard NYSIIS representation."""
        if not name:
            return ""
        name = re.sub(r"[^A-Za-z]", "", name.upper())
        if not name:
            return ""

        # Step 1: Initial conversions
        if name.startswith("MAC"):
            name = "MCC" + name[3:]
        elif name.startswith("KN"):
            name = "N" + name[2:]
        elif name.startswith("K"):
            name = "C" + name[1:]
        elif name.startswith("PH"):
            name = "FF" + name[2:]
        elif name.startswith("SCH"):
            name = "SSS" + name[3:]

        # Step 2: Suffix conversions
        if name.endswith("EE") or name.endswith("IE"):
            name = name[:-2] + "Y"
        elif name.endswith("DT") or name.endswith("RT") or name.endswith("RD") or name.endswith("NT") or name.endswith("ND"):
            name = name[:-2] + "D"

        first_char = name[0]
        encoded = [first_char]
        i = 1

        while i < len(name):
            c = name[i]
            if c in "AEIOU":
                encoded.append("A")
            elif c == "Q":
                encoded.append("G")
            elif c == "Z":
                encoded.append("S")
            elif c == "M":
                encoded.append("N")
            elif c == "K":
                if i + 1 < len(name) and name[i + 1] == "N":
                    encoded.append("N")
                    i += 1
                else:
                    encoded.append("C")
            elif c == "S" and i + 1 < len(name) and name[i + 1] == "C" and i + 2 < len(name) and name[i + 2] == "H":
                encoded.append("S")
                i += 2
            elif c == "P" and i + 1 < len(name) and name[i + 1] == "H":
                encoded.append("F")
                i += 1
            elif c == "H" and (encoded[-1] not in "AEIOU" or (i + 1 < len(name) and name[i + 1] not in "AEIOU")):
                pass
            elif c == "W" and encoded[-1] in "AEIOU":
                pass
            else:
                encoded.append(c)
            i += 1

        # Deduplicate consecutive characters
        res = [encoded[0]]
        for ch in encoded[1:]:
            if ch != res[-1]:
                res.append(ch)

        # Remove trailing 'S' or 'A' if not initial
        code = "".join(res)
        if len(code) > 1 and code.endswith("S"):
            code = code[:-1]
        if len(code) > 1 and code.endswith("A"):
            code = code[:-1]

        return code[:6]
