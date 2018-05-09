#!/usr/bin/env python

import os
import glob
import yaml
import shutil
import jinja2

join = os.path.join

DIR = os.path.abspath('.')
DIR_ITEMS = join(DIR, 'items')

def tpl_newlines(text):
    return text.replace('\n', '<br/>')

tmpl = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./templates'),
    undefined=jinja2.StrictUndefined,
)

tmpl.globals.update({'newlines': tpl_newlines})

def find_image(base):
    extensions = ['png', 'jpg', 'jpeg']
    for ext in extensions:
        fn = '{}.{}'.format(base, ext)
        
        if os.path.exists(fn):
            return fn


def clean_up():
    files = glob.glob(join(DIR_ITEMS, '*.html'))
    for fn in files:
        os.remove(fn)


def generate_index():
    files = glob.glob(join(DIR_ITEMS, '*.yaml'))
    files = list(reversed(sorted(files)))

    items = []
    for fn in files:
        name, ext = os.path.splitext(fn)

        fn_yaml = fn
        fn_img = find_image(name)

        item = {'imgurl': join('/items', os.path.basename(fn_img))}
        item.update(yaml.load(open(fn_yaml)))

        template = tmpl.get_template('./image.html')
        html = template.render(item=item)

        fn_html = '{}.html'.format(os.path.basename(name))
        fn_html = join(DIR_ITEMS, fn_html)
        with open(fn_html, 'w') as f:
            f.write(html)

        item.update({'link': join('/items', os.path.basename(fn_html))})
        items.append(item)

    template = tmpl.get_template('./index.html')
    item = template.render(items=items)

    with open(join(DIR, 'index.html'), 'w') as fn:
        fn.write(item)
    

if __name__ == '__main__':
    clean_up()
    generate_index()
