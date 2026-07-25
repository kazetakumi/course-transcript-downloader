#!/usr/bin/env python3
"""
MIT OpenCourseWare course downloader.

Uses the MIT Learn API (https://api.learn.mit.edu) to resolve a course from a
topic, a course number/title, or a direct OCW URL, then downloads its video
transcripts, lecture notes, problem sets, and exams into an organized folder.

Subcommands
-----------
  search   <query>              List ranked candidate courses (JSON).
  resolve  <query|number|url>   Resolve a single best-match course (JSON).
  download <query|number|url>   Download a course's materials to disk.

Video files (.mp4) and images are intentionally skipped — transcripts stand in
for the video. See .wayfinder/assets/00{1,2}-*.md for the researched contract.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

API = "https://api.learn.mit.edu"
OCW = "https://ocw.mit.edu"
UA = "mit-ocw-downloader/1.0 (+https://ocw.mit.edu)"

CAPTION_EXTS = {".vtt", ".srt", ".webvtt"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".svg"}
SKIP_EXTS = {".mp4", ".m4v", ".mov"} | IMAGE_EXTS

# feature-type -> folder. Extension/title fallbacks handle the rest.
FEATURE_FOLDER = {
    "Lecture Notes": "lecture-notes",
    "Readings": "lecture-notes",
    "Problem Sets": "problem-sets",
    "Problem Set Solutions": "problem-sets",
    "Assignments": "problem-sets",
    "Written Assignments": "problem-sets",
    "Exams": "exams",
    "Exam Solutions": "exams",
}


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
def _get(url: str, *, tries: int = 3, as_json: bool = False):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
            return json.loads(data) if as_json else data
        except Exception as exc:  # noqa: BLE001 - retry any transient failure
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {tries} tries: {url}\n  {last}")


def _api(path: str, **params) -> dict:
    qs = urllib.parse.urlencode(params)
    return _get(f"{API}{path}?{qs}", as_json=True)


# --------------------------------------------------------------------------- #
# Resolution (topic / number / url  ->  course record)
# --------------------------------------------------------------------------- #
def _slug_from_url(text: str) -> str | None:
    m = re.search(r"ocw\.mit\.edu/courses/([^/?#]+)", text)
    return m.group(1) if m else None


def _summarize(course: dict, *, has_video: bool | None = None) -> dict:
    runs = course.get("runs") or [{}]
    run = runs[0]
    cf = course.get("course_feature") or []
    return {
        "readable_id": course.get("readable_id"),
        "title": course.get("title"),
        "url": course.get("url"),
        "slug": _slug_from_url(course.get("url") or ""),
        "year": run.get("year"),
        "run_id": run.get("id"),
        "course_feature": cf,
        # Light search-time signal only. Authoritative check is post-enumeration.
        "likely_has_video": ("Lecture Videos" in cf) if has_video is None else has_video,
    }


# A bare MIT course number, e.g. "18.06", "6.006", "24.200", "18.06SC", "21G".
_NUMBER_RE = re.compile(r"^\d+[A-Za-z]*(\.\w+)?$")


def _course_number(readable_id: str | None) -> str:
    return (readable_id or "").split("+", 1)[0]


def search_courses(query: str, limit: int = 8) -> list[dict]:
    # API relevance order is authoritative for topic search — do NOT reorder it.
    data = _api(
        "/api/v1/learning_resources_search/",
        q=query,
        platform="ocw",
        resource_type="course",
        limit=limit,
    )
    return [_summarize(c) for c in data.get("results", [])]


def resolve_course(target: str) -> dict:
    """Return one best-match course summary for a number, title, url, or topic."""
    slug = _slug_from_url(target)
    if slug:
        # Direct URL: match the search hit whose url contains the slug.
        words = slug.replace("-", " ")
        for c in search_courses(words, limit=12):
            if c["slug"] == slug:
                return c
        # Fallback: synthesize from the slug even if search misses.
        return {"readable_id": None, "title": slug, "url": f"{OCW}/courses/{slug}/",
                "slug": slug, "year": None, "run_id": None, "course_feature": [],
                "likely_has_video": None}

    # Exact readable_id (e.g. "18.06+fall_2011")
    if "+" in target:
        data = _api("/api/v1/courses/", readable_id=target)
        if data.get("results"):
            return _summarize(data["results"][0])

    hits = search_courses(target, limit=12)
    if not hits:
        raise SystemExit(json.dumps({"error": "no_match", "query": target}))

    # Bare course number: prefer an exact course-number match over text relevance
    # (search for "18.06" otherwise ranks "18.102" et al. above it).
    if _NUMBER_RE.match(target.strip()):
        want = target.strip().upper()
        exact = [c for c in hits if _course_number(c["readable_id"]).upper() == want]
        if exact:
            return _prefer_video(exact)
        prefix = [c for c in hits
                  if _course_number(c["readable_id"]).upper().startswith(want)
                  and not _course_number(c["readable_id"])[len(want):len(want) + 1].isdigit()]
        if prefix:
            return _prefer_video(prefix)

    return hits[0]


def _prefer_video(cands: list[dict]) -> dict:
    """Among equally-matched course-number variants, favor one likely to have video."""
    cands = sorted(cands, key=lambda c: (not c["likely_has_video"], -(c["year"] or 0)))
    return cands[0]


# --------------------------------------------------------------------------- #
# Enumeration + categorization
# --------------------------------------------------------------------------- #
def list_contentfiles(run_id: int) -> list[dict]:
    out, offset = [], 0
    while True:
        data = _api("/api/v1/contentfiles/", run_id=run_id, limit=100, offset=offset)
        batch = data.get("results", [])
        if not batch:
            break
        out.extend(batch)
        offset += 100
        if offset >= data.get("count", 0):
            break
    return out


def _is_transcript(cf: dict, ext: str) -> bool:
    if ext in CAPTION_EXTS:
        return True
    name = f"{cf.get('title','')} {cf.get('url','')} {cf.get('key','')}".lower()
    return ext == ".pdf" and "transcript" in name


def categorize(cf: dict) -> str | None:
    """Return the destination folder, or None to skip this file."""
    ext = (cf.get("file_extension") or "").lower()
    if ext in SKIP_EXTS:
        return None
    if _is_transcript(cf, ext):
        return "transcripts"
    for feat in cf.get("content_feature_type") or []:
        if feat in FEATURE_FOLDER:
            return FEATURE_FOLDER[feat]
    if ext in (".pdf", ".m", ".txt", ".docx", ".xlsx", ".zip"):
        return "other"
    return None


# --------------------------------------------------------------------------- #
# Raw file URL discovery (scrape resource page)
# --------------------------------------------------------------------------- #
class _HrefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)


def raw_file_url(cf: dict) -> str | None:
    """Find the direct file URL by scraping the resource page for the matching href."""
    page = cf.get("url")
    ext = (cf.get("file_extension") or "").lower()
    if not page or not ext:
        return None
    try:
        html = _get(page).decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return None
    parser = _HrefCollector()
    parser.feed(html)
    # candidate hrefs that point at a real file with our extension
    cands = [h for h in parser.hrefs if h.lower().split("?")[0].endswith(ext)]
    if not cands:
        return None
    # Prefer the href whose basename maps to this contentfile's key slug.
    key_slug = (cf.get("key") or "").rstrip("/").split("/")[-1].lower()
    best = None
    for h in cands:
        base = h.split("?")[0].rsplit("/", 1)[-1].lower()
        stem = base.rsplit(".", 1)[0]
        if key_slug and (stem in key_slug or key_slug in stem or stem.replace("_", "") in key_slug):
            best = h
            break
    href = best or cands[0]
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return OCW + href
    return href


# --------------------------------------------------------------------------- #
# Transcript cleanup (caption -> readable .txt)
# --------------------------------------------------------------------------- #
def is_latin_text(text: str, threshold: float = 0.6) -> bool:
    """True if the transcript is predominantly Latin script (English et al.).

    OCW ships some translated caption files (Chinese, etc.) that the API does
    not language-tag, so we infer from the content and default to English.
    """
    alpha = [ch for ch in text if ch.isalpha()]
    if len(alpha) < 20:
        return True  # too little signal — keep it rather than mis-drop
    ascii_letters = sum(1 for ch in alpha if "a" <= ch.lower() <= "z")
    return (ascii_letters / len(alpha)) >= threshold


def caption_to_text(raw: bytes) -> str:
    lines = raw.decode("utf-8", "replace").splitlines()
    out, seen_blank = [], False
    for ln in lines:
        s = ln.strip()
        if s in ("WEBVTT",) or s.isdigit():
            continue
        if "-->" in s:  # timestamp cue line
            continue
        if not s:
            seen_blank = True
            continue
        s = re.sub(r"<[^>]+>", "", s)  # strip inline tags
        if out and seen_blank:
            out.append("")
        out.append(s)
        seen_blank = False
    # collapse >1 blank lines
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


# --------------------------------------------------------------------------- #
# Download orchestration
# --------------------------------------------------------------------------- #
VIDEO_EXTS = {".mp4", ".m4v", ".mov"}


def _safe_name(cf: dict, href: str) -> str:
    base = href.split("?")[0].rsplit("/", 1)[-1]
    base = urllib.parse.unquote(base)
    return re.sub(r"[^\w.\-]+", "_", base)


def _abs_url(href: str) -> str:
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return OCW + href
    return href


def video_page_transcripts(page_url: str, youtube_id: str | None) -> list[str]:
    """Scrape a lecture-video resource page for its transcript/caption file URLs.

    OCW does not index per-video transcripts as separate contentfiles — the
    English transcript lives on the video's own page as `<hash>_<youtube_id>.pdf`
    (and sometimes a caption file). Without this, the core deliverable is missed.
    """
    try:
        html = _get(page_url).decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return []
    parser = _HrefCollector()
    parser.feed(html)
    out, seen = [], set()
    for h in parser.hrefs:
        base = h.lower().split("?")[0].rsplit("/", 1)[-1]
        ext = "." + base.rsplit(".", 1)[-1] if "." in base else ""
        keep = ext in CAPTION_EXTS or (
            ext == ".pdf" and youtube_id and youtube_id.lower() in base
        )
        if keep:
            u = _abs_url(h)
            if u not in seen:
                seen.add(u)
                out.append(u)
    return out


def _existing_sub(course_dir: Path, folder: str, fname: str) -> str | None:
    """Return the sub-path a file already lives in (base or other-languages), else None."""
    if (course_dir / folder / fname).exists():
        return folder
    if (course_dir / folder / "other-languages" / fname).exists():
        return f"{folder}/other-languages"
    return None


def _store(blob: bytes, *, course_dir: Path, dest_root: Path, folder: str, fname: str,
           title: str | None, source: str, manifest: dict, counts: dict,
           caption_text: str | None) -> None:
    """Write a file (routing non-English captions aside) and record it."""
    sub = folder
    if caption_text is not None and folder == "transcripts" and not is_latin_text(caption_text):
        sub = f"{folder}/other-languages"
    out_dir = course_dir / sub
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / fname
    out_path.write_bytes(blob)
    counts[sub] = counts.get(sub, 0) + 1  # tally by actual location, not the base folder
    record = {"folder": sub, "file": str(out_path.relative_to(dest_root)),
              "title": title, "source": source}
    if caption_text is not None:  # emit a cleaned plain-text version
        txt = out_path.with_suffix(".txt")
        try:
            txt.write_text(caption_text, encoding="utf-8")
            record["plain_text"] = str(txt.relative_to(dest_root))
        except Exception:  # noqa: BLE001
            pass
    if folder == "transcripts" and sub == "transcripts":
        manifest["transcripts_available"] = True
    manifest["downloaded"].append(record)


def download_course(target: str, dest_root: Path, *, force: bool = False) -> dict:
    course = resolve_course(target)
    if not course.get("run_id"):
        raise SystemExit(json.dumps(
            {"error": "unresolved_run", "course": course,
             "hint": "Could not find a Learn API run id for this course."}, indent=2))

    slug = course["slug"] or re.sub(r"[^\w\-]+", "-", course["title"].lower())
    course_dir = dest_root / "courses" / slug
    files = list_contentfiles(course["run_id"])

    manifest = {
        "course": course,
        "counts": {},
        "transcripts_available": False,
        "downloaded": [],
        "skipped_video": 0,
        "errors": [],
    }
    counts: dict[str, int] = {}

    # --- Pass 1: video pages -> grab per-video transcripts, skip the video files.
    seen_pages: set[str] = set()
    for cf in files:
        if (cf.get("file_extension") or "").lower() not in VIDEO_EXTS:
            continue
        manifest["skipped_video"] += 1
        page, yt = cf.get("url"), cf.get("youtube_id")
        if not page or page in seen_pages:
            continue
        seen_pages.add(page)
        title = cf.get("title") or "video"
        stem = re.sub(r"[^\w.\-]+", "_", title)[:80].strip("_") or "video"
        for turl in video_page_transcripts(page, yt):
            ext = Path(turl.split("?")[0]).suffix.lower()
            is_cap = ext in CAPTION_EXTS
            fname = f"{stem}{ext}" if is_cap else f"{stem}_transcript.pdf"
            existing = None if force else _existing_sub(course_dir, "transcripts", fname)
            if existing:
                counts[existing] = counts.get(existing, 0) + 1
                if existing == "transcripts":
                    manifest["transcripts_available"] = True
                continue
            try:
                blob = _get(turl)
            except Exception as exc:  # noqa: BLE001
                manifest["errors"].append({"title": title, "reason": str(exc), "url": turl})
                continue
            _store(blob, course_dir=course_dir, dest_root=dest_root, folder="transcripts",
                   fname=fname, title=title, source=turl, manifest=manifest, counts=counts,
                   caption_text=caption_to_text(blob) if is_cap else None)

    # --- Pass 2: non-video files (notes, psets, exams, standalone transcripts).
    for cf in files:
        if (cf.get("file_extension") or "").lower() in VIDEO_EXTS:
            continue
        folder = categorize(cf)
        if folder is None:
            continue
        href = raw_file_url(cf)
        if not href:
            manifest["errors"].append({"title": cf.get("title"), "reason": "no_raw_url",
                                        "page": cf.get("url")})
            continue
        fname = _safe_name(cf, href)
        existing = None if force else _existing_sub(course_dir, folder, fname)
        if existing:
            counts[existing] = counts.get(existing, 0) + 1
            if existing == "transcripts":
                manifest["transcripts_available"] = True
            continue
        try:
            blob = _get(href)
        except Exception as exc:  # noqa: BLE001
            manifest["errors"].append({"title": cf.get("title"), "reason": str(exc), "url": href})
            continue
        is_caption = folder == "transcripts" and Path(fname).suffix.lower() in CAPTION_EXTS
        _store(blob, course_dir=course_dir, dest_root=dest_root, folder=folder, fname=fname,
               title=cf.get("title"), source=href, manifest=manifest, counts=counts,
               caption_text=caption_to_text(blob) if is_caption else None)

    # Report counts from what is actually on disk — the loop counters can double
    # count when duplicate video pages reference the same already-saved transcript.
    counts = _folder_counts(course_dir)
    manifest["counts"] = counts
    manifest["transcripts_available"] = counts.get("transcripts", 0) > 0
    course_dir.mkdir(parents=True, exist_ok=True)
    (course_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _write_readme(course_dir, course, counts, manifest)
    return manifest


ALL_FOLDERS = ("transcripts", "transcripts/other-languages",
               "lecture-notes", "problem-sets", "exams", "other")


def _folder_counts(course_dir: Path) -> dict[str, int]:
    """Count actual downloaded files per folder (excluding derived .txt sidecars)."""
    out: dict[str, int] = {}
    for sub in ALL_FOLDERS:
        d = course_dir / sub
        if not d.exists():
            continue
        n = sum(1 for f in d.iterdir()
                if f.is_file() and f.suffix.lower() != ".txt")
        if n:
            out[sub] = n
    return out


def _write_readme(course_dir: Path, course: dict, counts: dict, manifest: dict) -> None:
    lines = [
        f"# {course.get('title')} ({course.get('year') or ''})".strip(),
        "",
        f"- Source: {course.get('url')}",
        f"- OCW id: `{course.get('readable_id')}`",
        f"- Transcripts available: **{'yes' if manifest['transcripts_available'] else 'NO'}**",
        "",
        "## Downloaded materials",
        "",
    ]
    labels = [
        ("transcripts", "transcripts/ (English)"),
        ("transcripts/other-languages", "transcripts/other-languages/ (translated captions)"),
        ("lecture-notes", "lecture-notes/"),
        ("problem-sets", "problem-sets/"),
        ("exams", "exams/"),
        ("other", "other/"),
    ]
    for key, label in labels:
        if counts.get(key):
            lines.append(f"- **{label}** — {counts[key]} files")
    if manifest["skipped_video"]:
        lines.append(f"- _(skipped {manifest['skipped_video']} video files — out of scope)_")
    if manifest["errors"]:
        lines.append(f"- _(⚠ {len(manifest['errors'])} files could not be fetched — see manifest.json)_")
    lines.append("")
    (course_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Download MIT OpenCourseWare materials.")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search", help="List candidate courses for a topic.")
    ps.add_argument("query")
    ps.add_argument("--limit", type=int, default=8)

    pr = sub.add_parser("resolve", help="Resolve one best-match course.")
    pr.add_argument("target")

    pd = sub.add_parser("download", help="Download a course's materials.")
    pd.add_argument("target", help="topic, course number, readable_id, or OCW URL")
    pd.add_argument("--dest", default=".", help="destination root (default: cwd)")
    pd.add_argument("--force", action="store_true", help="re-download existing files")

    args = p.parse_args(argv)

    if args.cmd == "search":
        print(json.dumps(search_courses(args.query, args.limit), indent=2))
    elif args.cmd == "resolve":
        print(json.dumps(resolve_course(args.target), indent=2))
    elif args.cmd == "download":
        man = download_course(args.target, Path(args.dest).resolve(), force=args.force)
        summary = {
            "course": man["course"]["title"],
            "readable_id": man["course"]["readable_id"],
            "transcripts_available": man["transcripts_available"],
            "counts": man["counts"],
            "skipped_video": man["skipped_video"],
            "errors": len(man["errors"]),
        }
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
