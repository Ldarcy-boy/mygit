import json
from flask import Flask, render_template, request
from util.config import Module_Config
from util.connect_to_db import connect
from module.weld_module import get_pie_compare_data, get_line_no_list, get_defects_type_and_weld_no_list, get_location_defects_sum_data

c = connect()
app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', input_text='', res_text='')


@app.route('/save_data', methods=['POST'])
def save_data():
    info = request.get_json()
    if info['type'] == 'string':
        db = c['STRING']
        data = db.data
        data.insert_one(info['data'])
    return 'OK', 200


@app.route('/get_line_list_no', methods=['GET'])
def get_line_list_no():
    return_obj_list = get_line_no_list()
    return json.dumps(return_obj_list, ensure_ascii=False)


@app.route('/weld_pie_compare', methods=['GET'])
def weld_pie_compare():
    if Module_Config['weld_pie_compare']:
        return render_template('weld_pie_compare.html', input_text='', res_text='')
    else:
        return render_template('error.html', input_text='', res_text='')


@app.route('/get_weld_pie_compare', methods=['GET'])
def get_weld_pie_compare():
    return_obj_list = get_pie_compare_data(request.args['line_no'],
                                           int(request.args['start_time']),
                                           int(request.args['end_time']))
    return json.dumps(return_obj_list, ensure_ascii=False)


@app.route('/weld_defects_location_el', methods=['GET'])
def weld_defects_location():
    if Module_Config['weld_defects_location_el']:
        return render_template('weld_defects_location_el.html', input_text='', res_text='')
    else:
        return render_template('error.html', input_text='', res_text='')


@app.route('/weld_defects_location_ab', methods=['GET'])
def weld_defects_location_ab():
    if Module_Config['weld_defects_location_ab']:
        return render_template('weld_defects_location_ab.html', input_text='', res_text='')
    else:
        return render_template('error.html', input_text='', res_text='')


@app.route('/get_defects_type_and_weld_no', methods=['GET'])
def get_defects_type_and_weld_no():
    return_obj_list = get_defects_type_and_weld_no_list(request.args['line_no'])
    return json.dumps(return_obj_list, ensure_ascii=False)


@app.route('/get_location_defects_sum', methods=['POST'])
def get_location_defects_sum():
    request_obj = json.loads(list(dict(request.form).keys())[0])
    return_obj_list = get_location_defects_sum_data(request_obj['line_no'],
                                                    request_obj['start_time'],
                                                    request_obj['end_time'],
                                                    request_obj['weld_list'],
                                                    request_obj['defects_list'],
                                                    request_obj['side'])
    return json.dumps(return_obj_list, ensure_ascii=False)


if __name__ == '__main__':
    app.run('127.0.0.1', 8090)
