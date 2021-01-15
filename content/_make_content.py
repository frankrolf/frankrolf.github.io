import os
import random

languages = {
    'az': 'Azerbaijani',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'cz': 'Czech',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'et': 'Estonian',
    'eu': 'Basque',
    'fi': 'Finnish',
    'fr': 'French',
    'hu': 'Hungarian',
    'kk': 'Kazakh',
    'lv': 'Latvian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'se': 'Swedish',
    'sk': 'Slovak',
    'sr': 'Serbian',
    'uk': 'Ukrainian',
    'vi': 'Vietnamese',
}

article_template = '''
<h3 contenteditable lang="{lang_tag_a}"><i>{header}</i></h3>
<h4 contenteditable lang="{lang_tag_b}">{subhead}</h4>

<p contenteditable class="opsz_text">
{content}</p>

<div class="columns opsz_caption">
<p class="hide_on_mobile" contenteditable>
{content_caption}</p>

<p lang="en">
This text was assembled from the
<a href="{url_a}">{language_a}</a>
and
<a href="{url_b}">{language_b}</a>
Wikipedia pages about the the {animal}.
It was sampled in Winter 2020/21, and lightly edited for typography.
</p>
</div>
'''


def text_to_html(animal, txt_files):
    format_dict = {}
    output_dict = {}
    format_dict['animal'] = animal.title()

    for txt_file in txt_files:
        txt_file_basename = os.path.basename(txt_file)
        animal, lang_tag = os.path.splitext(txt_file_basename)[0].split('-')
        with open(txt_file, 'r') as f:
            data = f.read()

        format_dict.setdefault('lang_tags', []).append(
            lang_tag)
        format_dict.setdefault('language', []).append(
            languages.get(lang_tag, 'no language'))

        header, subhead, content, url = data.split('\n\n')
        print(f'{lang_tag} content', len(content))
        for l_index, line in enumerate(content.split('\n')):
            print('\t', l_index, len(line))
        format_dict.setdefault('header', []).append(header)
        format_dict.setdefault('subhead', []).append(subhead)
        format_dict.setdefault('content', []).append(content)
        format_dict.setdefault('url', []).append(url.strip('\n'))

    output_dict = format_dict.copy()
    options = range(len(txt_files))
    choice_a = random.choice(options)
    choice_b = next((i for i in options if i is not choice_a), choice_a)
    output_dict['header'] = format_dict['header'][choice_a]
    output_dict['subhead'] = format_dict['subhead'][choice_b]
    lang_tag_a = format_dict['lang_tags'][choice_a]
    lang_tag_b = format_dict['lang_tags'][choice_b]
    output_dict['lang_tag_a'] = lang_tag_a
    output_dict['lang_tag_b'] = lang_tag_b
    output_dict['language_a'] = languages.get(lang_tag_a)
    output_dict['language_b'] = languages.get(lang_tag_b)
    output_dict['url_a'] = format_dict['url'][choice_a]
    output_dict['url_b'] = format_dict['url'][choice_b]
    content_a = format_dict['content'][choice_a].split('\n')
    content_b = format_dict['content'][choice_b].split('\n')

    if len(txt_files) > 1:
        content_body = ''
        content_caption = ''
        content_list_a = []
        content_list_b = []

        while content_a:
            content_list_a.append(
                # '<span '
                # f'lang="{lang_tag_a}">{content_a.pop(0)}'
                # '</span>'
                content_a.pop(0)
            )
        while content_b:
            content_list_b.append(
                # '<span '
                # f'lang="{lang_tag_b}">{content_b.pop(0)}'
                # '</span>'
                content_b.pop(0)
            )

        for s_index, sentences in enumerate(
            list(zip(content_list_a, content_list_b))
        ):
            # make body text in which lines alternate by language
            sentence_a = sentences[choice_a]
            sentence_b = sentences[choice_b]

            if random.random() <= .3:
                italic_toggle_open = '<i>'
                italic_toggle_close = '</i>'
            else:
                italic_toggle_open = ''
                italic_toggle_close = ''

            if s_index % 2 == 0:
                content_body += '{}<span lang="{}">{}</span>{}\n'.format(
                    italic_toggle_open,
                    lang_tag_a, sentence_a,
                    italic_toggle_close)
                content_caption += (
                    '<span lang="{}">{}</span>\n'.format(
                        lang_tag_b, sentence_b))
            else:
                content_body += '{}<span lang="{}">{}</span>{}\n'.format(
                    italic_toggle_open,
                    lang_tag_b, sentence_b,
                    italic_toggle_close)
                content_caption += (
                    '<span lang="{}">{}</span>\n'.format(
                        lang_tag_a, sentence_a))

    else:
        # only one language exists for this animal
        content_body = '\n'.join(content_a)
        content_caption = '\n'.join(content_a)

    output_dict['content'] = content_body
    output_dict['content_caption'] = content_caption

    html_file_name = animal.replace(' ', '_') + '.html'
    output_path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), '../_includes', html_file_name))
    html_data = article_template.format(**output_dict)
    with open(output_path, 'w') as htmlfile:
        htmlfile.write(html_data)


if __name__ == '__main__':
    animals = {}
    for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
        if os.path.splitext(file)[-1].lower() == '.txt':
            file_path = os.path.abspath(file)
            animal, _ = os.path.splitext(file)[0].split('-')
            animals.setdefault(animal, []).append(file_path)

    print('animals found:')
    for animal, text_files in sorted(animals.items()):
        print('❤️ ' + animal.title())
        text_to_html(animal, text_files)
