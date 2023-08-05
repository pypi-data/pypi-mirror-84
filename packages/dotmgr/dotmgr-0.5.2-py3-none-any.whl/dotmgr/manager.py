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
"""A module for dotfile management classes and service functions.
"""

from functools import reduce
from getpass import getuser
from operator import add
from os import chmod, listdir, makedirs, remove, stat
from os.path import dirname, isabs, isdir, join
from socket import gethostname

from dotmgr.paths import home_path, orig_path, repo_path
from dotmgr.transformer import Transformer


def _copy_permissions(src_path, dest_path):
    """Applies the file mode of the source file to the target file.

    Args:
        source_path (str): path to the source file
        target_path (str): path to the target file
    """
    chmod(dest_path, stat(src_path).st_mode)

class Manager:
    """An instance of this class can be used to manage dotfiles.

    Attributes:
        dotfile_repository:      The dotfile repository.
        dotfile_tag_config_path: The absolute path to the dotfile tag configuration file.
        verbose:                 If set to `True`, debug messages are generated.
    """

    def __init__(self, repository, tag_config_path, verbose):
        self.dotfile_repository = repository
        self.dotfile_tag_config_path = tag_config_path
        self.verbose = verbose
        self._user = getuser()
        self._tags = self._get_tags()

    def _get_tags(self):
        """Parses the dotmgr config file and extracts the tags for the current host.

        Reads the hostname and searches the dotmgr config for a line defining tags for the host.

        Returns:
            The tags defined for the current host.
        """
        hostname = gethostname()
        tag_config = None
        with open(self.dotfile_tag_config_path, encoding='utf-8') as config:
            tag_config = config.readlines()

        for line in tag_config:
            if line.startswith(hostname + ':'):
                tags = line.split(':')[1]
                tags = tags.split()
                if self.verbose:
                    print('Found tags: {}'.format(', '.join(tags)))
                return tags
        print('Warning: No tags found for this machine!')
        return [""]

    def _recurse_repo_dir(self, directory_path, action, *args):
        """Recursively performs an action on all dotfiles in a directory.

        Args:
            directory_path: The relative path to the directory to recurse into.
            action: The action to perform.
            args:   The arguments to the action.
        """
        for entry in listdir(self.repo_path(directory_path)):
            entry_path = join(directory_path, entry)
            if isdir(self.repo_path(entry_path)):
                self._recurse_repo_dir(entry_path, action, *args)
            else:
                try:
                    action(entry_path, *args)
                except FileNotFoundError:
                    pass

    def _recurse_repository(self, action, *args):
        """Recursively performs an action on all dotfiles in the repository.

        Args:
            action: The action to perform.
            args:   The arguments to the action.
        """
        for entry in listdir(self.dotfile_repository.path):
            if entry == '.git':
                continue
            if isdir(self.repo_path(entry)):
                self._recurse_repo_dir(entry, action, *args)
            else:
                try:
                    action(entry, *args)
                except FileNotFoundError:
                    pass


    def delete(self, dotfile_path, commit):
        """Removes a dotfile from $HOME.

        Args:
            dotfile_path: The relative path to the dotfile to remove.
            commit:       If `True`, the removal is automatically committed to the repository.
        """
        print('Removing {} from repository'.format(dotfile_path))
        try:
            remove(self.repo_path(dotfile_path))
        except FileNotFoundError:
            print('Warning: {} is not in the repository'.format(dotfile_path))

        if commit:
            self.dotfile_repository.remove(dotfile_path)

    def generalize(self, dotfile_path, commit, message=None):
        """Generalizes a dotfile from $HOME.

        Identifies and un-comments blocks deactivated for this host.
        The generalized file is written to the repository.

        Args:
            dotfile_path: The relative path to the dotfile to generalize.
            commit:       If `True`, the changes are automatically committed to the repository.
            message:      An optional commit message. If omitted, a default message is generated.
        """
        def _commit_file():
            if not commit:
                return
            if dotfile_path not in self.dotfile_repository.lsfiles():
                self.dotfile_repository.add(dotfile_path, commit, message)
            elif dotfile_path in self.dotfile_repository.lsfiles(modified=True):
                self.dotfile_repository.update(dotfile_path, message)

        flt = None
        src_path = orig_path(dotfile_path)
        dst_path = self.repo_path(dotfile_path)
        old_content = None
        try:
            with open(dst_path, encoding='utf-8') as generic_dotfile:
                old_content = generic_dotfile.readlines()

            flt = Transformer(self._tags, self._user, self.verbose)
            header_info = flt.parse_header(old_content)
            if 'skip' in header_info and header_info['skip']:
                if self.verbose:
                    print('Skipping {} as requested in its header'.format(dotfile_path))
                return
            if 'path' in header_info:
                src_path = header_info['path']
                if not isabs(src_path):
                    src_path = home_path(dotfile_path)
        except FileNotFoundError:
            old_content = []

        content = None
        try:
            with open(src_path, encoding='utf-8') as specific_dotfile:
                content = specific_dotfile.readlines()
        except FileNotFoundError as err:
            print('Error: File {0} not found.'.format(dotfile_path))
            raise err
        if not content:
            print('Ignoring empty file {0}'.format(dotfile_path))
            raise FileNotFoundError

        if not flt:
            flt = Transformer(self._tags, self._user, self.verbose)
        content = flt.generalize(content)

        if not old_content:
            print('Creating ' + self.repo_path(dotfile_path, relative=True))
            makedirs(dirname(dst_path), exist_ok=True)
            # Print notice if file is not in $HOME and lacks dotmgr header with path specification
            header_info = flt.parse_header(content.split('\n'))
            if not src_path.startswith(home_path()) and 'path' not in header_info:
                print('Original file is not within your $HOME directory.\n' +
                      'You should consider adding a dotmgr header and specifying its destination.')

        old_content = reduce(add, old_content, '')
        if content != old_content:
            with open(dst_path, 'w', encoding='utf-8') as dotfile:
                dotfile.write(content)
            print('Generalized ' + self.repo_path(dotfile_path, relative=True))

        _copy_permissions(src_path, dst_path)
        _commit_file()

    def generalize_all(self, commit):
        """Generalizes all dotfiles in $HOME that have a pendant in the repository.

        Results are written directly to respective files in the repository.

        Args:
            commit: If `True`, the changes are automatically committed to the VCS.
        """
        print('Generalizing all dotfiles')
        self._recurse_repository(self.generalize, commit)

    def list_active_tags(self):
        """Lists all tag specifications matching the current host and user.
        """
        active_tags = Transformer(self._tags, self._user, self.verbose).tags
        active_tags += [tag.lstrip('{}@'.format(self._user)) for tag in active_tags]
        return ['{}@*'.format(self._user)] + active_tags

    def list_managed_files(self):
        """Lists all files currently managed by dotmgr.

        Respects `#path`- and `#use`-directives.

        Returns:
            a list of absolute paths to managed files
        """
        managed_files = []
        for path in self.dotfile_repository.lsfiles():
            with open(join(self.dotfile_repository.path, path), encoding='utf-8') as dotfile:
                content = dotfile.readlines()
            flt = Transformer(self._tags, self._user, self.verbose)
            header_info = flt.parse_header(content)
            if 'skip' in header_info and header_info['skip']:
                if self.verbose:
                    print('Skipping {} as requested in its header'.format(path))
                continue
            path = header_info.get('path', path)
            managed_files.append(path)
        return managed_files


    def repo_path(self, dotfile_path, relative=False):
        """Returns path to a named dotfile in the repository.

        Args:
            dotfile_path: Path to the dotfile whose repository path should by synthesized.
            relative:     If `true`, returns a path relative to the dotfile repository root.

        Returns:
            The absolute or relative path to the dotfile in the repository.
        """
        return repo_path(self.dotfile_repository.path, dotfile_path, relative)

    def specialize(self, dotfile_path):
        """Specializes a dotfile from the repository.

        Identifies and comments out blocks not valid for this host.
        The specialized file is written to the $HOME directory.

        Args:
            dotfile_path: The relative path to the dotfile to specialize.
        """

        src_path = self.repo_path(dotfile_path)
        dotfile_content = None
        try:
            with open(src_path, encoding='utf-8') as generic_dotfile:
                dotfile_content = generic_dotfile.readlines()
        except FileNotFoundError:
            print('{0} is not in the specified dotfile repository. :-('.format(dotfile_path))
        if not dotfile_content:
            print('Ignoring empty file {0}'.format(dotfile_path))
            return

        flt = Transformer(self._tags, self._user, self.verbose)
        header_info = flt.parse_header(dotfile_content)
        if 'skip' in header_info and header_info['skip']:
            if self.verbose:
                print('Skipping {} as requested in its header'.format(dotfile_path))
            return
        specific_content = flt.specialize(dotfile_content)

        dest_path = orig_path(dotfile_path)
        if 'path' in header_info:
            dest_path = header_info['path']
            if not isabs(dest_path):
                dest_path = home_path(dotfile_path)

        makedirs(dirname(dest_path), exist_ok=True)
        try:
            with open(dest_path, encoding='utf-8') as dotfile:
                old_content = dotfile.read()
                if old_content == specific_content:
                    return
        except FileNotFoundError:
            print('Creating ' + self.repo_path(dotfile_path, relative=True))

        with open(dest_path, 'w', encoding='utf-8') as dotfile:
            dotfile.write(specific_content)
        _copy_permissions(src_path, dest_path)
        print('Specialized ' + self.repo_path(dotfile_path, relative=True))

    def specialize_all(self):
        """Specializes all dotfiles in the repository and writes results to $HOME."""

        print('Specializing all dotfiles')
        self._recurse_repository(self.specialize)
