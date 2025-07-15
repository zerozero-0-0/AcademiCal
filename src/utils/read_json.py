import json

def read_json(file_path):
    try:
        json_open = open(file_path, 'r')
        json_load = json.load(json_open)
        json_open.close()
        
        return json_load
    except FileNotFoundError:
        print(f"Error: {file_path} が見つかりません")
        return None

