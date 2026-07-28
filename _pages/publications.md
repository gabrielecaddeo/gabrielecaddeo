---
layout: page
permalink: /publications/
title: Publications
description: Publications in reversed chronological order. Click for abstracts and BibTeX citations.
nav: true
nav_order: 2
---

<style>
  .publications .abbr .preview {
    width: 100%;
    height: auto;
  }

  .publications .abstract-title-toggle {
    cursor: pointer;
    text-decoration: underline;
    text-decoration-style: dotted;
    text-underline-offset: 0.2rem;
  }

  .publications .abstract-title-toggle:hover,
  .publications .abstract-title-toggle:focus-visible {
    color: var(--global-theme-color);
  }

  .publications .abstract-title-toggle:focus-visible {
    outline: 2px solid var(--global-theme-color);
    outline-offset: 0.2rem;
  }

  @media (min-width: 576px) {
    .publications ol.bibliography > li > .row > .abbr {
      flex: 0 0 25%;
      max-width: 25%;
    }

    .publications ol.bibliography > li > .row > .col-sm-8 {
      flex: 0 0 58.333333%;
      max-width: 58.333333%;
    }
  }
</style>

<script>
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".publications ol.bibliography > li").forEach((publication, index) => {
      const title = publication.querySelector(".title");
      const abstract = publication.querySelector("div.abstract.hidden");

      if (!title || !abstract) {
        return;
      }

      const abstractId = `publication-abstract-${index}`;
      title.classList.add("abstract-title-toggle");
      title.setAttribute("role", "button");
      title.setAttribute("tabindex", "0");
      title.setAttribute("aria-controls", abstractId);
      title.setAttribute("aria-expanded", "false");
      abstract.id = abstractId;

      const abstractButton = publication.querySelector(".links a.abstract");
      if (abstractButton) {
        abstractButton.hidden = true;
      }

      const toggleAbstract = () => {
        const willOpen = !abstract.classList.contains("open");

        publication.querySelectorAll(".abstract.hidden.open, .award.hidden.open, .bibtex.hidden.open").forEach((panel) => {
          panel.classList.remove("open");
        });

        abstract.classList.toggle("open", willOpen);
        title.setAttribute("aria-expanded", String(willOpen));
      };

      title.addEventListener("click", toggleAbstract);
      title.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          toggleAbstract();
        }
      });
    });
  });
</script>

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">

{% bibliography %}

</div>
