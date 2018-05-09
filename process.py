#!/usr/bin/env python

import os
import glob
import yaml
import shutil
import jinja2

join = os.path.join

DIR = os.path.abspath('.')
DIR_IN = join(DIR, 'items')
DIR_OUT = join(DIR, 'docs')
DIR_OUTIMG = join(DIR_OUT, 'img')

tmpl = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./templates'),
    undefined=jinja2.StrictUndefined,
)


def find_image(base):
    extensions = ['png', 'jpg', 'jpeg']
    for ext in extensions:
        fn = '{}.{}'.format(base, ext)
        
        if os.path.exists(fn):
            return fn


def clean_up():
    files = glob.glob(join(DIR_OUT, '*.html'))
    for fn in files:
        os.remove(fn)

    files = glob.glob(join(DIR_OUTIMG, '*'))
    for fn in files:
        os.remove(fn)


def generate_index():
    files = glob.glob(join(DIR_IN, '*.yaml'))
    files = list(reversed(sorted(files)))

    items = []
    for fn in files:
        name, ext = os.path.splitext(fn)

        fn_yaml = fn
        fn_img0 = find_image(name)
        fn_img1 = join(DIR_OUTIMG, os.path.basename(fn_img0))

        shutil.copy(fn_img0, fn_img1)

        item = {'imgurl': join('img', os.path.basename(fn_img1))}
        item.update(yaml.load(open(fn_yaml)))

        template = tmpl.get_template('./image.html')
        html = template.render(item=item)

        fn_html = 'img_{}.html'.format(os.path.basename(name))
        fn_html = join(DIR_OUT, fn_html)
        with open(fn_html, 'w') as f:
            f.write(html)

        item.update({'link': os.path.basename(fn_html)})
        items.append(item)

    template = tmpl.get_template('./index.html')
    item = template.render(items=items)

    with open(join(DIR_OUT, 'index.html'), 'w') as fn:
        fn.write(item)
    

if __name__ == '__main__':
    clean_up()
    generate_index()
