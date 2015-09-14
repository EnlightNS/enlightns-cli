import os
import argparse
import subprocess

APP_NAME = "enlightns-cli"
APP_VERSION = subprocess.check_output(["git", "describe", "--long", "--tags"]).strip()

settings = dict()


### ALL SETTINGS #####

settings["app_name"] = APP_NAME
settings["app_version"] = APP_VERSION
settings["run_deps"] = [
    'python-virtualenv',
    'devscripts',
    'git',
    'equivs',
    'python-all',
    'dh-python',
    'libffi-dev',
    'libssl-dev',
]
settings["base_dir"] = os.path.dirname(os.path.abspath(__file__))
settings["install_base"] = "/usr/local/lib"
settings["install_dir"] = os.path.join(settings["install_base"], settings["app_name"] + '-' + settings["app_version"])
settings["log_dir"] = '/var/log/webapp/'
settings["venv"] = os.path.join(settings["install_dir"], 'vp')
settings["venv_distpackages"] = os.path.join(settings["venv"], 'lib/python2.7/site-packages')
settings["requirements"] = os.path.join(settings["base_dir"], "requirements.txt")


postinst = """#!/bin/bash

set -e

APP_NAME={app_name}

case "$1" in
    configure)
        for file in "`find {venv_distpackages}/ -maxdepth 1 -type d`"; do
            dir_name=$(echo "$file" | cut -d/ -f6-);
            if [[ ! -d /usr/lib/python2.7/dist-packages/$dir_name ]];then
                cp -R {venv_distpackages}/$dir_name /usr/lib/python2.7/dist-packages/$dir_name
            fi
        done;;

    abort-upgrade|abort-remove|abort-deconfigure)
    ;;

    *)
        echo "postinst called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
""".format(**settings)


def main(args):
    print '[+] Preparing....'

    if os.path.exists('stage'):
        print "[+] Directory stage exists, preserving ... "
    else:
        subprocess.call("/bin/rm -rf stage", shell=True)

    subprocess.call("/bin/rm -rf *.deb", shell=True)

    subprocess.call("mkdir -p stage/installscripts", shell=True)
    subprocess.call("mkdir -p stage" + settings["install_dir"], shell=True)

    # f = open('stage/installscripts/postinst', 'w')
    # f.write(postinst)
    # f.close()

    if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "stage/vp")):
        print "[+] Creating virtualenv"
        subprocess.call("/usr/bin/virtualenv stage/vp", shell=True)
    else:
        print "[+] Virtualenv exists, reusing"
    pip_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stage/vp/bin/pip")
    pip_cmd = "{0} install -r {1}".format(pip_path, settings["requirements"])

    print "[+] Installing pip requirements"
    subprocess.call(pip_cmd, shell=True)

    print "[+] Copying virtualenv"
    subprocess.call("cp -R stage/vp stage{0}".format(settings["install_dir"]), shell=True)

    fpm_args = ["fpm", "-s", "dir", "-t", "deb", "-n", settings["app_name"], "-v",
                settings["app_version"], "-a", "all", "-x", '"*.git"', "-x", '"*.bak\"', "-x",
                '"*.orig"', '--python-obey-requirements-txt',
                "--description", '"Automated build. No Version Control.",']

    for x in settings["run_deps"]:
        fpm_args.append('-d')
        fpm_args.append(x)

    fpm_args.append("usr")
    fpm_cmd = ' '.join(fpm_args)

    print "[+] Executing: ", fpm_cmd
    subprocess.call(fpm_cmd, cwd="./stage", shell=True)
    subprocess.call("cp stage/*.deb .", shell=True)

    print '[+] Cleaning up....'
    subprocess.call("rm -rf ./dist", shell=True)
    subprocess.call("mkdir -p ./dist", shell=True)
    subprocess.call("mv *.deb ./dist/", shell=True)
    subprocess.call("rm -rf stage/*.deb", shell=True)

    if args.scanpackages:
        print "[+] Creating Packages.gz in dist/ directory: "
        subprocess.call("dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz", cwd="./dist", shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--preserve-virtualenv", dest="preserve_venv", action="store_true",
                        default=False, help="Preserve virtual environment if exists.")
    parser.add_argument("-s", "--scanpackages", dest="scanpackages", action="store_true",
                        default=False, help="Run dpkg-scanpackages on dist dir.")
    args = parser.parse_args()
    main(args)