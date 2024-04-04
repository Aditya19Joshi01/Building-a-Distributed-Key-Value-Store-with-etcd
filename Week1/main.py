import etcd3

client = etcd3.client(host='localhost', port=2379)

def list_all_keys():
    keys = []
    for key, _ in client.get_all():
        keys.append(key.decode())
    return keys

def get_value_for_key(key):
    value, _ = client.get(key)
    if value is not None:
        return value.decode()
    else:
        return None

def put_key_value(key, value):
    client.put(key, value)
    print(f"Key '{key}' with value '{value}' has been successfully put into etcd.")


def get(key):
    value,_=client.get(key)
    print(value.decode())


print("All keys : ",list_all_keys())
put_key_value("SRN", "PES2UG21CS038")
print(get_value_for_key("SRN"))
print("All keys : ",list_all_keys())
put_key_value("SRN1", "PES2UG21CS037")
print("All keys : ",list_all_keys())
put_key_value("SRN2", "PES2UG21CS015")
print("All keys : ",list_all_keys())
key1=input()
get(key1)
