import etcd3

# Establish connection to etcd server
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
    client.put(key, value)
    print(f"Key '{key}' with value '{value}' has been successfully put into etcd.")

def display_menu():
    print("\nMenu:")
    print("1. List all keys")
    print("2. Get value for a specific key")
    print("3. Put a key-value pair into etcd")
    print("4. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("All keys:", list_all_keys())
        elif choice == "2":
            key = input("Enter the key: ")
            value = get_value_for_key(key)
            if value is not None:
                print(f"Value for key '{key}': {value}")
            else:
                print(f"Key '{key}' not found in etcd.")
        elif choice == "3":
            key = input("Enter the key: ")
            value = input("Enter the value: ")
            put_key_value(key, value)
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if _name_ == "_main_":
    main()
