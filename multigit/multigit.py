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
import os
import subprocess
from argparse import ArgumentParser
from typing import Optional, Iterator, Any, List

import yaml


class GitRepo:
    def __init__(self,
                 name: str,
                 group: str,
                 directory: str,
                 url: Optional[str]) -> None:
        self.name = name
        self.group = group
        self.directory = directory
        self.url = url

    def __str__(self) -> str:
        return '{}:{} - {} - {}'.format(self.name, self.group, self.directory, self.url)


def build_args() -> ArgumentParser:
    parser = ArgumentParser(description='Run a Git command on multiple repositories.', add_help=True)

    parser.add_argument('command', type=str, choices=['clone', 'pull'],
                        help='The command to run.')

    # parser.add_argument('-d', type=str, dest='directory',
    #                     help='A directory to start the scan in, all sub directories will be scanned. Overrides -r.')

    parser.add_argument('-r', type=str, dest='repo_file', default='.git-repos.yml',
                        help='A repo yaml file to read repos from.')

    parser.add_argument('-g', type=str, dest='git', default='git',
                        help='The path to your git executable. This can be omitted if it\'s in your path.')

    return parser

# def find_git_repos_from_dir(directory):
#     """
#     Uses generators and recursion to find all git repos in sub dirs.
#     It just looks for the .git sub dir and doesn't support nested
#     git repos (not sure git supports that outside of submodules either).
#     """
#     try:
#         directories = []
#         for entry in os.scandir(directory):
#             if not entry.is_dir():
#                 continue
#             if entry.name == ".git":
#                 yield entry.path[:-4] # trim the .git
#                 # stop processing this dir, no nested repos
#                 return
#             else:
#                 directories.append(entry.path)
#
#         # recursive sub dir search
#         for currdir in directories:
#             yield from find_git_repos(currdir)
#
#         return
#     except FileNotFoundError as e:
#         # this can happen sometime on really deep dir paths
#         print("Error reading file! '%s'" % e)
#         return


def find_git_repos(config_file: str, working_dir: str) -> Iterator[GitRepo]:
    doc = None

    with open(config_file, 'r') as stream:
        try:
            doc = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(-1)

    if 'repos' not in doc:
        print('Invalid config file!')
        exit(-1)

    repos = doc['repos']
    for group_name, group in repos.items():
        for repo_name, repo in group.items():
            yield GitRepo(repo_name, group_name, os.path.join(working_dir, group_name, repo_name), repo['url'])

    return


def run_cmd(git: str, commands: List[str]):
    """
    Run the git command on all repositories in all sub dirs of the sent director
    """
    print('  * Running \'{} {}\'...'.format(git, commands))
    process = subprocess.Popen([git] + commands)
    process.wait()
    print('  * Complete.\n')


def clone_repos(repo: GitRepo, args: Any):
    try:
        if os.path.exists(os.path.join(repo.directory, '.git')):
            print('Skipping clone of \'{}/{}\' as already exists.'.format(repo.group, repo.name))
        else:
            print('Cloning \'{}/{}\':'.format(repo.group, repo.name))
            os.makedirs(repo.directory, exist_ok=True)
            run_cmd(args.git, ['clone', repo.url, repo.directory])
    except Exception as e:
        print('Error processing {}'.format(repo))


def pull_repos(repo: GitRepo, args: Any):
    try:
        if not os.path.exists(os.path.join(repo.directory, '.git')):
            print('Skipping pull of \'{}/{}\' as it\'s not a git repo!.'.format(repo.group, repo.name))
        else:
            print('Pulling  \'{}/{}\':'.format(repo.group, repo.name))
            curr_dur = os.getcwd()
            os.chdir(repo.directory)
            run_cmd(args.git, ['pull'])
            os.chdir(curr_dur)
    except Exception as e:
        print('Error processing {}'.format(repo))


def main():
    args = build_args().parse_args()

    working_dir = os.getcwd()

    commands = {
        'clone': clone_repos,
        'pull': pull_repos
    }

    for repo in find_git_repos(args.repo_file, working_dir):
        commands[args.command](repo, args)


if __name__ == "__main__":
    main()
