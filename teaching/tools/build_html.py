from __future__ import annotations

import html
import os
import re
import shutil
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "html"
ARTICLES_DIR = SITE_DIR / "articles"
TASKS_DIR = SITE_DIR / "tasks"


@dataclass(frozen=True)
class Page:
    source: Path
    output: Path
    title: str
    section: str
    summary: str = ""


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.hrefs.append(value)


ARTICLE_SOURCES: list[tuple[str, str, str]] = [
    (
        "README.md",
        "Teaching Pack Overview",
        "Start here for the library map and document guide.",
    ),
    (
        "01-project-summary.md",
        "Project Summary",
        "What the app does, the technologies used, and what students learn.",
    ),
    (
        "02-final-architecture.md",
        "Final Architecture",
        "Folder structure, module responsibilities, and request/data flow.",
    ),
    (
        "03-infrastructure-first-setup.md",
        "Infrastructure-First Setup",
        "The early setup path for tools, config, database, and smoke tests.",
    ),
    (
        "04-recommended-teaching-sequence.md",
        "Recommended Teaching Sequence",
        "The full from-scratch rebuild order with commits and dependencies.",
    ),
    (
        "05-parallelization-plan.md",
        "Parallelization Plan",
        "How to split student pairs or groups after the core path is complete.",
    ),
    (
        "06-teaching-notes.md",
        "Teaching Notes",
        (
            "Verbal explanations, common mistakes, checkpoint questions, "
            "and stretch ideas."
        ),
    ),
    (
        "07-risk-review.md",
        "Risk Review",
        "Complex areas to simplify, defer, or hide behind starter helpers.",
    ),
    (
        "08-code-walkthrough-snippets.md",
        "Code Walkthrough Snippets",
        "Short code anchors for live teaching.",
    ),
]


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def article_output(source: Path) -> Path:
    if source.name == "README.md":
        return ARTICLES_DIR / "teaching-pack-overview.html"
    return ARTICLES_DIR / f"{source.stem}.html"


def task_output(source: Path) -> Path:
    if source.name == "README.md":
        return TASKS_DIR / "index.html"
    return TASKS_DIR / f"{source.stem}.html"


def output_for_source(source: Path) -> Path:
    source = source.resolve()
    if source.parent == (ROOT / "tasks").resolve():
        return task_output(source)
    return article_output(source)


def rel_href(target: Path, current: Path) -> str:
    return Path(os.path.relpath(target, current.parent)).as_posix()


def resolve_markdown_link(target: str, source: Path, output: Path) -> str:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return target

    path_part, sep, anchor = target.partition("#")
    if not path_part:
        return f"#{anchor}"

    raw_path = (source.parent / path_part).resolve()
    if raw_path.is_dir():
        raw_path = raw_path / "README.md"
    elif raw_path.suffix != ".md":
        possible_readme = raw_path / "README.md"
        possible_markdown = raw_path.with_suffix(".md")
        if possible_readme.exists():
            raw_path = possible_readme
        elif possible_markdown.exists():
            raw_path = possible_markdown

    if raw_path.suffix == ".md" and raw_path.exists():
        href = rel_href(output_for_source(raw_path), output)
        return f"{href}#{anchor}" if sep else href

    return target


def render_text_chunk(chunk: str) -> str:
    escaped = html.escape(chunk)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def render_inline(text: str, source: Path, output: Path) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    rendered: list[str] = []

    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue

        cursor = 0
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", part):
            rendered.append(render_text_chunk(part[cursor : match.start()]))
            label = render_text_chunk(match.group(1))
            href = html.escape(resolve_markdown_link(match.group(2), source, output))
            rendered.append(f'<a href="{href}">{label}</a>')
            cursor = match.end()

        rendered.append(render_text_chunk(part[cursor:]))

    return "".join(rendered)


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    current = lines[index].strip()
    next_line = lines[index + 1].strip()
    return (
        current.startswith("|")
        and current.endswith("|")
        and next_line.startswith("|")
        and set(next_line.replace("|", "").replace(":", "").strip()) <= {"-", " "}
        and "-" in next_line
    )


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    return (
        stripped.startswith("#")
        or stripped.startswith("```")
        or stripped.startswith("> ")
        or stripped.startswith("- ")
        or bool(re.match(r"\d+\.\s+", stripped))
        or is_table_start(lines, index)
    )


def render_table(
    lines: list[str], index: int, source: Path, output: Path
) -> tuple[str, int]:
    headers = split_table_row(lines[index])
    index += 2
    rows: list[list[str]] = []

    while index < len(lines) and lines[index].strip().startswith("|"):
        rows.append(split_table_row(lines[index]))
        index += 1

    header_html = "".join(
        f"<th>{render_inline(cell, source, output)}</th>" for cell in headers
    )
    row_html = []
    for row in rows:
        cells = "".join(
            f"<td>{render_inline(cell, source, output)}</td>" for cell in row
        )
        row_html.append(f"<tr>{cells}</tr>")

    return (
        '<div class="table-wrap"><table>'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(row_html)}</tbody>"
        "</table></div>",
        index,
    )


def render_list(
    lines: list[str], index: int, source: Path, output: Path, ordered: bool
) -> tuple[str, int]:
    tag = "ol" if ordered else "ul"
    items: list[str] = []
    pattern = r"\d+\.\s+(.*)" if ordered else r"-\s+(.*)"

    while index < len(lines):
        stripped = lines[index].strip()
        match = re.match(pattern, stripped)
        if not match:
            break
        items.append(f"<li>{render_inline(match.group(1), source, output)}</li>")
        index += 1

    return f"<{tag}>{''.join(items)}</{tag}>", index


def markdown_to_html(markdown: str, source: Path, output: Path) -> str:
    lines = markdown.splitlines()
    rendered: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            class_attr = (
                f' class="language-{html.escape(language)}"' if language else ""
            )
            code = html.escape(chr(10).join(code_lines))
            rendered.append(f"<pre><code{class_attr}>{code}</code></pre>")
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            heading_id = slugify(re.sub(r"`([^`]+)`", r"\1", text))
            heading_text = render_inline(text, source, output)
            rendered.append(f'<h{level} id="{heading_id}">{heading_text}</h{level}>')
            index += 1
            continue

        if is_table_start(lines, index):
            table_html, index = render_table(lines, index, source, output)
            rendered.append(table_html)
            continue

        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("> "):
                quote_lines.append(lines[index].strip()[2:])
                index += 1
            quote = " ".join(quote_lines)
            rendered.append(
                f"<blockquote>{render_inline(quote, source, output)}</blockquote>"
            )
            continue

        if stripped.startswith("- "):
            list_html, index = render_list(lines, index, source, output, ordered=False)
            rendered.append(list_html)
            continue

        if re.match(r"\d+\.\s+", stripped):
            list_html, index = render_list(lines, index, source, output, ordered=True)
            rendered.append(list_html)
            continue

        paragraph: list[str] = []
        while (
            index < len(lines)
            and lines[index].strip()
            and not is_block_start(lines, index)
        ):
            paragraph.append(lines[index].strip())
            index += 1
        rendered.append(f"<p>{render_inline(' '.join(paragraph), source, output)}</p>")

    return "\n".join(rendered)


def extract_task_meta(source: Path) -> dict[str, str]:
    meta: dict[str, str] = {}
    lines = source.read_text(encoding="utf-8").splitlines()
    in_table = False

    for line in lines:
        if line.strip() == "## Task Metadata":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if in_table and line.startswith("|"):
            cells = split_table_row(line)
            if len(cells) == 2 and cells[0] not in {"Field", "---"}:
                meta[cells[0]] = cells[1]

    return meta


def page_title(source: Path) -> str:
    first_line = source.read_text(encoding="utf-8").splitlines()[0]
    return first_line.lstrip("#").strip()


def build_pages() -> tuple[list[Page], list[Page]]:
    articles = [
        Page(
            source=ROOT / path,
            output=article_output(ROOT / path),
            title=title,
            section="Articles",
            summary=summary,
        )
        for path, title, summary in ARTICLE_SOURCES
    ]

    task_sources = sorted((ROOT / "tasks").glob("[0-9][0-9][0-9]-*.md"))
    tasks = [
        Page(
            source=source,
            output=task_output(source),
            title=page_title(source),
            section="Tasks",
            summary=extract_task_meta(source).get("Suggested commit", ""),
        )
        for source in task_sources
    ]

    return articles, tasks


def nav_link(current_output: Path, target: Path, label: str) -> str:
    href = html.escape(rel_href(target, current_output))
    escaped_label = html.escape(label)
    return f'<a href="{href}">{escaped_label}</a>'


def sidebar(current_output: Path, articles: list[Page], tasks: list[Page]) -> str:
    article_links = "\n".join(
        f"<li>{nav_link(current_output, page.output, page.title)}</li>"
        for page in articles
    )
    task_links = "\n".join(
        f"<li>{nav_link(current_output, page.output, page.title)}</li>"
        for page in tasks
    )
    task_index = nav_link(current_output, TASKS_DIR / "index.html", "Task Index")
    article_index = nav_link(
        current_output, ARTICLES_DIR / "index.html", "Article Index"
    )

    return f"""
<aside class="sidebar">
  <div class="sidebar-section">
    <h2>Library</h2>
    <ul>
      <li>{nav_link(current_output, SITE_DIR / "index.html", "Home")}</li>
      <li>{article_index}</li>
      <li>{task_index}</li>
    </ul>
  </div>
  <div class="sidebar-section">
    <h2>Articles</h2>
    <ol>{article_links}</ol>
  </div>
  <div class="sidebar-section">
    <h2>Tasks</h2>
    <ol class="task-nav">{task_links}</ol>
  </div>
</aside>
"""


def page_shell(
    *,
    title: str,
    body: str,
    output: Path,
    articles: list[Page],
    tasks: list[Page],
    previous_page: Page | None = None,
    next_page: Page | None = None,
) -> str:
    stylesheet = html.escape(rel_href(SITE_DIR / "styles.css", output))
    home = html.escape(rel_href(SITE_DIR / "index.html", output))
    article_index = html.escape(rel_href(ARTICLES_DIR / "index.html", output))
    task_index = html.escape(rel_href(TASKS_DIR / "index.html", output))

    previous_link = (
        nav_link(output, previous_page.output, f"Previous: {previous_page.title}")
        if previous_page
        else ""
    )
    next_link = (
        nav_link(output, next_page.output, f"Next: {next_page.title}")
        if next_page
        else ""
    )
    pager = (
        f'<nav class="pager">{previous_link}<span></span>{next_link}</nav>'
        if previous_link or next_link
        else ""
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | Explore Teaching Library</title>
  <link rel="stylesheet" href="{stylesheet}">
</head>
<body>
  <header class="site-header">
    <a class="brand" href="{home}">Explore Teaching Library</a>
    <nav class="top-nav" aria-label="Primary navigation">
      <a href="{article_index}">Articles</a>
      <a href="{task_index}">Tasks</a>
    </nav>
  </header>
  <div class="page-layout">
    {sidebar(output, articles, tasks)}
    <main class="content">
      {body}
      {pager}
    </main>
  </div>
</body>
</html>
"""


def phase_for_task(meta: dict[str, str]) -> str:
    return meta.get("Parent epic", "Unassigned")


def card(title: str, summary: str, href: str, meta: str = "") -> str:
    meta_html = f'<p class="card-meta">{html.escape(meta)}</p>' if meta else ""
    return f"""
<a class="card" href="{html.escape(href)}">
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(summary)}</p>
  {meta_html}
</a>
"""


def render_home(articles: list[Page], tasks: list[Page]) -> str:
    article_cards = "\n".join(
        card(page.title, page.summary, rel_href(page.output, SITE_DIR / "index.html"))
        for page in articles[1:]
    )

    task_cards = []
    for page in tasks[:8]:
        meta = extract_task_meta(page.source)
        summary = meta.get("Parent epic", "")
        detail = f"{meta.get('Difficulty', '')} | {meta.get('Time estimate', '')}"
        task_cards.append(
            card(
                page.title,
                summary,
                rel_href(page.output, SITE_DIR / "index.html"),
                detail,
            )
        )

    body = f"""
<section class="hero">
  <p class="eyebrow">FastAPI Users Workshop</p>
  <h1>Explore Auth API Teaching Library</h1>
  <p class="hero-copy">A linked HTML library for teaching this repository from a
  clean slate: articles, architecture notes, task cards, sequencing, and workshop
  risks.</p>
  <div class="hero-actions">
    <a class="button primary" href="articles/index.html">Browse Articles</a>
    <a class="button" href="tasks/index.html">Browse Tasks</a>
  </div>
</section>

<section>
  <div class="section-heading">
    <h2>Teaching Articles</h2>
    <a href="articles/index.html">View article index</a>
  </div>
  <div class="card-grid">{article_cards}</div>
</section>

<section>
  <div class="section-heading">
    <h2>Task Library Preview</h2>
    <a href="tasks/index.html">View all 35 tasks</a>
  </div>
  <div class="card-grid task-grid">{"".join(task_cards)}</div>
</section>
"""
    return page_shell(
        title="Home",
        body=body,
        output=SITE_DIR / "index.html",
        articles=articles,
        tasks=tasks,
    )


def render_article_index(articles: list[Page], tasks: list[Page]) -> str:
    cards = "\n".join(
        card(
            page.title, page.summary, rel_href(page.output, ARTICLES_DIR / "index.html")
        )
        for page in articles
    )
    body = f"""
<h1>Article Index</h1>
<p>Use these articles as the instructor-facing guide for the workshop.</p>
<div class="card-grid">{cards}</div>
"""
    return page_shell(
        title="Article Index",
        body=body,
        output=ARTICLES_DIR / "index.html",
        articles=articles,
        tasks=tasks,
    )


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_styles() -> None:
    write_page(
        SITE_DIR / "styles.css",
        """* {
  box-sizing: border-box;
}

:root {
  --bg: #f7f8fb;
  --surface: #ffffff;
  --surface-alt: #eef2f7;
  --text: #17202a;
  --muted: #5c6674;
  --border: #d8dee8;
  --accent: #1d4ed8;
  --accent-dark: #173f9c;
  --code-bg: #101827;
  --code-text: #eef5ff;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
}

a {
  color: var(--accent);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 1.25rem;
  background: rgba(255, 255, 255, 0.96);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(10px);
}

.brand {
  color: var(--text);
  font-weight: 750;
}

.top-nav {
  display: flex;
  gap: 0.8rem;
  font-size: 0.95rem;
}

.page-layout {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 2rem;
  max-width: 1440px;
  margin: 0 auto;
  padding: 1.5rem;
}

.sidebar {
  align-self: start;
  position: sticky;
  top: 4.8rem;
  max-height: calc(100vh - 6rem);
  overflow: auto;
  padding: 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.sidebar h2 {
  margin: 0 0 0.35rem;
  font-size: 0.82rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.sidebar ul,
.sidebar ol {
  margin: 0;
  padding-left: 1.25rem;
}

.sidebar li {
  margin: 0.25rem 0;
  font-size: 0.92rem;
}

.sidebar-section + .sidebar-section {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
}

.task-nav {
  font-size: 0.86rem;
}

.content {
  min-width: 0;
  padding: 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.content h1 {
  margin-top: 0;
  font-size: clamp(2rem, 4vw, 3.25rem);
  line-height: 1.08;
}

.content h2 {
  margin-top: 2.2rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border);
}

.content h3 {
  margin-top: 1.6rem;
}

.content p,
.content li {
  max-width: 78ch;
}

.hero {
  padding: 2rem;
  background: linear-gradient(135deg, #eaf1ff, #ffffff 55%, #f3f7ff);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.eyebrow {
  margin: 0 0 0.5rem;
  color: var(--accent-dark);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.hero-copy {
  font-size: 1.15rem;
  color: var(--muted);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.5rem;
  padding: 0.55rem 0.9rem;
  color: var(--accent);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-weight: 700;
}

.button.primary {
  color: #ffffff;
  background: var(--accent);
  border-color: var(--accent);
}

.section-heading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 1rem;
}

.card {
  display: block;
  min-height: 100%;
  padding: 1rem;
  color: var(--text);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.card:hover {
  border-color: var(--accent);
  text-decoration: none;
}

.card h3 {
  margin: 0 0 0.4rem;
}

.card p {
  margin: 0;
  color: var(--muted);
}

.card-meta {
  margin-top: 0.8rem !important;
  font-size: 0.86rem;
  color: var(--accent-dark) !important;
}

.table-wrap {
  width: 100%;
  overflow-x: auto;
  margin: 1rem 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.94rem;
}

th,
td {
  padding: 0.65rem 0.75rem;
  text-align: left;
  vertical-align: top;
  border: 1px solid var(--border);
}

th {
  background: var(--surface-alt);
}

code {
  padding: 0.1rem 0.25rem;
  background: var(--surface-alt);
  border-radius: 4px;
}

pre {
  overflow: auto;
  padding: 1rem;
  background: var(--code-bg);
  color: var(--code-text);
  border-radius: 8px;
}

pre code {
  padding: 0;
  color: inherit;
  background: transparent;
}

blockquote {
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  color: var(--muted);
  background: var(--surface-alt);
  border-left: 4px solid var(--accent);
  border-radius: 4px;
}

.pager {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  margin-top: 2.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.pager a:last-child {
  text-align: right;
}

@media (max-width: 900px) {
  .page-layout {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .sidebar {
    position: static;
    max-height: none;
  }

  .content {
    padding: 1.25rem;
  }
}
""",
    )


def validate_local_links() -> list[str]:
    site_root = SITE_DIR.resolve()
    failures: list[str] = []

    for path in SITE_DIR.rglob("*.html"):
        parser = LinkParser()
        parser.feed(path.read_text(encoding="utf-8"))

        for href in parser.hrefs:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue

            clean_href = href.split("#", 1)[0]
            if not clean_href:
                continue

            target = (path.parent / unquote(clean_href)).resolve()
            try:
                target.relative_to(site_root)
            except ValueError:
                failures.append(f"{path}: {href} points outside the generated site")
                continue

            if not target.exists():
                failures.append(f"{path}: {href} does not resolve")

    return failures


def main() -> None:
    articles, tasks = build_pages()
    ordered_pages = (
        articles
        + [
            Page(
                ROOT / "tasks" / "README.md",
                TASKS_DIR / "index.html",
                "Task Index",
                "Tasks",
            )
        ]
        + tasks
    )

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)

    write_styles()
    write_page(SITE_DIR / "index.html", render_home(articles, tasks))
    write_page(ARTICLES_DIR / "index.html", render_article_index(articles, tasks))

    previous_by_output: dict[Path, Page | None] = {}
    next_by_output: dict[Path, Page | None] = {}
    for index, page in enumerate(ordered_pages):
        previous_by_output[page.output] = (
            ordered_pages[index - 1] if index > 0 else None
        )
        next_by_output[page.output] = (
            ordered_pages[index + 1] if index + 1 < len(ordered_pages) else None
        )

    task_index_source = ROOT / "tasks" / "README.md"
    task_index_body = markdown_to_html(
        task_index_source.read_text(encoding="utf-8"),
        task_index_source,
        TASKS_DIR / "index.html",
    )
    write_page(
        TASKS_DIR / "index.html",
        page_shell(
            title="Task Index",
            body=task_index_body,
            output=TASKS_DIR / "index.html",
            articles=articles,
            tasks=tasks,
            previous_page=previous_by_output[TASKS_DIR / "index.html"],
            next_page=next_by_output[TASKS_DIR / "index.html"],
        ),
    )

    for page in articles + tasks:
        body = markdown_to_html(
            page.source.read_text(encoding="utf-8"),
            page.source,
            page.output,
        )
        write_page(
            page.output,
            page_shell(
                title=page.title,
                body=body,
                output=page.output,
                articles=articles,
                tasks=tasks,
                previous_page=previous_by_output.get(page.output),
                next_page=next_by_output.get(page.output),
            ),
        )

    link_failures = validate_local_links()
    if link_failures:
        for failure in link_failures:
            sys.stderr.write(f"{failure}\n")
        sys.exit(1)

    page_count = len(list(SITE_DIR.rglob("*.html")))
    sys.stdout.write(f"Generated {page_count} HTML pages in {SITE_DIR}\n")


if __name__ == "__main__":
    main()
