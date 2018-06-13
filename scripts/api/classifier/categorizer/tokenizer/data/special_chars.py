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
    },

    "cy": {
        "â": "a",
        "ê": "e",
        "î": "i",
        "ô": "o",
        "û": "u",
        "ŵ": "w",
        "ŷ": "y",
        "ä": "a",
        "ë": "e",
        "ï": "i",
        "ö": "o",
        "ü": "u",
        "ẅ": "w",
        "ÿ": "y",
        "à": "a",
        "è": "e",
        "ì": "i",
        "ò": "o",
        "ù": "u",
        "ẁ": "w",
        "ỳ": "y",
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ẃ": "w",
        "ý": "y"
    },
    "all": {
        "À": "A",
        "Á": "A",
        "Â": "A",
        "Ã": "A",
        "Ä": "A",
        "Å": "A",
        "Æ": "A",
        "Ç": "C",
        "È": "E",
        "É": "E",
        "Ê": "E",
        "Ë": "E",
        "Ì": "I",
        "Í": "I",
        "Î": "I",
        "Ï": "I",
        "Ð": "E",
        "Ñ": "N",
        "Ò": "O",
        "Ó": "O",
        "Ô": "O",
        "Õ": "O",
        "Ö": "O",
        "Ø": "O",
        "Ù": "U",
        "Ú": "U",
        "Û": "U",
        "Ü": "U",
        "Ý": "Y",
        "Þ": "P",
        "ß": "s",
        "à": "a",
        "á": "a",
        "â": "a",
        "ã": "a",
        "ä": "a",
        "å": "a",
        "æ": "a",
        "ç": "c",
        "è": "e",
        "é": "e",
        "ê": "e",
        "ë": "e",
        "ì": "i",
        "í": "i",
        "î": "i",
        "ï": "i",
        "ð": "e",
        "ñ": "n",
        "ò": "o",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ö": "o",
        "ø": "o",
        "ù": "u",
        "ú": "u",
        "û": "u",
        "ü": "u",
        "ý": "y",
        "þ": "p",
        "ÿ": "y",
        "Ā": "A",
        "ā": "a",
        "Ă": "A",
        "ă": "a",
        "Ą": "A",
        "ą": "a",
        "Ć": "C",
        "ć": "c",
        "Ĉ": "C",
        "ĉ": "c",
        "Ċ": "C",
        "ċ": "c",
        "Č": "C",
        "č": "c",
        "Ď": "D",
        "ď": "d",
        "Đ": "D",
        "đ": "d",
        "Ē": "E",
        "ē": "e",
        "Ĕ": "E",
        "ĕ": "e",
        "Ė": "E",
        "ė": "e",
        "Ę": "E",
        "ę": "e",
        "Ě": "E",
        "ě": "e",
        "Ĝ": "G",
        "ĝ": "g",
        "Ğ": "G",
        "ğ": "g",
        "Ġ": "G",
        "ġ": "g",
        "Ģ": "G",
        "ģ": "g",
        "Ĥ": "H",
        "ĥ": "h",
        "Ħ": "H",
        "ħ": "h",
        "Ĩ": "I",
        "ĩ": "i",
        "Ī": "I",
        "ī": "i",
        "Ĭ": "I",
        "ĭ": "i",
        "Į": "I",
        "į": "i",
        "İ": "I",
        "ı": "i",
        "Ĳ": "i",
        "ĳ": "i",
        "Ĵ": "J",
        "ĵ": "j",
        "Ķ": "K",
        "ķ": "k",
        "ĸ": "k",
        "Ĺ": "L",
        "ĺ": "l",
        "Ļ": "L",
        "ļ": "l",
        "Ľ": "L",
        "ľ": "l",
        "Ŀ": "L",
        "ŀ": "l",
        "Ł": "L",
        "ł": "l",
        "Ń": "N",
        "ń": "n",
        "Ņ": "N",
        "ņ": "n",
        "Ň": "N",
        "ň": "n",
        "ŉ": "n",
        "Ŋ": "N",
        "ŋ": "n",
        "Ō": "O",
        "ō": "o",
        "Ŏ": "O",
        "ŏ": "o",
        "Ő": "O",
        "ő": "o",
        "Œ": "O",
        "œ": "o",
        "Ŕ": "R",
        "ŕ": "r",
        "Ŗ": "R",
        "ŗ": "r",
        "Ř": "R",
        "ř": "r",
        "Ś": "S",
        "ś": "s",
        "Ŝ": "S",
        "ŝ": "s",
        "Ş": "S",
        "ş": "s",
        "Š": "S",
        "š": "s",
        "Ţ": "T",
        "ţ": "t",
        "Ť": "T",
        "ť": "t",
        "Ŧ": "T",
        "ŧ": "t",
        "Ũ": "U",
        "ũ": "u",
        "Ū": "U",
        "ū": "u",
        "Ŭ": "U",
        "ŭ": "u",
        "Ů": "U",
        "ů": "u",
        "Ű": "U",
        "ű": "u",
        "Ų": "U",
        "ų": "u",
        "Ŵ": "W",
        "ŵ": "w",
        "Ŷ": "Y",
        "ŷ": "y",
        "Ÿ": "Y",
        "Ź": "Z",
        "ź": "z",
        "Ż": "Z",
        "ż": "z",
        "Ž": "Z",
        "ž": "z",
        "ſ": "s"
    }
}

patterns = {
    "non_alpha_numeric": r"[^A-z^0-9^ ^\-^_]|\\|\^|\]|\[",
    "alpha_only": r"[A-z]",
    "alpha_upper": r"[A-Z]",
    "alpha_lower": r"[a-z]",
    "numeric": r"[0-9]",
    "punctuation": r"[’'()[\]{}<>:,‒–—―…!.«»\-‐?‘’“”;/⁄␠·&@*\\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※]",
    "list_boundries": r"concentrate| or | and |[\/\n,;&.\\]+",
    "whitespace": r"[ \t\b\n]+"
}


def re_pattern(key):
    return re.compile(patterns[key])
