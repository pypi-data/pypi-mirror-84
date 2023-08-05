# What is `dotmgr`?
`dotmgr` is a little helper script you can use to manage and deploy your dotfiles or other configs
across multiple machines.

The idea is to define tags for individual hosts and/or types of devices such as "laptop",
"headless", "work", "server" and use those to filter ("specialize") dotfiles by commenting out
blocks. Therefor the dotfiles have to be decorated with markup comments controlling the filter.  
Dotfile "templates" are stored in a git repository so you can track and possibly revert your changes
or get totally schwifty by combining the powers of `dotmgr` and git branches.  
Specialized dotfiles are written directly to your home directory. Changes made to those files can
later be merged back into the repository by applying an inverted ("generalize") filter.


## Features

* Store and maintain dotfiles containing different sets of configurations in a git repository.
* Maintain specific versions of dotfiles in your home directory (or anywhere on the file system)
  and merge changes back.
* Filter files based on defined tags (or simply hostnames) and/or user name.
* Ignore files based on the same rules so they don't pollute your home directory.
* Concise command-line interface inspired by pacman.


## How it works
### Dotfile repository
Dotfile templates - also called "generic dotfiles" - are stored in a git repository. Each dotfile's
path relative to the repository's root directory is the same as relative to your home directory.

Special comments in the dotfiles are used to indicate blocks ("tagged blocks") that should either be
commented out or left intact, depending on the tags activated for a host. Lines not enclosed by a
tagged block directives are always left untouched. Note that for this to work, the first line of a
dotfile **must** begin with a comment so `dotmgr` can identify the comment character sequence
(`#` for bash, `--` for lua, `"` for vim, ...).

The dotfile repository path default is `~/.local/share/dotmgr/repository`. It can be modified using
the environment variable `$DOTMGR_REPO`.

### Tag configuration
The script relies on a simple configuration file that defines active tags for hostnames in the
following format:
```
hostnameA: tagA1 tagA2 ...
hostnameB: tagB1 tagB2 ...
```
This file is normally read from `.config/dotmgr/tags.conf` in your home directory or, if that file
does not exist, directly from dotfile repository.

If for some reason this does not suit you, setting the environment variable `$DOTMGR_TAG_CONF` lets
you override the default path. It is however not recommended.

### Command-line interface
`dotmgr`'s clean command-line interface lets you add dotfiles from your home directory to the
repository, filter (specialize/generalize) them according to your tag configuration and filter
directives or remove them from the repository in case they become obsolete. It also lets you
perform common git tasks with the flick of a switch.



# Usage
## Installation
You can install the script via `pip`, which will conveniently take care of dependencies:
```
pip install dotmgr
```

It is important that you use the Python 3 version of `pip`. If in doubt, call `pip3` explicitly:
```
pip3 install dotmgr
```

## Initial run
If you already have a repository containing your dotfiles, you can simply clone it:
```
dotmgr -I git@github.com:<user>/dotfiles.git
```
If the tag configuration is not found, `dotmgr` will automatically create one and commit it.
If you do not have a repository yet, you can let `dotmgr` create one for you:
```
dotmgr -I
```
This will also generate and commit an initial tag configuration.

When the repository is set up, you can specialize all dotfiles:
```
dotmgr -S
```

## Data- and workflow
The following diagram summarizes the data-/workflow and associated command-line parameters:

![Data flow](docs/data_flow.png)

You can tell `dotmgr` about a new dotfile it should care about by issuing:
```
dotmgr -G <file>
```
It will automatically generalize the file and copy the result to your repository.

After you have changed a file, you can re-generalize it, for example:
```
dotmgr -G .vimrc
```
Omitting the file path (which has to be a path relative to your home directory) lets you generalize
all dotfiles at once.

When files in the dotfile repository change, you can apply those changes to your dotfiles:
```
dotmgr -S
```
If you want to specialize only a single file, just add its path to the command line.

To forget about a file, delete it from the repository:
```
dotmgr -D <file>
```

Please refer to the scripts `--help` option for more information on command line options and
arguments.


## Git integration
The program can interact with the repository and automate or at least simplify some pretty
repetitive actions when managing dotfiles:
* `-I` initializes or clones remote repositories as shown in [Initial run](#initial-run).
* `-c` automatically commits changes to dotfiles (using generated or custom commit messages).
* `-s` automatically synchronizes with a remote repository before specialization / after generalization.
* `-V` lets you execute git commands in the dotfile repository without having to `cd` into it first.

Please refer to `--help` for details on the command-line syntax.



# Configuration
## Dotfile specialization / generalization
This is the workflow for generating specific dotfiles for the current hostname and installing them
in the system:
1. Read hostname and the tags activated for it this host from the tag configuration
2. Read dotfiles from the repository
3. Specialize / generalize dotfiles by uncommenting / commenting blocks with matching tags
4. Write them to the home directory

When changed dotfiles are generalized and merged back to the dotfile repository, all changes of the
specialization are reversed by removing all comments from tagged blocks.

## Tagged blocks
Create tagged blocks using a double comment sequence and the directive `only` or `not`. A double
comment sequence followed by `end` ends a tagged block. The following example assumes that the
comment character for the file is `#` - of course the same is possible for other file types as well:
```
##only desktop laptop
# ordinary comment
firefox
##end

##not headless
numlockx
##end
```

You can leave out the `##end` directive on sequential lines / blocks:
```
##only tagA
echo Hello dotmgr
fortune
##not tagB
echo Cheers dotmgr
##end
```

If you have multiple accounts on a host (maybe root and a user account) and you want to customize
your dotfiles based on these, you can use an e-mail / SSH-style syntax in all directives:
```
##only operator@reactor
warnings=ignore
##not guest@reactor
allow_shutdown=yes
##end
```

If you want a particular user to have the same set of files and configuration on all devices, you
can use the syntax `<user>@*` in tag definitions. This is probably most useful with admin accounts
such as `root`. Please see [Skipping files](#skipping-files) below for an example.

## Special `dotmgr` header
During specialization, files can be written to arbitrary locations or skipped completely on hosts
with certain tags by adding a special `dotmgr` header to it.
```
# dotmgr
##use not server
##end

[...]
```

As with tag-blocks, the `end` directive marks the end of the header block. Everything after it is
treated as "normal" file content.

### Skipping files
The `use` directive allows you to skip ignore files during specialization.  
Syntax: `use (only|not) <tag> [<tag> ...]`  
Example:
```
% dotmgr
%%use not root@*
%%

yada yada
[...]
```
Parameters `only` and `not` have the same effect as in tagged-blocks.

### Custom paths
You can store files anywhere on you machine by specifying a custom path using the `path`
directive:  
Syntax: `path <path> <tag> [<tag> ...]`  
Example:
```
# dotmgr
##path /etc/hosts root@server
##end
```
If the `path` directive is present in the header and the host's active tags do not match, the file
is automatically skipped.


## Advanced vim magic
Adding the following line to your .vimrc automagically invokes the script each time you save a
dotfile in your home directory:
```
autocmd BufWritePost ~/.* !dotmgr -G %
```

# Development

## Setup
```
python -m venv venv
. venv/bin/activate
pip install -e '.[dev]'
./test # should succeed
```
