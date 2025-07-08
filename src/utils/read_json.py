import json

def read_json(file_name):
    try:
        json_open = open(file_name, 'r')
        json_load = json.load(json_open)
        json_open.close()
        
        return json_load
    except FileNotFoundError:
        print(f"Error: {file_name} が見つかりません")
        return None

