'''
'''

import os
import random
import _make_content

html_prologue = '''\
---
title: Source Serif 4
---

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="format-detection" content="telephone=no">
        <title>Source Serif 4</title>
        <link rel="stylesheet" href="/style.css">
        <link rel="stylesheet" href="/source-serif-var.css">
        <link rel="stylesheet" href="/source-serif-caption.css">
        <link rel="stylesheet" href="/source-serif-smtext.css">
        <link rel="stylesheet" href="/source-serif-text.css">
        <link rel="stylesheet" href="/source-serif-subhead.css">
        <link rel="stylesheet" href="/source-serif-display.css">
    </head>
    <body class="dynamic_color">
        <header class="dynamic_color sticky">
            <h1><a class="dynamic_color" href="http://github.com/adobe-fonts/source-serif-pro/releases/latest">
            Source Serif 4
            </a>
            </h1>
            <div class="links_right smcp hide_on_mobile">
                <a href="https://github.com/adobe-fonts/source-serif-pro/tree/main">fork</a>
                &ensp;|&ensp;
                <a href="http://github.com/adobe-fonts/source-serif-pro/releases/latest">fonts</a>
            </div>
        </header>
        <div class="spacer">
            &nbsp;
        </div>
        <main spellcheck="false">
'''

html_epilogue = '''\
        </main>
    </body>
</html>'''

weights = [
    'ExtraLight',
    'Light',
    'Regular',
    'Semibold',
    'Bold',
    'Black',
]

article_tag_template = (
    '            <article class="{}">\n'
    '                <h2>{}</h2>\n'
    '                {{% include {} %}}\n'
    '            </article>\n'
)

_make_content.refresh()
article_dir = os.path.join(os.path.dirname(__file__), '../_includes')
article_htmls = [
    file for file in os.listdir(article_dir) if
    os.path.splitext(file)[-1].lower() == '.html']
random.shuffle(article_htmls)

html_output = html_prologue

for w_index, weight in enumerate(weights * 2):
    article_html = article_htmls[w_index]
    html_output += article_tag_template.format(weight, weight, article_html)
html_output += html_epilogue

index_html = os.path.join(os.path.dirname(__file__), '../index.html')
with open(index_html, 'w') as html_out:
    html_out.write(html_output)
