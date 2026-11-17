#!/usr/bin/env python3
"""Mirror a LinkedIn post as a stub entry in _posts/ and a line in _news/.

Creates a post that carries the title, description and tags on this site while
`redirect:` sends readers to the original LinkedIn activity, matching the style
of the existing external-post entries. It also adds an inline news item linking
to the post, so it shows up in the news section of the about page.

Usage:
    python bin/new_linkedin_post.py \
        --url https://www.linkedin.com/posts/gabriele-caddeo-1b6232194_..._activity-7481356411730313217-7xWS \
        --title "Our paper was accepted to ECCV 2026" \
        --description "One-sentence summary shown in the blog list." \
        --tags "eccv-2026, robotics"

Prints the path of each created file to stdout, one per line; progress messages
go to stderr.
"""

import argparse
import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POSTS_DIR = REPO_ROOT / "_posts"
DEFAULT_NEWS_DIR = REPO_ROOT / "_news"
DEFAULT_TIMEZONE = "Europe/Rome"
DEFAULT_BODY = "Read the full post on LinkedIn."
NEWS_LINK_TEXT = "Read the post on LinkedIn"
CATEGORIES = ["external-posts"]
BASE_TAG = "linkedin"
MAX_SLUG_WORDS = 12


def log(message):
    print(message, file=sys.stderr)


def fail(message):
    log(f"error: {message}")
    sys.exit(1)


def slugify(value, max_words=None):
    """Lowercase ASCII slug, matching the hyphenated style of existing posts."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    words = [word for word in re.split(r"[\s_-]+", value) if word]
    if max_words:
        words = words[:max_words]
    return "-".join(words)


def normalize_url(url):
    """Validate that the URL points at a LinkedIn post and strip tracking params."""
    url = url.strip()
    if not url:
        fail("--url is empty")
    url = url.split("?", 1)[0].rstrip("/")
    if not re.match(r"^https?://([\w-]+\.)*linkedin\.com/", url):
        fail(f"not a linkedin.com URL: {url}")
    if not re.search(r"/(posts|feed/update|pulse)/", url):
        fail(f"not a LinkedIn post/article URL (expected /posts/, /feed/update/ or /pulse/): {url}")
    if not url.startswith("https://"):
        url = "https://" + url.split("://", 1)[1]
    return url


def activity_id(url):
    """The numeric activity/share id, used to detect an already-mirrored post."""
    match = re.search(r"(?:activity[-:]|share[-:]|ugcPost[-:])(\d{6,})", url)
    return match.group(1) if match else None


def find_existing(directory, url):
    """Return the post or news item in `directory` already linking to this LinkedIn activity, if any."""
    identifier = activity_id(url)
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if url in text or (identifier and identifier in text):
            return path
    return None


def local_now(timezone):
    try:
        from zoneinfo import ZoneInfo

        return dt.datetime.now(ZoneInfo(timezone))
    except Exception:  # no tzdata available - fall back to the site's usual offset
        log(f"warning: timezone {timezone} unavailable, falling back to a fixed +02:00 offset")
        return dt.datetime.now(dt.timezone(dt.timedelta(hours=2)))


def parse_date(value, timezone):
    """Accept an empty value (now), a date, or a date with time."""
    now = local_now(timezone)
    if not value or not value.strip():
        return now
    value = value.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            parsed = dt.datetime.strptime(value, fmt)
        except ValueError:
            continue
        if fmt == "%Y-%m-%d":
            parsed = parsed.replace(hour=now.hour, minute=now.minute, second=now.second)
        return parsed.replace(tzinfo=now.tzinfo)
    fail(f"could not parse --date {value!r} (expected YYYY-MM-DD or YYYY-MM-DD HH:MM[:SS])")


def parse_tags(value):
    tags = [slugify(tag) for tag in re.split(r"[,\n]", value or "")]
    tags = [tag for tag in tags if tag and tag != BASE_TAG]
    return [BASE_TAG] + tags


def yaml_scalar(value):
    """Quote only when the plain form would be ambiguous to a YAML parser."""
    value = " ".join(value.split())
    if not value:
        return '""'
    risky_start = value[0] in "-?:,[]{}#&*!|>'\"%@`"
    if risky_start or ": " in value or value.endswith(":") or " #" in value:
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def render(title, date, description, url, tags, body):
    front_matter = [
        "---",
        "layout: post",
        f"title: {yaml_scalar(title)}",
        f"date: {date.strftime('%Y-%m-%d %H:%M:%S %z')}",
        f"description: {yaml_scalar(description)}",
        f"redirect: {url}",
        f"categories: [{', '.join(CATEGORIES)}]",
        f"tags: [{', '.join(tags)}]",
        "related_posts: false",
        "---",
    ]
    return "\n".join(front_matter) + "\n\n" + body.strip() + "\n"


def next_news_path(news_dir):
    """Next free announcement_<n>.md, continuing the numbering of the existing news items."""
    numbers = [int(match.group(1)) for path in news_dir.glob("*.md") if (match := re.fullmatch(r"announcement_(\d+)\.md", path.name))]
    return news_dir / f"announcement_{max(numbers, default=0) + 1}.md"


def render_news(date, text, url):
    """Inline news item: the text followed by a link to the LinkedIn post."""
    text = " ".join(text.split())
    if not text.endswith((".", "!", "?")):
        text += "."
    front_matter = [
        "---",
        "layout: post",
        f"date: {date.strftime('%Y-%m-%d %H:%M:%S %z')}",
        "inline: true",
        "related_posts: false",
        "---",
    ]
    return "\n".join(front_matter) + "\n\n" + f"{text} [{NEWS_LINK_TEXT}]({url}).\n"


def created(path):
    log(f"created {path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path}")
    print(path)


def main():
    parser = argparse.ArgumentParser(description="Mirror a LinkedIn post as a stub post in _posts/ and a news item in _news/.")
    parser.add_argument("--url", required=True, help="URL of the LinkedIn post")
    parser.add_argument("--title", required=True, help="Title shown on the blog")
    parser.add_argument("--description", default="", help="One-sentence summary shown in the blog list")
    parser.add_argument("--tags", default="", help="Extra tags, comma separated ('linkedin' is always added)")
    parser.add_argument("--date", default="", help="YYYY-MM-DD or YYYY-MM-DD HH:MM[:SS] (default: now)")
    parser.add_argument("--body", default=DEFAULT_BODY, help="Body text of the stub post")
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE, help=f"IANA timezone for the post date (default: {DEFAULT_TIMEZONE})")
    parser.add_argument("--posts-dir", default=str(DEFAULT_POSTS_DIR), help="Directory to write the post into")
    parser.add_argument("--news-text", default="", help="Text of the news item on the about page (default: the title)")
    parser.add_argument("--news-dir", default=str(DEFAULT_NEWS_DIR), help="Directory to write the news item into")
    parser.add_argument("--no-news", action="store_true", help="Only create the post, without a news item")
    parser.add_argument("--force", action="store_true", help="Write even if this LinkedIn post is already mirrored")
    args = parser.parse_args()

    posts_dir = Path(args.posts_dir)
    if not posts_dir.is_dir():
        fail(f"posts directory not found: {posts_dir}")
    news_dir = Path(args.news_dir)
    if not args.no_news and not news_dir.is_dir():
        fail(f"news directory not found: {news_dir}")

    url = normalize_url(args.url)
    title = " ".join(args.title.split())
    if not title:
        fail("--title is empty")

    existing = find_existing(posts_dir, url)
    if existing and not args.force:
        fail(f"this LinkedIn post is already mirrored in {existing} (use --force to add it again)")

    date = parse_date(args.date, args.timezone)
    slug = slugify(title, MAX_SLUG_WORDS) or slugify(activity_id(url) or "linkedin-post")
    path = posts_dir / f"{date.strftime('%Y-%m-%d')}-{slug}.md"
    if path.exists() and not args.force:
        fail(f"{path} already exists (use --force to overwrite)")

    description = args.description.strip()
    if not description:
        log("warning: no --description given; the blog list will show an entry without a summary")

    path.write_text(render(title, date, description, url, parse_tags(args.tags), args.body), encoding="utf-8")
    created(path)

    if args.no_news:
        return
    existing_news = find_existing(news_dir, url)
    if existing_news and not args.force:
        log(f"warning: {existing_news} already links to this LinkedIn post; not adding another news item")
        return
    news_path = next_news_path(news_dir)
    news_path.write_text(render_news(date, args.news_text.strip() or title, url), encoding="utf-8")
    created(news_path)


if __name__ == "__main__":
    main()
