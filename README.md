# Gabriele Mario Caddeo — Personal Website

[![Deploy site](https://github.com/gabrielecaddeo/gabrielecaddeo/actions/workflows/deploy.yml/badge.svg)](https://github.com/gabrielecaddeo/gabrielecaddeo/actions/workflows/deploy.yml)

Source code for my personal academic website:

**[gabrielecaddeo.github.io/gabrielecaddeo](https://gabrielecaddeo.github.io/gabrielecaddeo/)**

I am a Postdoctoral Researcher in Robotics and Artificial Intelligence at the
Italian Institute of Technology (IIT). My research focuses on robot perception
and manipulation, particularly visuo-tactile sensing, multimodal learning, and
contact-rich interaction.

The website contains:

- research news and updates;
- publications, abstracts, BibTeX entries, and accompanying media;
- open research positions and calls;
- talks and workshops;
- student profiles;
- my curriculum vitae.

## Local development

Build the website with Jekyll:

```bash
bundle exec jekyll build
```

Alternatively, run it with Docker:

```bash
docker compose up
```

The Docker development server is available at
`http://localhost:8080/gabrielecaddeo/`.

## Mirroring LinkedIn posts

LinkedIn activity is mirrored on the blog as short entries that link back to the
original post. To add one, open the
[mirror workflow](https://github.com/gabrielecaddeo/gabrielecaddeo/actions/workflows/mirror-linkedin-post.yml),
click **Run workflow**, and paste the post's URL together with a title, a
one-sentence description, and any extra tags. The entry is committed to `_posts/`
and the site is redeployed automatically. This also works from the GitHub mobile
app, so a post can be mirrored right after publishing it.

The same entry can be created locally:

```bash
python bin/new_linkedin_post.py \
  --url "https://www.linkedin.com/posts/..." \
  --title "Title shown on the blog" \
  --description "One-sentence summary." \
  --tags "eccv-2026, robotics"
```

Mirrored posts are tagged `linkedin` and filed under the `external-posts`
category, so they can be filtered from the blog page.

## Deployment

Changes pushed to the `main` branch are built and deployed automatically to
GitHub Pages by the repository's
[deployment workflow](https://github.com/gabrielecaddeo/gabrielecaddeo/actions/workflows/deploy.yml).

## Acknowledgements

This website is built with [Jekyll](https://jekyllrb.com/) and the
[al-folio](https://github.com/alshedivat/al-folio) academic theme.
