"""Rebuild the WordPress-safe embed from the standalone quiz.

Run from the repo root:  python3 jdms-utilities-quiz/build/build_embed.py

Copies the ROLES, GOALS and CHALLENGES data from jdms-utilities-quiz/index.html
into embed-template.html, then checks for anything WordPress would mangle and
writes jdms-utilities-quiz/jdms-utilities-quiz-embed.html.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUIZ = HERE.parent / "index.html"
TEMPLATE = HERE / "embed-template.html"
OUT = HERE.parent / "jdms-utilities-quiz-embed.html"

quiz = QUIZ.read_text(encoding="utf-8")
template = TEMPLATE.read_text(encoding="utf-8")

# Pull the three data objects out of the standalone quiz.
start = quiz.index("const jdmsuRoles")
end = quiz.index("/* ------", quiz.index("const jdmsuChallenges"))
data = re.sub(r"/\*.*?\*/", "", quiz[start:end], flags=re.S)
data = (data.replace("const jdmsuRoles", "var ROLES")
            .replace("const jdmsuGoals", "var GOALS")
            .replace("const jdmsuChallenges", "var CHALLENGES"))

# WordPress re-encodes & and curly punctuation, so write them as \u escapes.
data = (data.replace("&", "\\u0026").replace("\u2192", "\\u2192")
            .replace("\u2019", "\\u2019").replace("\u2014", "\\u2014"))
non_ascii = {ch for ch in data if ord(ch) > 127}
if non_ascii:
    sys.exit(f"Non-ASCII characters in quiz data; add an escape for: {non_ascii}")
data = "\n".join("  " + line.rstrip() for line in data.split("\n") if line.strip())

out = template.replace("__DATA__", data)
script = out[out.index("<script>") + 8:out.index("</script>")]
style = out[out.index("<style>") + 7:out.index("</style>")]

# Anything here breaks once WordPress tidies the pasted code.
problems = []
for name, part in (("script", script), ("style", style)):
    for bad in ("&&", "<", ">"):
        for m in re.finditer(re.escape(bad), part):
            problems.append(f"{name} has {bad!r}: ...{part[max(0, m.start() - 40):m.end() + 20]!r}")
if "//" in script:
    problems.append("script has a // comment or URL; use /* */ comments")
if "\n\n" in out:
    problems.append("blank line (WordPress turns it into a <p> tag)")
if "onclick" in out:
    problems.append("onclick attribute (WordPress may strip it); use data-jdmsu instead")
if problems:
    sys.exit("\n".join(problems))


def one_line(part):
    return " ".join(line.strip() for line in part.split("\n") if line.strip())


# Single-line script and style, so WordPress has no line breaks to turn into <br>.
out = (out.replace("<script>" + script + "</script>", "<script>" + one_line(script) + "</script>")
          .replace("<style>" + style + "</style>", "<style>" + one_line(style) + "</style>"))
OUT.write_text(out, encoding="utf-8")
print(f"Wrote {OUT.name}: {len(out)} chars, {out.count(chr(10))} lines")
