import re

special_chars = {
  "es": {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ü": "u",
    "ñ": "n",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ü": "U",
    "Ñ": "N",
    "¿": None,
    "¡": None
  },

  "fr": {
    "é": "e",
    "à": "a",
    "è": "e",
    "ù": "u",
    "â": "a",
    "ê": "e",
    "î": "i",
    "ô": "o",
    "û": "u",
    "ç": "c",
    "ë": "e",
    "ï": "i",
    "ü": "u",
    "œ": "oe",
    "É": "E",
    "À": "A",
    "È": "E",
    "Ù": "U",
    "Â": "A",
    "Ê": "E",
    "Î": "I",
    "Ô": "O",
    "Û": "U",
    "Ç": "C",
    "Ë": "E",
    "Ï": "I",
    "Ü": "U",
    "Œ": "OE"
  }
}

patterns = {
  "non_alpha_numeric": r"[^A-z^0-9^ ^\-^_]|\\|\^|\]|\[",
  "alpha_only": r"[A-z]",
  "alpha_upper": r"[A-Z]",
  "alpha_lower": r"[a-z]",
  "numeric": r"[0-9]",
  "punctuation": r"[’'()[\]{}<>:,‒–—―…!.«»\-‐?‘’“”;/⁄␠·&@*\\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※]",
  "list_boundries": r"concentrate|or|and|[\/\n,;&.\\]+",
  "whitespace": r"[ \t\b\n]+"
}

def re_pattern(key):
    return re.compile(patterns[key])

