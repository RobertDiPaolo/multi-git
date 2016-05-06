# The MIT License (MIT)
#
# Copyright (c) 2016 Robert Di Paolo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import getopt
import os
import subprocess
import textwrap
import sys


def print_usage():
    """
    Prints the command line usage instructions.
    """
    print(textwrap.dedent(
        u"""
        ---
        GitSubDirCmd Usage
        ---

        GitSubDirCmd -d <Directory> -c "<git command>"

        -d, --directory\t\tA directory to start the scan, all sub directories will be scanned.
        -c, --command\t\tThe git command to execute on each repository found.
        -g, --git\t\tThe path to you git executable. This can be omitted if it's in your path.
        -h, --help\t\t\tShow this usage message.

        e.g:
        GitSubDirCmd -d "/usr/repositories" -c "pull"

        Will run 'git pull' on all repositories in '/usr/repositories', it will recursively scan
        all subdirectories.
        """))


def parse_command_line():
    """
    This method parses the command line and returns a dictionary of all the options.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:c:g:h", ["directory", "command", "git", "help"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(-1)

    if opts is None:
        print_usage()
        sys.exit(-1)

    show_help = False
    directory = None
    command = None
    git = "git"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help = True
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-d", "directory"):
            directory = arg
        elif opt in ("-g", "git"):
            git = arg

    if show_help:
        print_usage()
        sys.exit()

    if directory is None or command is None:
        print_usage()
        sys.exit(-1)

    if not os.path.isdir(directory):
        print("'%s' is not a valid directory!" % directory)
        sys.exit(-2)

    retval = {"directory": directory, "command": command, "git": git}
    return retval


def find_git_repos(directory):
    """
    Uses generators and recursion to find all git repos in sub dirs.
    It just looks for the .git sub dir and doesn't support nested
    git repos (not sure git supports that outside of submodules either).
    """
    try:
        directories = []
        for entry in os.scandir(directory):
            if not entry.is_dir():
                continue
            if entry.name == ".git":
                yield entry.path[:-4] # trim the .git
                # stop processing this dir, no nested repos
                return
            else:
                directories.append(entry.path)

        # recursive sub dir search
        for currdir in directories:
            yield from find_git_repos(currdir)

        return
    except FileNotFoundError as e:
        # this can happen sometime on really deep dir paths
        print("Error reading file! '%s'" % e)
        return


def run_cmd(git, command, directory):
    """
    Run the git command on all repositories in all sub dirs of the sent director
    """
    for repo in find_git_repos(directory):
        print("Running '%s %s' on '%s..." % (git, command, repo))
        process = subprocess.Popen([git, command], cwd=repo)
        process.wait()
        print("Complete.\n")


if __name__ == "__main__":
    params = parse_command_line()
    run_cmd(params["git"], params["command"], params["directory"])
