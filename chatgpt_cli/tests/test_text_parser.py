from ..text_parser import parse_markdown

sample_markdown = """
---
published: true
title: Title of the post
description: Description of the post
layout: post
---

<figure>
    <img src="/public/img/med-badr-chemmaoui-ZSPBhokqDMc-unsplash.jpg"
         alt="An image of a block">
    <figcaption>Photo by Unsplash</figcaption>
</figure>

Some text here **bold** *italic* and some more text

> Some quote here
"""


class TestTextParser:

    def test_removes_the_frontmatter_and_html(self):
        result = parse_markdown(sample_markdown)
        assert result == (
            "Some text here bold italic and some more text\n"
            "Some quote here")
