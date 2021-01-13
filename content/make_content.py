import os
import random

languages = {
    'az': 'Azerbaijani',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'cz': 'Czech',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'eu': 'Basque',
    'fi': 'Finnish',
    'kk': 'Kazakh',
    'lv': 'Latvian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'sr': 'Seriban',
    'vi': 'Vietnamese',
}

html_template = '''
<h3 contenteditable ><i>{header}</i></h3>
<h4 contenteditable lang="{lang_tag}">{subhead}</h4>

<p contenteditable class="opsz_text" lang="{lang_tag}">
{content}
</p>

<div class="columns opsz_caption">
<p contenteditable">
{content_small}
</p>
<p lang="en">
This sample text was assembled from the <a href="{url_a}">{language_a}</a> and <a href="{url_b}">{language_b}</a> Wikipedia pages about the the {animal}.
They were sampled in November 2020, and lightly edited for typography.
</p>
</div>
'''


def text_to_html(animal, filenames):
    format_dict = {}
    output_dict = {}
    format_dict['animal'] = animal.title()

    for filename in filenames:
        animal, lang_tag = os.path.splitext(filename)[0].split('-')
        with open(filename, 'r') as f:
            data = f.read()

        format_dict.setdefault('lang_tag', []).append(
            lang_tag)
        format_dict.setdefault('language', []).append(
            languages.get(lang_tag, 'no language'))

        header, subhead, content, url = data.split('\n\n')
        format_dict.setdefault('header', []).append(header)
        format_dict.setdefault('subhead', []).append(subhead)
        format_dict.setdefault('content', []).append(content)
        format_dict.setdefault('url', []).append(url)

    output_dict = format_dict.copy()
    options = range(len(filenames))
    choice_a = random.choice(options)
    choice_b = next((i for i in options if i is not choice_a), choice_a)
    output_dict['header'] = format_dict['header'][choice_a]
    output_dict['subhead'] = format_dict['subhead'][choice_b]
    lang_tag_a = format_dict['lang_tag'][choice_a]
    lang_tag_b = format_dict['lang_tag'][choice_b]
    output_dict['language_a'] = languages.get(lang_tag_a)
    output_dict['language_b'] = languages.get(lang_tag_b)
    output_dict['url_a'] = format_dict['url'][choice_a]
    output_dict['url_b'] = format_dict['url'][choice_b]
    content_a = format_dict['content'][choice_a].split('\n')
    content_b = format_dict['content'][choice_b].split('\n')

    if len(filenames) > 1:
        content = ''
        content_small = ''
        content_list_a = []
        content_list_b = []

        while content_a:
            content_list_a.append(
                f'<span lang="{lang_tag_a}">{content_a.pop(0)}</span>')
        while content_b:
            content_list_b.append(
                f'<span lang="{lang_tag_b}">{content_b.pop(0)}</span>')

        for p_index, pair in enumerate(
            list(zip(content_list_a, content_list_b))
        ):
            if p_index % 2 == 0:
                content += pair[choice_a] + ' '
                content_small += pair[choice_b] + ' '
            else:
                content += pair[choice_b] + ' '
                content_small += pair[choice_a] + ' '

    else:
        content = (
            f'<span lang="{lang_tag_a}">' +
            '\n'.join(content_a) + '</span>')
        content_small = (
            f'<span lang="{lang_tag_a}">' +
            '\n'.join(content_a) + '</span>')

    output_dict['content'] = content
    output_dict['content_small'] = content_small

    output_path = os.path.join('..', '_includes', f'{animal}.html')
    html_data = html_template.format(**output_dict)
    with open(output_path, 'w') as htmlfile:
        htmlfile.write(html_data)


animals = {}
for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    if os.path.splitext(file)[-1].lower() == '.txt':
        animal, _ = os.path.splitext(file)[0].split('-')
        animals.setdefault(animal, []).append(file)
for animal, text_files in animals.items():
    print(text_files)
    text_to_html(animal, text_files)

        # text_to_html(file)
