import datetime
import io
import json
import os
import re

from flask import Flask, render_template, request, redirect, Response, send_file, abort, url_for
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, content_security_policy=None)

try:
    app.config['GA_TRACKING_ID'] = os.environ['GA_TRACKING_ID']
except:
    print('Tracking ID not set')

page_names = ["home", "projects", "experiences", "playing", "resume"]

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
    # fixme: choose the experience one for now, cuz I've done some shite hardcoding here.
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))

if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
