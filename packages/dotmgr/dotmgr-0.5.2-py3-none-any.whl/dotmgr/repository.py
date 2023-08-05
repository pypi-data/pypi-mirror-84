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
"""A module for dotfile repository management classes and service functions.
"""

from os import makedirs
from os.path import dirname, isdir, isfile, join
from socket import gethostname
import sys

from git import Repo
from git.cmd import Git
from git.exc import GitCommandError, GitCommandNotFound, InvalidGitRepositoryError


class Repository:
    """An instance of this class can be used to manage dotfiles.

    Attributes:
        path:    The absolute path to the dotfile repository.
        verbose: If set to `True`, debug messages are generated.
    """

    def __init__(self, repository_path, verbose):
        self.path = repository_path
        self.verbose = verbose
        self._git_instance = None

    def _commit_file(self, dotfile_path, message):
        """Commit helper function.

        Args:
            dotfile_path: The relative path to the dotfile to commit.
            message:      A commit message.
        """
        print('Committing {}'.format(dotfile_path))
        _exec_fancy(lambda: self._git().stage(dotfile_path))
        _exec_fancy(lambda: self._git().commit(message=message))

    def _git(self):
        """Singleton factory for the Git object.
        """
        if not self._git_instance:
            try:
                self._git_instance = Repo(self.path).git
                # Check if we can actually execute git commands
                try:
                    self._git_instance.rev_parse()
                except GitCommandNotFound:
                    print('Error: Could not find the git executable. Is git installed?')
                    sys.exit()
            except InvalidGitRepositoryError:
                print('Error: {} is not a git repository!\n'
                      '       You can try running `dotmgr -I` to initialize it.'.format(self.path))
                sys.exit()
        return self._git_instance

    def add(self, dotfile_path, commit=False, message=None):
        """Adds and commits a new dotfile.

        Args:
            dotfile_path: The relative path to the dotfile to commit.
        """
        if commit:
            if not message:
                message = 'Add {}'.format(dotfile_path)
            self._commit_file(dotfile_path, message)
        else:
            _exec_fancy(lambda: self._git().stage(dotfile_path))
            print('Staged new dotfile {}'.format(dotfile_path))

    def clone(self, url):
        """Clones a dotfile repository.

        Args:
            url: The URL of the repository to clone.
        """
        print('Cloning {} into {}'.format(url, self.path))
        _exec_raw(lambda: Git().clone(url, self.path))

    def execute(self, args):
        """Executes a git command in the dotfile repository.

        Args:
            args (array): Command line arguments for git.
        """
        command = 'git -c color.ui=always'.split() + args
        if self.verbose:
            print('Executing `{}`'.format(' '.join(command)))
        output = _exec_raw(lambda: self._git().execute(command), _default_error_handler)
        if output:
            print(output)

    def initialize(self, tag_config_path):
        """Initializes an empty git repository and creates and commits an initial tag configuration.

        If the repository already exists, only the tag configuration file is created and committed.

        Args:
            tag_config_path: The (relative) path to the dotfile tag configuration.
        """
        if not isdir(self.path):
            print('Initializing empty repository in {}'.format(self.path))
            _exec_raw(lambda: Git().init(self.path))

        try:
            self._git().rev_parse()
        except InvalidGitRepositoryError:
            print('Initializing repository in existing directory {}'.format(self.path))
            _exec_raw(lambda: Git(self.path).init())

        full_path = join(self.path, tag_config_path)
        if not isfile(full_path):
            print('Creating initial tag configuration')
            makedirs(dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as tag_config:
                tag_config.write('{0}: {0}'.format(gethostname()))
            self.add(tag_config_path)

    def lsfiles(self, modified=False):
        """Executes `git ls-files` and returns its results.
        """
        args = None
        if modified:
            args = '--modified'
        return _exec_raw(lambda: self._git().ls_files(args).split('\n'))

    def push(self):
        """Pushes to upstream.
        """
        print('Pushing to upstream')
        _exec_fancy(lambda: self._git().push())

    def pull(self):
        """Pulls from upstream.
        """
        print('Pulling from upstream')
        _exec_fancy(lambda: self._git().pull())

    def remove(self, dotfile_path):
        """Commits the removal of a dotfile.

        Args:
            dotfile_path: The relative path to the dotfile to remove.
        """
        print('Committing removal of {}'.format(dotfile_path))
        _exec_fancy(lambda: self._git().rm(dotfile_path, cached=True))
        _exec_fancy(lambda: self._git().commit(message='Remove {}'.format(dotfile_path)))

    def update(self, dotfile_path, message=None):
        """Commits changes to a dotfile.

        Args:
            dotfile_path: The relative path to the dotfile to commit.
            message:      A commit message. If omitted, a default message is generated.
        """
        # Skip if the file has not changed
        if not self._git().diff(dotfile_path, name_only=True):
            if self.verbose:
                print('File {} has not changed - skipping commit'.format(dotfile_path))
            return

        if not message:
            message = 'Update {}'.format(dotfile_path)
        self._commit_file(dotfile_path, message)

def _default_error_handler(error):
    cmdline = ' '.join(error.command)
    print('Error: Execution of the command\n'
          '       {}\n'
          '       failed with the following message:'.format(cmdline))
    print(error.args[2].decode('utf-8'))
    sys.exit(error.status)

def _exec_fancy(command_func):
    """Executes a git command and handles errors gracefully.

    In case of errors a note on what failed and how to re-try the operation is printed and program
    execution is aborted.

    Args:
        command_func:   A function that executes a git command.
    """
    def _error_handler(error):
        def quote(string):
            if not ' ' in string:
                return string
            if not '=' in string:
                return "'" + string + "'"
            return string.replace('=', "='", 1) + "'"
        tokens = [quote(token) for token in error.command]
        args = ' '.join(tokens[1:])
        cmdline = ' '.join([tokens[0], args])
        print('Error: Sorry, something went wrong during execution of `{}`. :-(\n'
              '       You can execute `dotmgr -V {}` to try again and find out what happened.'
              .format(cmdline, args))
        sys.exit(error.status)
    _exec_raw(command_func, _error_handler)

def _exec_raw(command_func, error_handler=None):
    """Executes a git command.

    Args:
        command_func:   A function that executes a git command.
        error_handler:  A function that handles a GitCommandError. The function must take the
                        caught GitCommand error as a function parameter.
                        May be `None`, in which case the executed command line and stderr are
                        dumped and program execution is aborted.

    Returns:
        The output of the executed git command as a string.
    """
    try:
        return command_func()
    except GitCommandError as err:
        if error_handler:
            error_handler(err)
        else:
            _default_error_handler(err)
