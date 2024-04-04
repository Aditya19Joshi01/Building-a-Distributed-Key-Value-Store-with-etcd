import etcd3

# Establish connection to etcd server
client = etcd3.client(host='localhost', port=2379)

def list_all_keys():
    try:
        keys = [metadata.key.decode('utf-8') for _, metadata in client.get_all()]
        return keys
    except etcd3.exceptions.ConnectionFailedError as e:
        print(f"Error: {e}")
        return []

def get_value_for_key(key):
    try:
        value, _ = client.get(key)
        if value is not None:
            return value.decode()
        else:
            return None
    except etcd3.exceptions.KeyNotFoundError:
        print(f"Error: Key '{key}' not found in etcd.")
        return None
    except etcd3.exceptions.ConnectionFailedError as e:
        print(f"Error: {e}")
        return None

def put_key_value(key, value):
    try:
        client.put(key, value)
        print(f"Success: Key '{key}' with value '{value}' has been successfully put into etcd.")
    except etcd3.exceptions.ConnectionFailedError as e:
        print(f"Error: {e}")

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
            keys = list_all_keys()
            if keys:
                print("All keys:", keys)
        elif choice == "2":
            key = input("Enter the key: ")
            value = get_value_for_key(key)
            if value is not None:
                print(f"Value for key '{key}': {value}")
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
