import collections
import datetime
import io
import json
import os
import re
import requests

from flask import Flask, render_template, request, redirect, Response, send_file, abort, url_for
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, content_security_policy=None)

try:
    app.config['GA_TRACKING_ID'] = os.environ['GA_TRACKING_ID']
except:
    print('Tracking ID not set')

page_names = ["home", "projects", "experiences", "playing", "resume", "appml"]

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/terminal_input', methods=['POST'])
def terminal_input():
    input = request.form['response']
    input = input.split(" ")
    if len(input) == 2:
        input[1] = str(input[1])
        pattern = re.compile("projects/(.*)")
        if input[0] == "cd" and (input[1] in page_names or bool(pattern.match(input[1]))):
            try:
                if '/' in list(input[1]):
                    return redirect(url_for('.project', title=input[1].split('/')[1]))
                return redirect(url_for(input[1]), 308)
            except:
                return redirect(url_for('.index'), 308)
        else:
            return redirect(url_for('.index'), 308)
    else:
        return redirect(url_for('.index'), 308)

@app.route('/playing', methods=['GET', 'POST'])
def playing():
    data = get_static_json("static/playing.json")
    return render_template('playing.html', data=data)


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', projects=data, tag=tag)

@app.route('/experiences', methods=['GET', 'POST'])
def experiences():
    experiences = get_static_json("static/experiences/experiences.json")['experiences']
    experiences.sort(key=order_projects_by_weight, reverse=True)
    return render_template('projects.html', projects=experiences, tag=None)


def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0


@app.route('/projects/<title>', methods=['GET', 'POST'])
def project(title):
    projects = get_static_json("static/projects/projects.json")['projects']
    experiences = get_static_json("static/experiences/experiences.json")['experiences']

    in_project = next((p for p in projects if p['link'] == title), None)
    in_exp = next((p for p in experiences if p['link'] == title), None)

    if in_project is None and in_exp is None:
        return render_template('404.html'), 404
    # fixme: choose the experience one for now, cuz I've done some bad hardcoding here.
    elif in_project is not None and in_exp is not None:
        selected = in_exp
    elif in_project is not None:
        selected = in_project
    else:
        selected = in_exp

    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "experiences" if in_exp is not None else "projects"
        selected['description'] = io.open(get_static_file(
            'static/%s/%s/%s.html' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()
    return render_template('project.html', project=selected)

@app.route('/resume', methods=['GET', 'POST'])
def resume():
    return render_template('resume.html')

@app.route('/appml', methods=['GET', 'POST'])
def appml():
    informal_list = []
    formal_list = []
    
    informal = requests.get(url = 'https://api.github.com/repos/pasolano/appml/contents/informal', headers={'Accept': 'application/vnd.github.v3+json'})
    informal = informal.json()

    formal = requests.get(url = 'https://api.github.com/repos/pasolano/appml/contents/formal', headers={'Accept': 'application/vnd.github.v3+json'})
    formal = formal.json()

    for item in informal:
        informal_list.append(item["download_url"])
    for item in formal:
        formal_list.append(item["download_url"])
    informal_list = convert_dates(informal_list)
    return render_template('appml.html', informal=informal_list, formal=formal_list)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))

def convert_dates(filenames):
    dates = {}
    for filename in filenames:
        parts_of_path = filename.split('/')
        info = parts_of_path[len(parts_of_path)-1][:-3].split('-')
        info[0] = info[0].title()
        if info[0] == 'Feb' or info[0] == 'February':
            month = 200
        elif info[0] == 'Mar' or info[0] == 'March':
            month = 300
        elif info[0] == 'Apr' or info[0] == 'April':
            month = 400
        elif info[0] == 'May':
            month = 500
        else:
            month = 0
        if len(info) == 2:
            date = month + int(info[1])
        else:
            date = month
        dates[date] = filename
    od = collections.OrderedDict(sorted(dates.items(), reverse=True))
    new_filename_order = []
    for value in od.values():
        new_filename_order.append(value)
    return new_filename_order


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
