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

from os import environ
from os.path import abspath, expanduser, isabs, isdir, isfile, join, relpath


DEFAULT_DOTFILE_REPOSITORY_PATH = '~/.local/share/dotmgr/repository'
DEFAULT_DOTFILE_TAG_CONFIG_PATH = '.config/dotmgr/tags.conf'
REPOSITORY_PATH_VAR = 'DOTMGR_REPO'
TAG_CONFIG_PATH_VAR = 'DOTMGR_TAG_CONF'

def home_path(path=None):
    """Returns the absolute path to a file in the user's $HOME directory.

    If the path is already an absolute path, it is not touched.

    Args:
        path: A path to a file. May be None, in which case the path to $HOME is returned.

    Returns:
        The absolute path to (the specified file in) the user's $HOME directory.
    """
    if not path:
        return expanduser('~')
    return path if isabs(path) else expanduser('~/{}'.format(path))

def orig_path(path):
    """Returns an absolute path to a file.

    If the path is already an absolute path, it is not touched.

    Args:
        path: A path to a file.

    Returns:
        An absolute path.
    """
    return path if isabs(path) else abspath(path)

def prepare_repository_path(init, verbose):
    """Synthesizes the path to the dotfile repository.

    If DOTMGR_REPO is defined, it is read from the environment and returned.
    Otherwise the DEFAULT_DOTFILE_REPOSITORY_PATH is used.

    Args:
        init:    If set to `True`, the check for the file's existence is skipped.
        verbose: If set to `True`, this function generates debug messages.

    Returns:
        The (absolute) path to the dotfile repository.
    """
    dotfile_repository_path = expanduser(DEFAULT_DOTFILE_REPOSITORY_PATH)
    if REPOSITORY_PATH_VAR in environ:
        dotfile_repository_path = environ[REPOSITORY_PATH_VAR]

    if not init and not isdir(dotfile_repository_path):
        print('Error: dotfile repository {} does not exist'.format(dotfile_repository_path))
        exit()

    if verbose:
        print('Using dotfile repository at {}'.format(dotfile_repository_path))
    return dotfile_repository_path

def prepare_tag_config_path(init, verbose, repo_root):
    """Synthesizes the path to the dotmgr tag configuation file.

    If DOTMGR_TAG_CONF is defined, it is read from the environment and returned.
    Otherwise the DEFAULT_DOTFILE_STAGE_PATH is appended to the path of the user's home directory.
    If the chosen path does not point to a file, the program exits with an error message.

    Args:
        init:       If set to `True`, a path to the config within the dotfile repository is returned
                    and the check for the file's existence is skipped.
        verbose:    If set to `True`, this function generates debug messages.
        repo_root:  The path to the dotfile repository.

    Returns:
        The (absolute) path to the tag configuration file.
    """
    dotfile_tag_config_path = expanduser('~/' + DEFAULT_DOTFILE_TAG_CONFIG_PATH)
    if TAG_CONFIG_PATH_VAR in environ:
        dotfile_tag_config_path = environ[TAG_CONFIG_PATH_VAR]
    if init or not isfile(dotfile_tag_config_path):
        dotfile_tag_config_path = repo_root + '/' + DEFAULT_DOTFILE_TAG_CONFIG_PATH

    if not init and not isfile(dotfile_tag_config_path):
        print('Error: Tag configuration file "{}" not found!\n'
              '       You can set ${} to override the default path.'\
              .format(dotfile_tag_config_path, TAG_CONFIG_PATH_VAR))
        exit()

    if verbose:
        print('Using dotfile tags config at {}'.format(dotfile_tag_config_path))
    return dotfile_tag_config_path

def repo_path(repo_root, dotfile_path, relative):
    """Returns path to a named dotfile in the repository.

    Args:
        repo_root:    Path to the dotfile repository root folder
        dotfile_path: Path to the dotfile whose repository path should by synthesized.
        relative:     If `true`, returns a path relative to the dotfile repository root.

    Returns:
        The absolute or relative path to the dotfile in the repository.
    """
    path = orig_path(dotfile_path)
    home = home_path()
    if home in path:
        path = relpath(path, home)
    else:
        path = path[1:]
    return path if relative else join(repo_root, path)
