"""
IPAMD CLI Tool
"""
import argparse
import json
import os
from shutil import unpack_archive, make_archive, rmtree, copyfile

import requests

from ipamd.public import shared_data
from ipamd.public.utils.output import warning

def list_plugins():
    """
    List all installed plugin packs
    """
    meta_dir = os.path.join(shared_data.module_installation_dir, "meta")
    for meta_file in os.listdir(meta_dir):
        if meta_file.endswith("_meta.json"):
            meta_file = os.path.join(meta_dir, meta_file)
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                print(meta["name"])

def show_examples():
    """
    Show examples of ipamd
    """
    print("Examples of ipamd:")
    print("")
    print("Active Examples:")
    print("  1. single_chain_simulation    - Run a single chain simulation")
    print("    @ https://github.com/secretqsan/ipamd/tree/master/demo/single_chain_simulation")
    print("  2. sequence_analysis          - Perform analysis on protein sequences")
    print("    @ https://github.com/secretqsan/ipamd/tree/master/demo/sequence_analysis")
    print("  3. basic_example              - Droplet simulation and contact analysis")
    print("    @ https://github.com/secretqsan/ipamd/tree/master/demo/basic_example")
    print("  4. slab_simulation            - Slab simulation with plotting")
    print("    @ https://github.com/secretqsan/ipamd/tree/master/demo/slab_simulation")
    print("  5. RNA+Protein                - Simulate RNA and protein systems")
    print("    @ https://github.com/secretqsan/ipamd/tree/master/demo/RNA+Protein")
    print("  6. custom_system              - Create custom molecular systems")
    print("    @ https://github.com/secretqsan/ipamd/tree/master/demo/custom_system")
    print("")

def install_plugin(plugin_filename):
    """
    Install a plugin from the file

    Args:
        plugin_filename (str): The filename of the plugin to install
    """
    plugin_format = ""
    online_installation = False
    if not os.path.exists(plugin_filename):
        plugin_filename = f"{plugin_filename}.zip"
        base_url = "https://raw.githubusercontent.com/secretqsan/ipamd/refs/heads/master"
        target_url = f"{base_url}/plugin_packs/zipped/{plugin_filename}"
        print(f"Downloading plugin {plugin_filename} from {target_url}")
        try:
            response = requests.get(target_url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            raise ValueError(f"Failed to download plugin {plugin_filename}: {e}") from e
        with open(plugin_filename, 'wb') as f:
            f.write(response.content)
        online_installation = True

    if os.path.isdir(plugin_filename):
        temp_dir = plugin_filename
    else:
        temp_dir = f"{os.path.splitext(plugin_filename)[0]}_unpacked"
        try:
            unpack_archive(plugin_filename, temp_dir)
            plugin_format = "archive"
        except Exception as e:
            raise ValueError(f"Failed to unpack plugin {plugin_filename}: {e}") from e
    with open(os.path.join(temp_dir, "meta.json"), 'r', encoding='utf-8') as f:
        meta = json.load(f)
    meta_dir = os.path.join(shared_data.module_installation_dir, "meta")
    meta_filename = os.path.join(meta_dir, f"{meta["name"]}_meta.json")
    if os.path.exists(meta_filename):
        warning(
            f"Plugin {meta['name']} already installed. The older version will be replaced."
        )
        remove_plugin(meta["name"])

    copyfile(
        os.path.join(temp_dir, "meta.json"),
        meta_filename
    )
    global_meta_file = os.path.join(meta_dir, "global.json")
    with open(global_meta_file, 'r', encoding='utf-8') as f:
        global_meta = json.load(f)
    install_dependency(meta['dep'])
    def copy_files(base_dir, section):
        if section not in meta:
            return
        for class_name in meta[section]:
            target_dir = os.path.join(base_dir, class_name)
            os.makedirs(target_dir, exist_ok=True)
            scripts = meta[section][class_name]
            for file in scripts:
                src_dir = os.path.join(temp_dir, file)
                pid = f"{class_name}@{file}"
                if pid not in global_meta:
                    global_meta[pid] = 1
                else:
                    warning(
                        f"{file} already installed, please check if there is a name conflict."
                    )
                    global_meta[pid] += 1
                copyfile(src_dir, os.path.join(target_dir, file))
    plugin_dir = os.path.join(shared_data.module_installation_dir, "plugins")
    copy_files(plugin_dir, "scripts")
    data_dir = os.path.join(shared_data.module_installation_dir, "data")
    copy_files(data_dir, "data")
    with open(global_meta_file, 'w', encoding='utf-8') as f:
        json.dump(global_meta, f, indent=4)
    if plugin_format == "archive":
        rmtree(temp_dir)
    if online_installation:
        os.remove(plugin_filename)

    print(f"Plugin {meta['name']} installed")
    print(f"\nINFO: {meta["info"]}")

def install_dependency(dependencies):
    """
    Install dependencies for a plugin

    Args:
        dependencies (list): A list of dependencies to install
    """
    for dep in dependencies:
        os.system(f"pip install {dep}")

def remove_plugin(plugin_name):
    """
    Remove a plugin from the installation directory

    Args:
        plugin_name (str): The name of the plugin to remove
    """
    meta_dir = os.path.join(shared_data.module_installation_dir, "meta")
    meta_file = os.path.join(
        meta_dir,
        f"{plugin_name}_meta.json"
    )
    plugin_dir = os.path.join(shared_data.module_installation_dir, "plugins")
    if not os.path.exists(meta_file):
        raise ValueError(f"Plugin {plugin_name} not installed")
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    global_meta_file = os.path.join(meta_dir, "global.json")
    with open(global_meta_file, 'r', encoding='utf-8') as f:
        global_meta = json.load(f)
    def remove_files(base_dir, section):
        if section not in meta:
            return
        for class_name in meta[section]:
            target_dir = os.path.join(base_dir, class_name)
            for file in meta[section][class_name]:
                pid = f"{class_name}@{file}"
                global_meta[pid] -= 1
                if global_meta[pid] == 0:
                    del global_meta[pid]
                    os.remove(os.path.join(target_dir, file))
    remove_files(plugin_dir, "scripts")
    data_dir = os.path.join(shared_data.module_installation_dir, "data")
    remove_files(data_dir, "data")

    with open(global_meta_file, 'w', encoding='utf-8') as f:
        json.dump(global_meta, f, indent=4)
    print(f"Plugin {plugin_name} removed")
    os.remove(meta_file)

def pack_plugin(plugin_dir):
    """
    Pack a plugin directory into a zip file

    @param plugin_dir (str): The directory to pack
    """

    meta_file = os.path.join(plugin_dir, "meta.json")
    if not os.path.exists(meta_file):
        raise FileNotFoundError(f"Meta file {meta_file} not found in {plugin_dir}")
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    filename = meta['name']
    make_archive(filename, 'zip', plugin_dir)
    print(f"{filename}.zip is created")

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description="IPAMD CLI Tool")
    parser.add_argument('-i', '--install-plugin', metavar='plugin', help='Install a plugin from the file')
    parser.add_argument('-p', '--pack', metavar='plugin_dir', help='Pack a plugin from the file')
    parser.add_argument(
        '-l', '--list-plugin', action='store_true', help='List all installed plugin packs'
    )
    parser.add_argument('-v', '--version', action='version', version='0.0.28')
    parser.add_argument('-r', '--remove-plugin', metavar='plugin_name', help='Remove a plugin pack')
    parser.add_argument('-s', '--show-examples', action='store_true', help='Show examples of ipamd')
    args = parser.parse_args()

    if args.list_plugin:
        list_plugins()
    elif args.install_plugin:
        install_plugin(args.install_plugin)
    elif args.pack:
        pack_plugin(args.pack)
    elif args.remove_plugin:
        remove_plugin(args.remove_plugin)
    elif args.show_examples:
        show_examples()
    else:
        print("No action specified. Use -i or --install-plugin to install a plugin.")

if __name__ == "__main__":
    main()
