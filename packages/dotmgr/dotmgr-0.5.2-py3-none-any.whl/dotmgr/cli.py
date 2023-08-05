#!/usr/bin/env python3
#
# This file is part of dotmgr.
#
# dotmgr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dotmgr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dotmgr.  If not, see <http://www.gnu.org/licenses/>.
"""Dotfile manager CLI

A small script that can help you maintain your dotfiles across several devices.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter, REMAINDER
from os import chdir
from sys import argv
from textwrap import dedent, indent

from pkg_resources import require

from dotmgr.manager import Manager
from dotmgr.paths import DEFAULT_DOTFILE_REPOSITORY_PATH, DEFAULT_DOTFILE_TAG_CONFIG_PATH, \
                         home_path, orig_path, prepare_repository_path, prepare_tag_config_path
from dotmgr.repository import Repository

def get_version():
    """Returns the program version."""
    return require('dotmgr')[0].version

def prepare_argument_parser():
    """Creates and configures the argument parser for the CLI.
    """
    parser = ArgumentParser(usage=indent(dedent("""
                    dotmgr [-h]
                    dotmgr [-v] -I           [path]
                    dotmgr [-v] -D [-c | -s] <path>
                    dotmgr [-v] -G [-c | -s] [path] [message]
                    dotmgr [-v] -S      [-s] [path]
                    dotmgr [-v] -Q <-f | -l | -r | -t>
                    dotmgr [-v] -V <command...>
                            """), '  '),
                            description='Generalize / specialize dotfiles',
                            epilog=dedent("""\
                    default paths and environment variables:
                      General dotfiles are read from / written to {}.
                      You can set the environment variable $DOTMGR_REPO to change this.

                      Tags are read from ~/{}, which can be changed
                      by setting $DOTMGR_TAG_CONF.

                    version:
                      This is version {} of dotmgr.
                            """).format(DEFAULT_DOTFILE_REPOSITORY_PATH,
                                        DEFAULT_DOTFILE_TAG_CONFIG_PATH,
                                        get_version()),
                            formatter_class=RawDescriptionHelpFormatter,
                            add_help=True)
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='enable verbose output (useful for debugging)')

    acts = parser.add_argument_group('actions').add_mutually_exclusive_group(required=True)
    acts.add_argument('-D', dest='delete', action='store_true',
                      help='remove a dotfile from the repository')
    acts.add_argument('-G', dest='generalize', action='store_true',
                      help='generalize a tracked dotfile in your home directory')
    acts.add_argument('-I', dest='init', action='store_true',
                      help='clone a dotfile repository from the given <path> or initialize an '
                           'empty one if <path> is omitted')
    acts.add_argument('-Q', dest='query', action='store_true',
                      help='query certain settings and parameters of dotmgr')
    acts.add_argument('-S', dest='specialize', action='store_true',
                      help='specialize a dotfile from the repository')
    acts.add_argument('-V', dest='command', nargs=REMAINDER, metavar='arg',
                      help='run a git command in the dotfile repository')

    parser.add_argument('path', nargs='?', default=None,
                        help='a relative path to a dotfile - if omitted, the requested action is '
                             'performed for all dotfiles')
    parser.add_argument('message', nargs='?', default=None,
                        help='a commit message for git')

    vcs_opts = parser.add_argument_group('VCS options').add_mutually_exclusive_group()
    vcs_opts.add_argument('-c', dest='commit', action='store_true',
                          help='commit changes to the dotfile repository')
    vcs_opts.add_argument('-s', dest='sync', action='store_true',
                          help='synchronize repository before / after operation (implies -c)')

    query_opts = parser.add_argument_group('query options').add_mutually_exclusive_group()
    query_opts.add_argument('-f', dest='tag_conf', action='store_true',
                            help='the (absolute) path to dotmgr\'s tag configuration file')
    query_opts.add_argument('-l', dest='files', action='store_true',
                            help='list of (relative) paths to dotfiles managed by dotmgr')
    query_opts.add_argument('-r', dest='repo', action='store_true',
                            help='the (absolute) path to the dotfile repository')
    query_opts.add_argument('-t', dest='tags', action='store_true',
                            help='all tag specifications matching the curent machine and user')

    return parser

def dotmgr(args):
    """dotmgr CLI

    Args:
        args ([string]):    command-line arguments
    """
    def delete():
        """Helper function for the -D action.
        """
        if not args.path:
            parser.print_usage()
            exit()
        manager.delete(args.path, args.commit or args.sync)
        if args.sync:
            repository.push()

    def generalize():
        """Helper function for the -G action.
        """
        try:
            if args.path:
                manager.generalize(args.path, args.commit or args.sync, args.message)
            else:
                chdir(home_path())
                manager.generalize_all(args.commit or args.sync)
        except FileNotFoundError:
            return
        if args.sync:
            repository.push()

    def query():
        """Helper function for the -Q action.
        """
        if args.files:
            print('\n'.join(manager.list_managed_files()))
        elif args.repo:
            print(dotfile_repo_path)
        elif args.tag_conf:
            print(dotfile_conf_path)
        elif args.tags:
            print('\n'.join(manager.list_active_tags()))
        exit()

    def specialize():
        """Helper function for the -S action.
        """
        if args.sync:
            repository.pull()
        if args.path:
            manager.specialize(args.path)
        else:
            chdir(home_path())
            manager.specialize_all()

    # Check and parse arguments
    parser = prepare_argument_parser()
    args = parser.parse_args(args)

    # Prepare paths
    dotfile_repo_path = prepare_repository_path(args.init, args.verbose)
    dotfile_conf_path = prepare_tag_config_path(args.init, args.verbose, dotfile_repo_path)
    if args.path and orig_path(args.path).startswith(dotfile_repo_path):
        chdir(home_path())

    # If desired, initialize or clone the dotfile repository and exit
    repository = Repository(dotfile_repo_path, args.verbose)
    if args.init:
        if args.path:
            repository.clone(args.path)
        else:
            repository.initialize(dotfile_conf_path)
        exit()

    # Fire up dotfile manager instance
    manager = Manager(repository, dotfile_conf_path, args.verbose)

    # Execute selected action
    if args.delete:
        delete()
    elif args.generalize:
        generalize()
    elif args.specialize:
        specialize()
    elif args.query:
        query()
    elif args.command:
        repository.execute(args.command)

def main():
    """Program entry point.

    Where things start to happen...
    """
    dotmgr(argv[1:])
