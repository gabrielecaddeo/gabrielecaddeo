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

## Deployment

Changes pushed to the `main` branch are built and deployed automatically to
GitHub Pages by the repository's
[deployment workflow](https://github.com/gabrielecaddeo/gabrielecaddeo/actions/workflows/deploy.yml).

## Acknowledgements

This website is built with [Jekyll](https://jekyllrb.com/) and the
[al-folio](https://github.com/alshedivat/al-folio) academic theme.
