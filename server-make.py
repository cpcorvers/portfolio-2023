from ruamel.yaml import YAML
from jinja2 import Environment, FileSystemLoader
import glob
import datetime
import operator
from pathlib import Path

# (un)comment before uploading to web
# outputfile = 'output'
# site = {'title': 'local cp.corvers',
#         'url': '../output',
#         'home': 'index.html',
#         'pathtoimages': '../../content/images/', }
site = {'title': 'cp.corvers', 'url': 'https://www.cpcorvers.nl'}
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

# for work in worklist:
#     print(work['title'], work['modal-id'])
#
# render pages fr m templates
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