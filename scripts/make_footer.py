'''
Rebuild footer
'''

import os
import re

statement = '''
Source Serif is an open-source typeface for setting text in many sizes,
weights, and languages. The design of Source Serif represents a contemporary
interpretation of the transitional typefaces of
<a href="https://en.wikipedia.org/wiki/Pierre_Simon_Fournier">
Pierre-Simon Fournier</a>.
Additionally, Source Serif has been conceived as a friendly companion to
Paul D. Hunt’s
<a href="https://adobe-fonts.github.io/source-sans-pro/">
Source Sans</a>.

With six weights in five optical sizes, the Source Serif family has a total of
60 styles, shared across Roman and Italic. Nevertheless, if you are looking at
this page in a browser that supports variable fonts, only two font files will
have been loaded.
Source Serif supports the
<a href="http://adobe-type-tools.github.io/adobe-latin-charsets/adobe-latin-4.html">
Adobe Latin-4</a> character set, as well as
<a href="http://adobe-type-tools.github.io/adobe-cyrillic-charsets/adobe-cyrillic-2.html">
Cyrillic</a> and
<a href="http://adobe-type-tools.github.io/adobe-greek-charsets/adobe-greek-1.html">
Greek</a> writing systems.

Source Serif was designed by Frank Grießhammer, with contributions by
Irene Vlachou, Emilios Theofanous, Reymund Schroeder, and Thomas Thiemich.

Significant extensions of this project were made possible through
support from
<a href="https://design.google/library/variable-fonts-are-here-to-stay/">
Google Fonts</a>.
'''

person_template = '''\
<li><a href="{url}">{name}</a><br><p class="indent">{role}</p></li>'''


def make_footer():
    txt_file = os.path.join(
        os.path.dirname(__file__), '../CONTRIBUTORS.txt')
    footer_html = os.path.join(
        os.path.dirname(__file__), '../_includes/footer.html')
    with open(txt_file, 'r') as f:
        txt_data = f.read().splitlines()

    rx_person = re.compile(
        # named subgroups:
        # https://docs.python.org/3/library/re.html#re.Match.groupdict
        r'\t(?P<name>.+?) \((?P<url>.+?)\) – (?P<role>.+?) \((?P<time>.+?)\)')

    statement_paragraphs = statement.split('\n\n')
    html_output = [

        '<div class="opsz_smtext">',
    ]

    for paragraph in statement_paragraphs:
        html_output.append(f'<p class="para_padding" lang="en">{paragraph}</p>')

    html_output.extend([
        '<p>&nbsp</p>',
        '<p class="smcp">credits</p>',
        '<p><ul>'])

    role_dict = {}
    for line in txt_data:

        if line.startswith('\t'):
            rx = re.match(rx_person, line)
            if rx:
                last_name = rx.group(1).split()[-1]
                role_dict[last_name] = rx.groupdict()

    for last_name, group_dict in sorted(role_dict.items()):
        html_output.append(person_template.format(**group_dict))

    html_output.append('</ul>')
    html_output.append('<p>&nbsp</p>')
    html_output.append('© Adobe 2014–2021</div>')

    with open(footer_html, 'w') as footer:
        footer.write('\n'.join(html_output))


if __name__ == '__main__':
    make_footer()
