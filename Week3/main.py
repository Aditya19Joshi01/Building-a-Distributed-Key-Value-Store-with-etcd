
from flask import Flask, render_template, request, redirect, url_for
import etcd3
import grpc

app = Flask(_name_)

# Define etcd connection
client = etcd3.client(host='localhost', port=2379)

def list_all_keys():
    try:
        keys = [metadata.key.decode('utf-8') for _, metadata in client.get_all()]
        return keys
    except etcd3.exceptions.ConnectionFailedError as e:
        print(f"Error: {e}")
        return []

def get_value_for_key(key):
    value, _ = client.get(key)
    if value is not None:
        return value.decode()
    else:
        return None

def put_key_value(key, value):
    try:
        client.put(key, value)
        return True
    except grpc.RpcError:
        return False

def delete_key(key):
    try:
        client.delete(key)
        return True
    except KeyError:
        return False
    except grpc.RpcError:
        return False

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/all_keys_values')
def all_keys_values():
    try:
        keys = list_all_keys()
        key_value_pairs = []
        for key in keys:
            value = get_value_for_key(key)
            key_value_pairs.append({'key': key, 'value': value})
        return render_template('all_keys_values.html', key_value_pairs=key_value_pairs)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/put', methods=['GET', 'POST'])
def put_key_value_page():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
        if put_key_value(key, value):
            return redirect(url_for('all_keys_values'))
        else:
            return "Error putting key-value into etcd."
    return render_template('put_key_value.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_key_page():
    error = None
    if request.method == 'POST':
        key = request.form['key']
        if key not in list_all_keys():
            error = "Error: Key does not exist."
        else:
            if delete_key(key):
                return redirect(url_for('all_keys_values'))
            else:
                error = "Error deleting key from etcd."
    return render_template('delete_key.html', error=error)

@app.route('/get_value', methods=['GET', 'POST'])
def get_value_page():
    error = None
    if request.method == 'POST':
        key = request.form['key']
        value = get_value_for_key(key)
        if value is not None:
            return render_template('get_value.html', value=value)
        else:
            error = "Key not found."
    return render_template('get_value.html', error=error)

if _name_ == '_main_':
    app.run(debug=True)
