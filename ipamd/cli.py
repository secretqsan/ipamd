"""
IPAMD CLI Tool
"""
import argparse
import json
import os
from shutil import unpack_archive, make_archive, rmtree, copyfile
from ipamd.public import shared_data

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

def install_plugin(plugin_filename):
    """
    Install a plugin from the file

    Args:
        plugin_filename (str): The filename of the plugin to install
    """
    temp_dir = f"{os.path.splitext(plugin_filename)[0]}_packed"
    try:
        unpack_archive(plugin_filename, temp_dir)
    except Exception as e:
        raise ValueError(f"Failed to unpack plugin {plugin_filename}: {e}") from e
    with open(os.path.join(temp_dir, "meta.json"), 'r', encoding='utf-8') as f:
        meta = json.load(f)
    meta_path = os.path.join(shared_data.module_installation_dir, "meta")
    copyfile(
        os.path.join(temp_dir, "meta.json"),
        os.path.join(meta_path, f"{meta["name"]}_meta.json")
    )
    plugin_dir = os.path.join(shared_data.module_installation_dir, "plugins")
    install_dependency(meta['dep'])
    for plugin_class in meta["scripts"]:
        scripts = meta["scripts"][plugin_class]
        target_dir = os.path.join(plugin_dir, plugin_class)
        os.makedirs(target_dir, exist_ok=True)
        for script in scripts:
            src_dir = os.path.join(temp_dir, script)
            copyfile(src_dir, os.path.join(target_dir, script))
    rmtree(temp_dir)
    print(f"Plugin {meta['name']} installed")

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
    for plugin_class in meta["scripts"]:
        target_dir = os.path.join(plugin_dir, plugin_class)
        for script in meta["scripts"][plugin_class]:
            os.remove(os.path.join(target_dir, script))
    print(f"Plugin {plugin_name} removed")
    os.remove(meta_file)

def pack_plugin(plugin_dir):
    """
    Pack a plugin directory into a zip file

    Args:
        plugin_dir (str): The directory to pack
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
    parser.add_argument('--install-plugin', help='Install a plugin from the file')
    parser.add_argument('--pack', help='Pack a plugin from the file')
    parser.add_argument('--list-plugin', action='store_true', help='List all installed plugin packs')
    parser.add_argument('--version', action='version', version='0.0.16')
    parser.add_argument('--remove-plugin', help='Remove a plugin pack')
    args = parser.parse_args()
    
    if args.list_plugin:
        list_plugins()
    elif args.install_plugin:
        install_plugin(args.install_plugin)
    elif args.pack:
        pack_plugin(args.pack)
    elif args.remove_plugin:
        remove_plugin(args.remove_plugin)
    else:
        print("No action specified. Use --install-plugin to install a plugin.")

if __name__ == "__main__":
    main()
