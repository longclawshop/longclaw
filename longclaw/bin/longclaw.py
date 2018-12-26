import subprocess
import argparse
import sys
from os import path
import os
from django.core.management import ManagementUtility
import longclaw

def create_project(args):
    """
    Create a new django project using the longclaw template
    """

    # Make sure given name is not already in use by another python package/module.
    try:
        __import__(args.project_name)
    except ImportError:
        pass
    else:
        sys.exit("'{}' conflicts with the name of an existing "
                 "Python module and cannot be used as a project "
                 "name. Please try another name.".format(args.project_name))

    # Get the longclaw template path
    template_path = path.join(path.dirname(longclaw.__file__), 'project_template')

    utility = ManagementUtility((
        'django-admin.py',
        'startproject',
        '--template={}'.format(template_path),
        '--extension=html,css,js,py,txt',
        args.project_name
    ))
    utility.execute()
    print("{} has been created.".format(args.project_name))

def build_assets(args):
    """
    Build the longclaw assets
    """
    # Get the path to the JS directory
    asset_path = path.join(path.dirname(longclaw.__file__), 'client')
    try:
        # Move into client dir
        curdir = os.path.abspath(os.curdir)
        os.chdir(asset_path)
        print('Compiling assets....')
        subprocess.check_call(['npm', 'install'])
        subprocess.check_call(['npm', 'run', 'build'])
        os.chdir(curdir)
        print('Complete!')
    except (OSError, subprocess.CalledProcessError) as err:
        print('Error compiling assets:  {}'.format(err))
        raise SystemExit(1)

def main():
    """
    Setup the parser and call the command function
    """
    parser = argparse.ArgumentParser(description='Longclaw CLI')
    subparsers = parser.add_subparsers()
    start = subparsers.add_parser('start', help='Create a Wagtail+Longclaw project')
    start.add_argument('project_name', help='Name of the project')
    start.set_defaults(func=create_project)

    build = subparsers.add_parser('build', help='Build the front-end assets for Longclaw')
    build.set_defaults(func=build_assets)

    args = parser.parse_args()

    # Python 3 lost the default behaviour to fall back to printing
    # help if a subparser is not selected.
    # See: https://bugs.python.org/issue16308
    # So we must explicitly catch the error thrown on py3 if
    # no commands given to longclaw
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
