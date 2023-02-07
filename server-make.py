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
        'pathtoimages': '../images/'}
outputfile = 'docs'

# load yml datafiles from /content/data
with open("content/data/workshops.yml") as f:
    yaml = YAML(typ="safe", pure=True)
    workshops = yaml.load(f)

with open("content/data/navigation.yml") as g:
    yaml = YAML(typ="safe", pure=True)
    navigation = yaml.load(g)

with open("content/data/testimonials.yml") as h:
    yaml = YAML(typ="safe", pure=True)
    testimonials = yaml.load(h)

with open("content/data/about.yml") as i:
    yaml = YAML(typ="safe", pure=True)
    about = yaml.load(i)

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

page = 'index'
rendered = env.get_template(f'{page}.html').render(
    navigation=navigation,
    pagetitle=page,
    site=site)
fileName = Path(f"./{outputfile}/{page}.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

page = 'vision'
rendered = env.get_template(f'{page}.html').render(
    navigation=navigation,
    pagetitle=page,
    site=site)
fileName = Path(f"./{outputfile}/{page}/index.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

page = ('workportfolio', 'work')
rendered = env.get_template(f'{page[0]}.html').render(
    navigation=navigation,
    worklist=worklist,
    pagetitle=page[1],
    site=site)
fileName = Path(f"./{outputfile}/{page[1]}/index.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

for work in worklist:
    page = 'workpost'
    rendered = env.get_template(f'{page}.html').render(
        navigation=navigation,
        work=work,
        site=site)
    fileName = Path(f"./{outputfile}/{work['pagetitle']}/index.html")
    fileName.parent.mkdir(exist_ok=True, parents=True)
    with open(f"{fileName}", "w") as f:
        f.write(rendered)

page = 'techniques'
rendered = env.get_template(f'{page}.html').render(
    navigation=navigation,
    pagetitle=page,
    site=site)
fileName = Path(f"./{outputfile}/{page}/index.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

page = 'workshops'
rendered = env.get_template(f'{page}.html').render(
    workshops=workshops,
    navigation=navigation,
    pagetitle=page,
    site=site)
fileName = Path(f"./{outputfile}/{page}/index.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

page = 'tools'
rendered = env.get_template(f'{page}.html').render(
    navigation=navigation,
    pagetitle=page,
    site=site)
fileName = Path(f"./{outputfile}/{page}/index.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

page = 'about'
rendered = env.get_template(f'{page}.html').render(
    about=about,
    testimonials=testimonials,
    navigation=navigation,
    pagetitle=page,
    site=site)
fileName = Path(f"./{outputfile}/{page}/index.html")
fileName.parent.mkdir(exist_ok=True, parents=True)
with open(f"{fileName}", "w") as f:
    f.write(rendered)

print('rendered: ', datetime.datetime.now())
