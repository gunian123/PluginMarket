import os
import json


def generate_json(directory):
    data = {}

    # 确保目标目录存在
    target_directory = directory
    if not os.path.exists(target_directory) or not os.path.isdir(target_directory):
        print("目录不存在或不是一个目录")
        return data

    # 获取目录下所有文件
    for root, _, files in os.walk(target_directory):
        relative_path = os.path.relpath(root, target_directory)
        if any(item in relative_path for item in [".", ".git"]):
            continue
        data[relative_path] = []

        # 添加文件
        for file in files:
            data[relative_path].append(file)

    return data


def get_latest_versions(directory):
    v_dict = {}
    for p1 in os.listdir(directory):
        if p1.startswith("[pkg]"):
            continue
        if os.path.isfile(os.path.join(directory, p1, "datas.json")):
            with open(
                os.path.join(p1, "datas.json"),
                encoding="utf-8",
            ) as f:
                dat = json.load(f)
                v_dict[dat["plugin-id"]] = dat["version"]
    return json.dumps(v_dict, indent=2, ensure_ascii=False)


def flush_basic_datas():
    with open("market_tree.json", encoding="utf-8") as f:
        market_d = json.load(f)
    market_d["MarketPlugins"] = {}
    market_d["Packages"] = {}
    for path in os.listdir():
        datpath = os.path.join(path, "datas.json")
        if os.path.isfile(datpath):
            with open(datpath, encoding="utf-8") as f:
                dat = json.load(f)
                if not path.startswith("[pkg]"):
                    market_d["MarketPlugins"][dat["plugin-id"]] = {
                        "name": path,
                        "author": dat["author"],
                        "version": dat["version"],
                        "plugin-type": dat["plugin-type"],
                    }
                else:
                    market_d["Packages"][path[5:]] = {
                        "plugin-ids": dat["plugin-ids"],
                        "description": dat["description"],
                        "author": dat["author"],
                        "version": dat["version"]
                    }

    format_tree_depen = {}
    format_tree_main = {}
    for k, v in market_d["MarketPlugins"].items():
        if "前置" in v["name"]:
            format_tree_depen[k] = v
        else:
            format_tree_main[k] = v
    market_d["MarketPlugins"].update(format_tree_main)
    market_d["MarketPlugins"].update(format_tree_depen)
    with open("market_tree.json", "w", encoding="utf-8") as f:
        json.dump(market_d, f, indent=2, ensure_ascii=False)


def flush_plugin_ids_map():
    mapper = {}
    for path in os.listdir():
        if path.startswith("[pkg]"):
            continue
        datpath = os.path.join(path, "datas.json")
        if os.path.isfile(datpath):
            with open(datpath, encoding="utf-8") as f:
                dat = json.load(f)
                mapper[dat["plugin-id"]] = path

    with open("plugin_ids_map.json", "w", encoding="utf-8") as f:
        json.dump(mapper, f, indent=2, ensure_ascii=False)

def get_tree(basepath: str = ""):
    dirs = {}
    for path in (os.listdir(basepath) if basepath else os.listdir()):
        new_path = os.path.join(basepath, path)
        if os.path.isfile(new_path):
            dirs[path] = 0
        else:
            if path.startswith(".") or path == "__pycache__":
                continue
            dirs[path] = get_tree(new_path)
    return dirs


if __name__ == "__main__":
    directory = "."  # 你的仓库目录

    json_data = generate_json(directory)

    # 将生成的 JSON 数据写入文件
    with open("directory.json", "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    with open("latest_versions.json", "w", encoding="utf-8") as f:
        f.write(get_latest_versions(directory))

    with open("directory_tree.json", "w", encoding="utf-8") as f:
        json.dump(get_tree(), f, indent=4, ensure_ascii=False)

    flush_basic_datas()
    flush_plugin_ids_map()
