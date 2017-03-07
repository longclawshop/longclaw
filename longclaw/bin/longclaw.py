from __future__ import absolute_import, print_function, unicode_literals
import argparse
import sys
from os import path
from django.core.management import ManagementUtility
import longclaw

def create_project(args):
    '''
    Create a new django project using the longclaw template
    '''

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
        '--ext=html,css,js,py,txt',
        args.project_name
    ))
    utility.execute()
    print("{} has been created.".format(args.project_name))

def main():
    '''
    Setup the parser and call the command function
    '''
    parser = argparse.ArgumentParser(description='Longclaw CLI')
    subparsers = parser.add_subparsers()
    start = subparsers.add_parser('start', help='Create a Wagtail+Longclaw project')
    start.add_argument('project_name', help='Name of the project')
    start.set_defaults(func=create_project)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
