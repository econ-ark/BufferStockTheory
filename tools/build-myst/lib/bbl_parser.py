"""Parse `\\harvarditem`-style bibliographies (econark / Harvard format).

The output of `bibtex` for the BST paper produces entries like:

    \\harvarditem[Bewley]{Bewley}{1977}{bewleyPIH}
    \\textsc{Bewley, Truman~F.}  (1977): ``The Permanent Income ...,''
      \\emph{Journal of Economic Theory}, 16, 252--292.

This parser walks `\\thebibliography ... \\end{thebibliography}` and produces
a deterministic dict `{citekey: CitationEntry}` where CitationEntry has:

- `key`: the citation key (4th \\harvarditem arg)
- `short_authors`: 1st arg (or 2nd if 1st is empty) — used for `\\citep` short form
- `long_authors`: 2nd arg — used for `\\citet` / "Author (Year)" form
- `year`: 3rd arg
- `body`: the rendered prose after the \\harvarditem call, cleaned to plain text
- `short`: rendered "(Author, Year)" form
- `long`: rendered "Author (Year)" form

The cleaning of `body` strips common LaTeX commands so the rendered References
section is plain markdown.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional


@dataclass
class CitationEntry:
    key: str
    short_authors: str
    long_authors: str
    year: str
    body: str = ""

    @property
    def short(self) -> str:
        # \\citep{foo}  → "(Author, Year)"
        return f"({self.short_authors}, {self.year})"

    @property
    def long(self) -> str:
        # \\citet{foo}  → "Author (Year)"
        return f"{self.long_authors} ({self.year})"


def _balanced_braces(s: str, start: int) -> int:
    """Given s[start] == '{', return index *after* the matching '}'."""
    assert s[start] == "{"
    depth = 0
    i = start
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("Unbalanced braces starting at offset %d" % start)


def _take_optional(s: str, start: int) -> tuple[Optional[str], int]:
    """If s[start] == '[', consume optional [..] and return (content, end)."""
    if start >= len(s) or s[start] != "[":
        return None, start
    depth = 0
    i = start
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            i += 2
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    raise ValueError("Unbalanced [...] starting at offset %d" % start)


def _take_braced(s: str, start: int) -> tuple[str, int]:
    """Consume `{...}` and return (content, end_after_close)."""
    if start >= len(s) or s[start] != "{":
        raise ValueError(f"expected '{{' at {start}, got {s[start:start+10]!r}")
    end = _balanced_braces(s, start)
    return s[start + 1:end - 1], end


def _balanced_replace(text: str, command: str, fmt: str) -> str:
    """Replace `\\command{...}` with `fmt.format(arg)`, handling nested braces.

    `fmt` is a Python format-string with `{}` for the argument body
    (e.g. `"*{}*"` for italics).
    """
    out: list[str] = []
    i = 0
    n = len(text)
    needle = "\\" + command
    while i < n:
        idx = text.find(needle, i)
        if idx == -1:
            out.append(text[i:])
            break
        end_name = idx + len(needle)
        if end_name < n and (text[end_name].isalpha() or text[end_name] == "@"):
            out.append(text[i:end_name])
            i = end_name
            continue
        out.append(text[i:idx])
        cursor = end_name
        while cursor < n and text[cursor] in " \t\n":
            cursor += 1
        if cursor >= n or text[cursor] != "{":
            i = cursor
            continue
        try:
            end = _balanced_braces(text, cursor)
        except ValueError:
            i = cursor
            continue
        body = text[cursor + 1:end - 1]
        # Recursively clean nested commands of the same kind (handles
        # `\textsc{Schmitt-Groh{\'e}...}`).
        out.append(fmt.format(body))
        i = end
    return "".join(out)


# LaTeX accent -> Unicode lookup. Each key is the LaTeX accent macro
# (without the leading backslash); each value maps a base letter to its
# accented form. Covers the accents that appear in this paper's bibliography
# and acknowledgements (Schmitt-Grohé, Rincón, Rodríguez, Durán, etc.); extend
# as new sources arrive.
LATEX_ACCENT: dict[str, dict[str, str]] = {
    "'":  {"a": "á", "e": "é", "i": "í", "o": "ó",
           "u": "ú", "y": "ý",
           "A": "Á", "E": "É", "I": "Í", "O": "Ó",
           "U": "Ú", "Y": "Ý",
           "c": "ć", "C": "Ć", "n": "ń", "N": "Ń",
           "s": "ś", "S": "Ś", "z": "ź", "Z": "Ź"},
    "`":  {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù",
           "A": "À", "E": "È", "I": "Ì", "O": "Ò", "U": "Ù"},
    '"':  {"a": "ä", "e": "ë", "i": "ï", "o": "ö",
           "u": "ü", "y": "ÿ",
           "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö",
           "U": "Ü", "Y": "Ÿ"},
    "^":  {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û",
           "A": "Â", "E": "Ê", "I": "Î", "O": "Ô", "U": "Û"},
    "~":  {"a": "ã", "n": "ñ", "o": "õ",
           "A": "Ã", "N": "Ñ", "O": "Õ"},
    "=":  {"a": "ā", "e": "ē", "i": "ī", "o": "ō", "u": "ū",
           "A": "Ā", "E": "Ē", "I": "Ī", "O": "Ō", "U": "Ū"},
    ".":  {"e": "ė", "z": "ż",
           "E": "Ė", "Z": "Ż", "I": "İ"},
    "v":  {"c": "č", "s": "š", "z": "ž", "r": "ř",
           "n": "ň", "l": "ľ", "t": "ť", "d": "ď",
           "C": "Č", "S": "Š", "Z": "Ž", "R": "Ř",
           "N": "Ň", "L": "Ľ", "T": "Ť", "D": "Ď",
           "e": "ě", "E": "Ě"},
    "u":  {"a": "ă", "e": "ĕ", "g": "ğ",
           "A": "Ă", "E": "Ĕ", "G": "Ğ"},
    "c":  {"c": "ç", "s": "ş", "C": "Ç", "S": "Ş"},  # cedilla
    "k":  {"a": "ą", "e": "ę", "A": "Ą", "E": "Ę"},  # ogonek
}

# Special LaTeX letter-name macros that don't take a base letter.
LATEX_LETTER: dict[str, str] = {
    "i":  "ı",  # \i -> dotless i
    "j":  "ȷ",  # \j -> dotless j
    "l":  "ł", "L":  "Ł",   # Polish stroke L
    "o":  "ø", "O":  "Ø",   # Danish/Norwegian O slash
    "ae": "æ", "AE": "Æ",
    "oe": "œ", "OE": "Œ",
    "ss": "ß",                                # German sharp s
    "aa": "å", "AA": "Å",   # Scandinavian A-ring
    "TH": "Þ", "th": "þ",   # Icelandic Thorn
    "DH": "Ð", "dh": "ð",   # Icelandic Eth
}


def _apply_latex_accents(text: str) -> str:
    r"""Replace LaTeX accent constructs with Unicode equivalents.

    Handles the common forms:
        \'o   ->  ó         \v{c}    -> č         \ss   -> ß
        \'{o} ->  ó         {\v{c}}  -> č         {\ss} -> ß
        {\'o} ->  ó         \'\i    -> í         (etc.)

    Anything not in LATEX_ACCENT / LATEX_LETTER passes through untouched —
    better to leak the source than emit a wrong character.
    """
    # Pass 1: braced multi-letter accents like {\v{c}}, {\u{g}}, {\c{c}}
    def _braced_multi(m):
        accent, base = m.group(1), m.group(2).lstrip("\\")
        return LATEX_ACCENT.get(accent, {}).get(base, m.group(0))
    text = re.sub(r"\{\\([vuck])\{?(\\?[a-zA-Z])\}?\}", _braced_multi, text)

    # Pass 2: braced punctuation accents like {\'o}, {\'\i}
    def _braced_punct(m):
        accent, base = m.group(1), m.group(2).lstrip("\\")
        return LATEX_ACCENT.get(accent, {}).get(base, m.group(0))
    text = re.sub(r"""\{\\(['`"^~=.])\\?([a-zA-Z])\}""", _braced_punct, text)

    # Pass 3: braced letter-name macros like {\ss}, {\TH}, {\i}
    def _braced_letter(m):
        return LATEX_LETTER.get(m.group(1), m.group(0))
    text = re.sub(r"\{\\([a-zA-Z]{1,2})\}", _braced_letter, text)

    # Pass 4: bare \v{c}, \u{g}, \c{c}, \k{a}
    def _bare_multi(m):
        accent, base = m.group(1), m.group(2).lstrip("\\")
        return LATEX_ACCENT.get(accent, {}).get(base, m.group(0))
    text = re.sub(r"\\([vuck])\{(\\?[a-zA-Z])\}", _bare_multi, text)

    # Pass 5: bare \'o, \'{o}, \"a, etc.
    def _bare_punct(m):
        accent = m.group(1)
        base = (m.group(2) or m.group(3) or "").lstrip("\\")
        return LATEX_ACCENT.get(accent, {}).get(base, m.group(0))
    text = re.sub(
        r"""\\(['`"^~=.])(?:\{(\\?[a-zA-Z])\}|(\\?[a-zA-Z]))""",
        _bare_punct,
        text,
    )

    # Pass 6: bare letter-name macros like \ss, \i (only when followed by a
    # non-letter, so we don't eat \section or \in etc.)
    def _bare_letter(m):
        return LATEX_LETTER.get(m.group(1), m.group(0))
    text = re.sub(
        r"\\(ss|aa|AA|ae|AE|oe|OE|TH|th|DH|dh|i|j|l|L|o|O)(?![a-zA-Z])",
        _bare_letter, text)

    # Pass 7: strip leftover singleton braces around single Unicode chars.
    # The `{\'{o}}` form (extra braces around the base) leaves `{ó}` after
    # passes 1–5; this pass unwraps it. Limited to single-char interior to
    # avoid swallowing intentional grouping like `{Title}`.
    text = re.sub(r"\{(\S)\}", r"\1", text)

    return text


def _strip_extra_braces_in_emphasis(text: str) -> str:
    """Convert ``*{X}*`` -> ``*X*`` and ``**{X}**`` -> ``**X**``.

    Sources sometimes write ``\emph{{Title}}`` (extra braces for grouping in
    LaTeX); _balanced_replace then emits ``*{Title}*`` since it captures the
    whole inner content including the inner braces. Strip a single surrounding
    pair when the inner content is a balanced span.
    """
    text = re.sub(r"\*\{([^{}]+)\}\*", r"*\1*", text)
    text = re.sub(r"\*\*\{([^{}]+)\}\*\*", r"**\1**", text)
    return text


_LITERAL_CLEAN = [
    (re.compile(r"\\BySame"),             r"———"),
    (re.compile(r"\\&"),                  r"&"),
    (re.compile(r"\\%"),                  r"%"),
    (re.compile(r"\\\$"),                 r"$"),
    (re.compile(r"\\#"),                  r"#"),
    (re.compile(r"\\_"),                  r"_"),
    # accent rules are handled by _apply_latex_accents()
    (re.compile(r"\\noopsort\{[^{}]*\}"), r""),
    (re.compile(r"\\providecommand\{[^{}]*\}\{[^{}]*\}"), r""),
    (re.compile(r"~"),                    r" "),
    (re.compile(r"--"),                   r"–"),
    (re.compile(r"``"),                   "\u201c"),
    (re.compile(r"''"),                   "\u201d"),
    (re.compile(r"\\\s"),                 r" "),
    (re.compile(r"\\\\"),                 r" "),
    (re.compile(r"\\?\{\\?-\\?\}"),       r""),       # {\-} / {-} → "" (hyphenation hint)
    (re.compile(r"\\-"),                  r""),       # bare \- (TeX hyphenation hint)
    (re.compile(r"\{([A-Za-z]+)\}"),      r"\1"),     # {C}arroll / {and} → Carroll / and
    (re.compile(r"\s+"),                  r" "),
]


def _clean_body(raw: str) -> str:
    out = raw
    # Balanced-brace passes for commands whose arguments may contain other braces.
    out = _balanced_replace(out, "textsc",       "{}")
    out = _balanced_replace(out, "emph",         "*{}*")
    out = _balanced_replace(out, "textit",       "*{}*")
    out = _balanced_replace(out, "textbf",       "**{}**")
    out = _balanced_replace(out, "singleletter", "{}")
    out = _balanced_replace(out, "url",          "<{}>")
    # Strip surrounding braces inside emphasis from \emph{{...}} forms.
    out = _strip_extra_braces_in_emphasis(out)
    # Convert LaTeX accents to Unicode (Schmitt-Grohé, Rincón, etc.).
    out = _apply_latex_accents(out)
    # Remaining literal substitutions.
    for pat, repl in _LITERAL_CLEAN:
        out = pat.sub(repl, out)
    return out.strip().rstrip(",.; ")


def parse_bbl(bbl_text: str) -> Dict[str, CitationEntry]:
    """Parse a `.bbl` (or inlined `\\thebibliography` block) into a citation map."""
    # Restrict to the body of \\begin{thebibliography} ... \\end{thebibliography}
    m = re.search(r"\\begin\{thebibliography\}", bbl_text)
    if m:
        body_start = bbl_text.find("}", m.end()) + 1
    else:
        body_start = 0
    end = bbl_text.find(r"\end{thebibliography}", body_start)
    if end == -1:
        end = len(bbl_text)
    body = bbl_text[body_start:end]

    entries: Dict[str, CitationEntry] = {}
    i = 0
    while True:
        idx = body.find(r"\harvarditem", i)
        if idx == -1:
            break
        cursor = idx + len(r"\harvarditem")
        # Harvard format: \harvarditem[short]{long}{year}{key}
        # The optional [short] is the parenthetical-citation form;
        # {long} is the full-citation form (used for \citet etc.).
        opt, cursor = _take_optional(body, cursor)
        a_long, cursor = _take_braced(body, cursor)
        a_year, cursor = _take_braced(body, cursor)
        a_key,  cursor = _take_braced(body, cursor)

        # The body of the entry runs until the next \\harvarditem or end of bib.
        next_idx = body.find(r"\harvarditem", cursor)
        if next_idx == -1:
            next_idx = len(body)
        raw_body = body[cursor:next_idx]
        cleaned = _clean_body(raw_body)

        # Author fields are raw \\harvarditem args — they bypass _clean_body,
        # so we apply the same LaTeX-accent / hyphen-hint / extra-brace
        # normalisations here. Without this the rendered citations show
        # `Rinc{\\'o}n-Zapatero` literally.
        def _normalize_author(s: str) -> str:
            s = _apply_latex_accents(s)
            s = re.sub(r"\\-", "", s)              # bare \- hyphenation hint
            s = re.sub(r"\{([\w]+)\}", r"\1", s)   # {C}arroll → Carroll (incl. unicode)
            s = re.sub(r"\\ ", " ", s)             # \  → space
            return s.strip()

        short_authors = _normalize_author(opt if opt is not None else a_long)
        long_authors = _normalize_author(a_long)
        year = a_year.strip()
        key = a_key.strip()
        entries[key] = CitationEntry(
            key=key,
            short_authors=short_authors,
            long_authors=long_authors,
            year=year,
            body=cleaned,
        )
        i = next_idx
    return entries


def parse_bbl_file(path: str) -> Dict[str, CitationEntry]:
    with open(path, "r", encoding="utf-8") as f:
        return parse_bbl(f.read())
