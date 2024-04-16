from flask import Flask, render_template, request, redirect, url_for
import etcd3
import grpc

app = Flask(_name_)

# Define etcd connection
client = etcd3.client(host='localhost', port=2379)

def list_all_keys():
    keys = []
    for _, metadata in client.get_all():
        keys.append(metadata.key.decode('utf-8'))
    return keys
    
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
def index():
    return render_template('index.html', keys=list_all_keys())

@app.route('/put', methods=['POST'])
def put():
    key = request.form['key']
    value = request.form['value']
    if put_key_value(key, value):
        return redirect(url_for('index'))
    else:
        return "Error putting key-value into etcd."

@app.route('/get_value', methods=['POST'])
def get():
    key = request.form['key']
    value = get_value_for_key(key)
    if value is not None:
        keys = list_all_keys()  # Retrieve all keys
        return render_template('index.html', value=value,keys=keys)
    else:
        return "Key not found."

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    if delete_key(key):
        return redirect(url_for('index'))
    else:
        return "Error deleting key from etcd."

if _name_ == 'main':
    app.run(debug=True)
