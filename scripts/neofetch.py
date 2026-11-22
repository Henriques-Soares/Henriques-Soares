#!/usr/bin/env python3
"""Generate the neofetch-style profile card (dark and light SVG).

Layout idea inspired by Andrew Grant's profile (github.com/Andrew6rant); this is an
independent implementation. Uses only the Python standard library.

Live data comes from the GitHub GraphQL API (GITHUB_TOKEN). If the API is unavailable,
the last good values in assets/stats.json are used, so the card never breaks.
"""
import datetime as dt
import json
import os
import pathlib
import urllib.request
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
LOGIN = os.environ.get("GH_USER", "Henriques-Soares")
PROFILE_REPO = LOGIN
RW = 58  # width of the right column, in characters

# --------------------------------------------------------------------------- content
PROFILE = [
    ("header", "henriques@soares"),
    ("kv", "OS", "São Paulo, Brazil · Angolan roots"),
    ("kv", "Uptime", "{uptime}"),
    ("kv", "Host", "Bradesco · IT Risk Advisory"),
    ("kv", "Kernel", "Computer Engineering @ FIAP"),
    ("kv", "Shell", "Security Engineering · GRC"),
    ("blank",),
    ("kv", "Languages.Programming", "Java, Python, TypeScript, C#"),
    ("kv", "Languages.Security", "PKI, mTLS, WireGuard, SIEM"),
    ("kv", "Frameworks", "MITRE ATT&CK, OWASP Top 10"),
    ("kv", "Infra", "Docker, PostgreSQL, Linux"),
    ("blank",),
    ("section", "Contact"),
    ("kv", "LinkedIn", "in/henriques-soares"),
    ("kv", "GitHub", "Henriques-Soares"),
    ("blank",),
    ("section", "GitHub Stats"),
    ("stats",),
]

PALETTES = {
    "dark": dict(card="#161b22", border="#30363d", text="#c9d1d9", key="#f5b83d",
                 value="#7dd3fc", cc="#4b5563", accent="#3fb950", a1="#67e8f9", a2="#f5b83d"),
    "light": dict(card="#f6f8fa", border="#d0d7de", text="#24292f", key="#b45309",
                  value="#0550ae", cc="#8c959f", accent="#1a7f37", a1="#0e7490", a2="#b45309"),
}


# --------------------------------------------------------------------------- data
def gql(query, variables):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("no GITHUB_TOKEN")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-neofetch"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]


QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    contributionsCollection { contributionCalendar { totalContributions } }
    repositoriesContributedTo(first: 1, includeUserRepositories: false,
      contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
      orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name pushedAt stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}"""


def fetch_stats():
    u = gql(QUERY, {"login": LOGIN})["user"]
    repos = u["repositories"]["nodes"]
    langs = {}
    for r in repos:
        if r["name"] == PROFILE_REPO:
            continue
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    latest = next((r for r in repos if r["name"] != PROFILE_REPO), None)
    return {
        "created": u["createdAt"][:10],
        "repos": u["repositories"]["totalCount"],
        "contributed": u["repositoriesContributedTo"]["totalCount"],
        "followers": u["followers"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "contributions_year": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "top_languages": [k for k, _ in sorted(langs.items(), key=lambda kv: -kv[1])[:3]],
        "latest_repo": latest["name"] if latest else "",
        "latest_push": latest["pushedAt"][:10] if latest else "",
    }


def load_stats():
    cache = ASSETS / "stats.json"
    try:
        stats = fetch_stats()
        cache.write_text(json.dumps(stats, indent=2) + "\n")
        print("live stats:", stats)
        return stats
    except Exception as exc:  # network/API problems must not break the card
        print("using cached stats:", exc)
        return json.loads(cache.read_text())


# --------------------------------------------------------------------------- formatting
def add_months(d, months):
    y, m = divmod(d.month - 1 + months, 12)
    y, m = d.year + y, m + 1
    last = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(y, m, min(d.day, last))


def uptime(start, today):
    months = (today.year - start.year) * 12 + today.month - start.month
    if add_months(start, months) > today:
        months -= 1
    days = (today - add_months(start, months)).days
    y, m = divmod(months, 12)

    def plural(n, w):
        return f"{n} {w}{'' if n == 1 else 's'}"

    return f"{plural(y, 'year')}, {plural(m, 'month')}, {plural(days, 'day')}"


def ago(date_str, today):
    if not date_str:
        return ""
    days = (today - dt.date.fromisoformat(date_str)).days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 14:
        return f"{days} days ago"
    if days < 60:
        return f"{days // 7} weeks ago"
    return f"{days // 30} months ago"


def kv_parts(key, value, width):
    """Return [(text, cls)] for '. key: ..... value' padded to width."""
    head = f"{key}:"
    dots = max(2, width - 2 - len(head) - len(value) - 2)
    return [(". ", "cc"), (head, "key"), (" " + "." * dots + " ", "cc"), (value, "value")]


def rule_parts(title, width, lead=""):
    used = len(lead) + len(title) + 1
    return [(lead, "cc"), (title + " ", "text"), ("─" * (width - used), "cc")]


def stats_lines(s, today):
    half = (RW - 3) // 2
    repos = f"{s['repos']} {{Contributed: {s['contributed']}}}" if s.get("contributed") else str(s["repos"])
    left = kv_parts("Repos", repos, half + 3)
    right = kv_parts("Followers", str(s["followers"]), RW - half - 4)[1:]
    lines = [left + [(" | ", "cc")] + right]
    # the card grows with the profile: these lines appear once the numbers are meaningful
    if s.get("stars", 0) >= 10 or s.get("contributions_year", 0) >= 50:
        l2 = kv_parts("Stars", str(s["stars"]), half + 3)
        r2 = kv_parts("Contrib.Year", str(s["contributions_year"]), RW - half - 4)[1:]
        lines.append(l2 + [(" | ", "cc")] + r2)
    lines.append(kv_parts("Latest.Push", f"{s['latest_repo']} · {ago(s['latest_push'], today)}", RW))
    lines.append(kv_parts("Top.Languages", " · ".join(s["top_languages"]), RW))
    return lines


def build_lines(stats, today):
    start = dt.date.fromisoformat(stats["created"])
    out = []
    for item in PROFILE:
        kind = item[0]
        if kind == "header":
            out.append([(item[1], "user"), (" " + "─" * (RW - len(item[1]) - 1), "cc")])
        elif kind == "kv":
            out.append(kv_parts(item[1], item[2].format(uptime=uptime(start, today)), RW))
        elif kind == "blank":
            out.append([(".", "cc")])
        elif kind == "section":
            out.append(rule_parts(item[1], RW, lead="- "))
        elif kind == "stats":
            out.extend(stats_lines(stats, today))
    return out


# --------------------------------------------------------------------------- svg
def render(theme, lines, portrait, today):
    p = PALETTES[theme]
    fs, lh = 15, 20
    top = 34
    rows = max(len(portrait), len(lines) + 2)
    height = top + rows * lh + 22
    width = 1000
    ax, rx = 26, 452

    css = f"""
@font-face {{ font-family: 'ConsolasFallback'; src: local('Consolas'); size-adjust: 109%; }}
text, tspan {{ white-space: pre; }}
.cc {{ fill: {p['cc']}; }} .key {{ fill: {p['key']}; }} .value {{ fill: {p['value']}; }}
.text {{ fill: {p['text']}; }} .user {{ fill: {p['text']}; font-weight: bold; }}
.prompt {{ fill: {p['accent']}; font-weight: bold; }}
.in {{ opacity: 0; animation: in .45s ease-out forwards; }}
.ascii {{ opacity: 0; animation: in 1.1s ease-out .1s forwards; }}
.cursor {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes in {{ to {{ opacity: 1; }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
"""
    font = ("ConsolasFallback, Consolas, 'Cascadia Mono', 'SFMono-Regular', Menlo, "
            "'DejaVu Sans Mono', monospace")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{font}" font-size="{fs}px" '
        f'role="img" aria-label="Henriques Soares profile card">',
        "<title>Henriques Soares · IT Risk &amp; Governance @ Bradesco · Security Engineering</title>",
        f"<style>{css}</style>",
        '<defs><linearGradient id="ag" x1="0" y1="0" x2="0.35" y2="1">'
        f'<stop offset="0" stop-color="{p["a1"]}"/><stop offset="1" stop-color="{p["a2"]}"/>'
        "</linearGradient></defs>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="14" '
        f'fill="{p["card"]}" stroke="{p["border"]}"/>',
    ]
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        parts.append(f'<circle cx="{22 + i * 18}" cy="17" r="5.5" fill="{c}" opacity="0.85"/>')

    parts.append(f'<text class="ascii" x="{ax}" y="{top + lh}" fill="url(#ag)" xml:space="preserve">')
    for i, row in enumerate(portrait):
        parts.append(f'<tspan x="{ax}" y="{top + (i + 1) * lh}">{escape(row)}</tspan>')
    parts.append("</text>")

    for i, line in enumerate(lines):
        y = top + (i + 1) * lh
        spans = "".join(f'<tspan class="{cls}">{escape(txt)}</tspan>' for txt, cls in line if txt)
        parts.append(f'<text class="in" style="animation-delay:{0.25 + i * 0.06:.2f}s" '
                     f'x="{rx}" y="{y}" xml:space="preserve">{spans}</text>')

    y = top + (len(lines) + 2) * lh
    delay = 0.25 + len(lines) * 0.06
    prompt = f"{LOGIN.lower()}@github:~$ "
    parts.append(f'<text class="in" style="animation-delay:{delay:.2f}s" x="{rx}" y="{y}" '
                 f'xml:space="preserve"><tspan class="prompt">{escape(prompt)}</tspan>'
                 f'<tspan class="cursor text">█</tspan></text>')
    parts.append(f'<text x="{width - 18}" y="{height - 10}" text-anchor="end" font-size="10px" '
                 f'class="cc">updated {today.isoformat()}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).date()  # São Paulo
    stats = load_stats()
    portrait = (ASSETS / "portrait.txt").read_text().rstrip("\n").split("\n")
    lines = build_lines(stats, today)
    for theme in PALETTES:
        (ASSETS / f"neofetch-{theme}.svg").write_text(render(theme, lines, portrait, today))
    print("wrote neofetch-dark.svg and neofetch-light.svg")


if __name__ == "__main__":
    main()
