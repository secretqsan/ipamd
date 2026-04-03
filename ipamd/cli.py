import argparse
import os
from ipamd.public import shared_data

def install_plugin():
    pass

def install_dependency(dependencies):
    for dep in dependencies:
        os.system(f"pip install {dep}")

def main():
    plugin_dir = os.path.join(shared_data.module_installation_dir, "plugins")
    parser = argparse.ArgumentParser(description="IPAMD CLI Tool")
    parser.add_argument('--install-plugin', action='store_true', help='Install a plugin from the file')
    args = parser.parse_args()

    if args.install_plugin:
        install_plugin()
        print(f"Plugin installed")
    else:
        print("No action specified. Use --install-plugin to install a plugin.")

if __name__ == "__main__":
    main()