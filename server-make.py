from ruamel.yaml import YAML
from jinja2 import Environment, FileSystemLoader
import glob
import datetime
import operator
from pathlib import Path
import shutil
# import os

site = {'title': 'cp.corvers',
        'url': 'https://www.cpcorvers.nl',
        'home': 'index.html',
        'pathtoimages': '../../images/'}
outputfile = 'docs'
language = ['en', 'nl']
pages = ['index', 'vision', 'techniques', 'workportfolio',
         'workshops', 'tools', 'about', 'vakmakerij']

# load yml datafiles from /content/data
# datafiles = ['workshops', 'navigation', 'testimonials', 'techniques', 'techniques_intro',
# 'tools', 'tools_intro', 'about', 'about_intro', 'vision_intro', 'vakmakerij', 'workshop_intro']

with open("content/data/workshops.yml") as f:
    yaml = YAML(typ="safe", pure=True)
    workshops = yaml.load(f)

with open("content/data/navigation.yml") as g:
    yaml = YAML(typ="safe", pure=True)
    navigation = yaml.load(g)

with open("content/data/testimonials.yml") as h:
    yaml = YAML(typ="safe", pure=True)
    testimonials = yaml.load(h)

with open("content/data/techniques.yml") as j:
    yaml = YAML(typ="safe", pure=True)
    techniques = yaml.load(j)

with open("content/data/techniques_intro.yml") as m:
    yaml = YAML(typ="safe", pure=True)
    techniques_intro = yaml.load(m)

with open("content/data/tools.yml") as k:
    yaml = YAML(typ="safe", pure=True)
    tools = yaml.load(k)

with open("content/data/tools_intro.yml") as k:
    yaml = YAML(typ="safe", pure=True)
    tools_intro = yaml.load(k)

with open("content/data/about.yml") as i:
    yaml = YAML(typ="safe", pure=True)
    about = yaml.load(i)

with open("content/data/about_intro.yml") as i:
    yaml = YAML(typ="safe", pure=True)
    about_intro = yaml.load(i)

with open("content/data/vision_intro.yml") as n:
    yaml = YAML(typ="safe", pure=True)
    vision_intro = yaml.load(n)

with open("content/data/vakmakerij.yml") as o:
    yaml = YAML(typ="safe", pure=True)
    vakmakerij = yaml.load(o)

with open("content/data/workshop_intro.yml") as p:
    yaml = YAML(typ="safe", pure=True)
    workshops_intro = yaml.load(p)

# load yml datafiles from content/work
worklist = []
datafiles_work = glob.glob('content/work/*.yml')
for file in datafiles_work:
    with open(file) as j:
        yaml = YAML(typ="safe", pure=True)
        work = yaml.load(j)
        worklist.append(work)

# sorted() the items in worklist so they are presented in the intended order
worklist = sorted(worklist, key=operator.itemgetter('modal-id'))

# copy imagery to the docs directory for upload to server
# define source and destination directory
src_dir = './content/images/'
dst_dir = Path(f'./{outputfile}/images/')
# create the destination directory if it doesn't exist
Path(dst_dir).mkdir(exist_ok=True, parents=True)
# get list of all files in source directory with the glob.py library
# by setting the root_dir to source directory glob only returns filenames
imagery = glob.glob('*.*', root_dir=src_dir)
# copy all files in the source directory to the destination using shutil.py
for image in imagery:
    src_file = Path(f"{src_dir}{image}")
    dst_file = Path(f"{dst_dir}/{image}")
    shutil.copy2(src_file, dst_file)

# copy css files to the docs directory for upload to server
# define source and destination directory
src_dir = './theme/css/'
dst_dir = Path(f'./{outputfile}/')
# create the destination directory if it doesn't exist
Path(dst_dir).mkdir(exist_ok=True, parents=True)
# get list of all files in source directory with the glob.py library
# by setting the root_dir to source directory glob only returns filenames
stylesheet = glob.glob('*.css', root_dir=src_dir)
# copy all files in the source directory to the destination using shutil.py
for css in stylesheet:
    src_file = Path(f"{src_dir}{css}")
    dst_file = Path(f"{dst_dir}/{css}")
    shutil.copy2(src_file, dst_file)

# render pages from templates
# and write html to a file
fileloader = FileSystemLoader("theme/templates")
env = Environment(loader=fileloader)

for lang in language:
    for page in pages:
        if page == 'index':
            filename = f'/{page}.html'
        else:
            filename = f'/{page}/index.html'
        filelocation = Path(f"{outputfile}/{lang}/{filename}")
        rendered = env.get_template(f'{page}.html').render(
            navigation=navigation,
            pagetitle=page,
            lang=lang,
            pageurl=filename,
            techniques=techniques,
            techniques_intro=techniques_intro,
            worklist=worklist,
            workshops_intro=workshops_intro,
            workshops=workshops,
            tools=tools,
            tools_intro=tools_intro,
            about=about,
            about_intro=about_intro,
            vision_intro=vision_intro,
            testimonials=testimonials,
            vakmakerij=vakmakerij,
            site=site)
        filelocation.parent.mkdir(exist_ok=True, parents=True)
        with open(f"{filelocation}", "w") as f:
            f.write(rendered)

for lang in language:
    for work in worklist:
        page = 'workpost'
        filename = f"/{work['pagetitle']}/index.html"
        filelocation = Path(
            f"{outputfile}/{lang}/{work['pagetitle']}/index.html")
        rendered = env.get_template(f'{page}.html').render(
            navigation=navigation,
            lang=lang,
            pageurl=filename,
            work=work,
            site=site)
        filelocation.parent.mkdir(exist_ok=True, parents=True)
        with open(f"{filelocation}", "w") as f:
            f.write(rendered)

print('rendered: ', datetime.datetime.now())
