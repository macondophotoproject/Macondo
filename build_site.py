#!/usr/bin/env python3
"""
Macondo Photo Project — site builder.
Reads each folder under content/<slug>/ (info.txt + photos/), generates
the matching progetti/<slug>.html page, AND rewrites the "Projects" rows
on the home page between the AUTO-PROJECTS markers.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUTDIR = ROOT / "progetti"
INDEX = ROOT / "index.html"

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Macondo Photo Project</title>
<meta name="description" content="{subtitle}">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="site-title" href="../index.html">Macondo Photo Project<small>Documentary photography</small></a>
    <nav class="site-nav">
      <a href="../index.html" aria-current="page">Projects</a>
      <a href="../collezioni/index.html">Collections</a>
      <a href="../sciolti.html">Loose shots</a>
      <a href="../biografia.html">Bio</a>
    </nav>
  </div>
</header>

<main class="wrap">

  <div class="page-header">
    <div class="eyebrow">Project · {status}</div>
    <h1>{title}</h1>
    <p class="dek">{subtitle}</p>
  </div>

{description_html}

  <div class="gallery" style="padding-top:36px;">
{gallery_html}
  </div>

</main>

<footer class="site-footer">
  <span>© <span id="year"></span> Macondo Photo Project</span>
  <span><a href="../biografia.html">Bio</a></span>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

PLATE_TEMPLATE = """    <figure class="plate">
      <div class="plate-frame"><img src="../content/{slug}/photos/{filename}" alt="{title} — photo {n}"></div>
      <figcaption class="plate-caption">
        <span class="stazione">Photo {n}</span>
      </figcaption>
    </figure>
"""

ROW_TEMPLATE = """    <a class="board-row" role="listitem" href="progetti/{slug}.html">
      <span class="board-code">{code}</span>
      <span class="board-name">{title}
        <span class="sub">{subtitle}</span>
      </span>
      <span class="board-status {status_class}">{status_label}</span>
      <span class="board-arrow">→</span>
    </a>
"""

IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
STATUS_CLASS = {"in progress": "attivo", "archive": "futuro", "completed": "futuro"}


def parse_info(path):
    meta = {"title": path.parent.name.title(), "subtitle": "", "status": "in progress"}
    desc_lines, in_desc = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not in_desc and line.lower().startswith("description:"):
            in_desc = True
            first = line.split(":", 1)[1].strip()
            if first:
                desc_lines.append(first)
            continue
        if in_desc:
            desc_lines.append(line)
        elif ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    paragraphs = [p.strip() for p in "\n".join(desc_lines).split("\n\n") if p.strip()]
    meta["description_html"] = "\n".join(f"  <p>{p}</p>" for p in paragraphs)
    return meta


def build_project(folder):
    info_path = folder / "info.txt"
    if not info_path.exists():
        print(f"  [skip] {folder.name}: manca info.txt")
        return None
    meta = parse_info(info_path)
    photos_dir = folder / "photos"
    photos = sorted(
        p.name for p in photos_dir.iterdir()
        if p.suffix.lower() in IMG_EXTENSIONS
    ) if photos_dir.exists() else []

    gallery_html = "\n".join(
        PLATE_TEMPLATE.format(slug=folder.name, filename=f, title=meta["title"], n=i + 1)
        for i, f in enumerate(photos)
    ) or (
        "    <p style=\"font-family:var(--mono); color:var(--slate);\">"
        f"No photos yet — add some to content/{folder.name}/photos/</p>"
    )

    html = PAGE_TEMPLATE.format(
        title=meta["title"], subtitle=meta["subtitle"], status=meta["status"],
        description_html=meta["description_html"], gallery_html=gallery_html,
    )
    OUTDIR.mkdir(exist_ok=True)
    out_path = OUTDIR / f"{folder.name}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  [ok] {out_path.relative_to(ROOT)}  ({len(photos)} photos)")

    meta["slug"] = folder.name
    meta["photo_count"] = len(photos)
    return meta


def sync_home(projects):
    if not INDEX.exists():
        print("  [skip] index.html non trovato")
        return
    html = INDEX.read_text(encoding="utf-8")
    start, end = "<!-- AUTO-PROJECTS:START -->", "<!-- AUTO-PROJECTS:END -->"
    if start not in html or end not in html:
        print("  [skip] segnaposto AUTO-PROJECTS non trovati in index.html")
        return

    rows = []
    for i, meta in enumerate(projects, start=1):
        code = (meta["slug"][:2] or "P" + str(i)).upper()
        rows.append(ROW_TEMPLATE.format(
            slug=meta["slug"], code=code, title=meta["title"], subtitle=meta["subtitle"],
            status_class=STATUS_CLASS.get(meta["status"].lower(), "attivo"),
            status_label=meta["status"].capitalize(),
        ))
    block = start + "\n" + "\n".join(rows) + "    " + end
    pre, _, rest = html.partition(start)
    _, _, post = rest.partition(end)
    INDEX.write_text(pre + block + post, encoding="utf-8")
    print(f"  [ok] index.html aggiornato con {len(projects)} progetti")


def main():
    if not CONTENT.exists():
        print("Cartella 'content' non trovata.")
        return
    print("Building project pages...")
    projects = []
    for folder in sorted(CONTENT.iterdir()):
        if folder.is_dir():
            meta = build_project(folder)
            if meta:
                projects.append(meta)
    print("Syncing home page...")
    sync_home(projects)
    print("Done.")


if __name__ == "__main__":
    main()
