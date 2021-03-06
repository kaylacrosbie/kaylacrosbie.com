#!/usr/bin/env python

import os
import glob
import yaml
import shutil
import jinja2
from PIL import Image

join = os.path.join

DIR = os.path.abspath('.')
DIR_ITEMS = join(DIR, 'items')
DIR_GEN = join(DIR, 'items-generated')
THUMBNAIL_WIDTH = 500
THUMBNAIL_EXTENSION = '.jpg'


def tpl_newlines(text):
    return text.replace('\n', '<br/>')

tmpl = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./templates'),
    undefined=jinja2.StrictUndefined,
)

tmpl.globals.update({'newlines': tpl_newlines})


def url(filepath):
    return join('/', filepath.replace(DIR, ''))

def path_gen(filename):
    name = os.path.basename(filename)
    return join(DIR_GEN, name)

def image_size(filename):
    im = Image.open(filename)
    return im.size

def create_thumbnail(filename):
    name, ext = os.path.splitext(filename)
    outfile = '{}-thumb{}'.format(name, THUMBNAIL_EXTENSION)
    outfile = path_gen(outfile)

    im = Image.open(filename)
    if im.size[0] > THUMBNAIL_WIDTH:
        width = THUMBNAIL_WIDTH
        height = int(im.size[1] / im.size[0] * width)
        im = im.resize((width, height), resample=Image.LANCZOS)
    im = im.convert('RGB')

    with open(outfile, 'wb') as fn:
        im.save(fn)

    return outfile

def find_image(base):
    extensions = ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']
    for ext in extensions:
        fn = '{}.{}'.format(base, ext)
        
        if os.path.exists(fn):
            return fn

def clean_up():
    files = glob.glob(join(DIR_ITEMS, '*.html'))
    for fn in files:
        os.remove(fn)

    files = glob.glob(join(DIR_ITEMS, '*-thumb.jpg'))
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
        fn_thm = create_thumbnail(fn_img)

        item = {
            'thumb': url(fn_thm),
            'imgurl': url(fn_img)
        }
        item.update(yaml.load(open(fn_yaml)))

        fn_html = '{}.html'.format(os.path.basename(name))
        fn_html = path_gen(fn_html)
        with open(fn_html, 'w') as f:
            template = tmpl.get_template('./image.html')
            html = template.render(item=item)
            f.write(html)

        item.update({'link': url(fn_html)})
        items.append(item)

    template = tmpl.get_template('./index.html')
    item = template.render(items=items)

    with open(join(DIR, 'index.html'), 'w') as fn:
        fn.write(item)
    
if __name__ == '__main__':
    clean_up()
    generate_index()
