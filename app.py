"""
# -*- coding: utf-8 -*-
@Time    : 8/10/2021 12:06 AM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""
import json

import flask.json
from flask import Flask, send_from_directory, request
import _thread
import sys
import os
import subprocess
import time
import pickle as pkl
from project import Project

url = 'http://localhost:5607'

app = Flask(__name__)


@app.route('/')
def root():
    with open('./templates/index.html', encoding='utf-8') as f:
        return f.read()


@app.route('/favicon.ico')
def ico():
    return send_from_directory('./templates', 'favicon.ico')


@app.route('/submit_settings', methods=['POST'])
def submit_settings():
    content = request.json
    cn_list = content['cn_list'].split('\n')
    en_list = content['en_list'].split('\n')
    if len(cn_list) != len(en_list):
        return flask.json.jsonify({'status': 'error', 'msg': '中英文补充字典文件长度不统一'})
    with open('./upload/rules.txt', 'w', encoding='utf-8') as f:
        f.write(content['rules'])
    with open('./upload/cn_list.txt', 'w', encoding='utf-8') as f:
        f.write(content['cn_list'])
    with open('./upload/en_list.txt', 'w', encoding='utf-8') as f:
        f.write(content['en_list'])
    dict_list = []
    for each in os.listdir('./upload/dict'):
        dict_list.append('./upload/dict/' + each)
    suite_list = []
    for each in os.listdir('./upload/suite'):
        suite_list.append('./upload/suite/' + each)
    _thread.start_new_thread(process_settings, (
        dict_list, suite_list, cn_list, en_list, content['rules']
    ))
    return flask.json.jsonify({'status': 'success'})


@app.route('/get_settings', methods=['GET'])
def get_settings():
    dict_file_list = []
    files = os.listdir('./upload/dict')
    for i in range(len(files)):
        dict_file_list.append({
            'uid': i,
            'name': files[i],
            'status': 'done'
        })
    suite_file_list = []
    files = os.listdir('./upload/suite')
    for i in range(len(files)):
        suite_file_list.append({
            'uid': i,
            'name': files[i],
            'status': 'done'
        })
    with open('./upload/rules.txt', encoding='utf-8') as f:
        rules = f.read()
    with open('./upload/cn_list.txt', encoding='utf-8') as f:
        cn_list = f.read()
    with open('./upload/en_list.txt', encoding='utf-8') as f:
        en_list = f.read()
    return flask.json.jsonify({
        'dict_file_list': dict_file_list,
        'suite_file_list': suite_file_list,
        'rules': rules,
        'cn_list': cn_list,
        'en_list': en_list
    })


@app.route('/upload_dict', methods=['POST'])
def upload_dict():
    ff = request.files['file']
    save_path = './upload/dict'
    ff.save(os.path.join(save_path, ff.filename))
    return flask.json.jsonify({'status': 'done'})


@app.route('/upload_suite', methods=['POST'])
def upload_suite():
    ff = request.files['file']
    save_path = './upload/suite'
    ff.save(os.path.join(save_path, ff.filename))
    return flask.json.jsonify({'status': 'done'})


@app.route('/del_dict', methods=['POST'])
def del_dict():
    content = request.json
    try:
        os.remove('./upload/dict/' + content['file'])
        return flask.json.jsonify({'status': 'success'})
    except Exception as e:
        return flask.json.jsonify({'status': 'failed', 'msg': str(e)})


@app.route('/del_suite', methods=['POST'])
def del_suite():
    content = request.json
    try:
        os.remove('./upload/suite/' + content['file'])
        return flask.json.jsonify({'status': 'success'})
    except Exception as e:
        return flask.json.jsonify({'status': 'failed', 'msg': str(e)})


@app.route('/status')
def status():
    if project.state != 1:
        return flask.json.jsonify({'state': project.state, 'error': project.error})
    return flask.json.jsonify({'state': project.state, 'data': project.get_result()})


@app.route('/edit_fields', methods=['POST'])
def edit_fields():
    try:
        field = request.json
        project.update_items(field['data'])
        save_project()
        return json.dumps({'status': 'success'})
    except Exception as e:
        return flask.json.jsonify({'status': 'failed', 'msg': str(e)})



def run_app():
    app.run(port=5607)


def open_brower():
    if sys.platform == 'win32':
        os.system("start " + url)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print('Please open a browser on: ' + url)


def init_project():
    global project
    try:
        with open('./project.pkl', 'rb') as f:
            project = pkl.load(f)
    except FileNotFoundError:
        'Project not found, creating a new one'
        project = Project()


def save_project():
    with open('./project.pkl', 'wb') as f:
        pkl.dump(project, f)


def process_settings(udd_path, log_path, cn_list, en_list, rules):
    try:
        project.init_all(udd_path, log_path, cn_list, en_list, rules)
        save_project()
    except Exception as e:
        print('Exception at process_settings(),', str(e))


if __name__ == '__main__':
    project = Project()
    _thread.start_new_thread(run_app, ())
    _thread.start_new_thread(open_brower, ())
    _thread.start_new_thread(init_project, ())
    while True:
        time.sleep(3600)
