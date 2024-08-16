# multi-git
Run a Git command on multiple repositories.

## Install
Ubuntu distributions already include `python3-yaml` which is the only dependency so it can be installed locally.

    python3.10 -m pip install .
    
You'll then be able to run `mult-git` from the command line.

## Git Credentials
The simplest option is to setup an ssh key [see here for bitbucket](https://confluence.atlassian.com/bitbucket/set-up-an-ssh-key-728138079.html#SetupanSSHkey-ssh2)
and then use the ssh urls like so `ssh://git@bitbucket.org/<repo_owner>/<reponame>.git`

If you want to use https, you'll have to use the git [credentials storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage) to save credentials, 
which is a bit more painful to setup.

Alternatively, and not recommended, you can store the repos in the .git-repos.yml file by putting them in the url.

## Repo Config file
Will default to looking for `.git-repos.yml` in the current working dir, but you can specify the file using the `-r` option. 
The file needs to look like this;

     repos:
       # a group, repos will be stored in sub dirs of the groups
       group-1:
         # a repo
         repo1:
           # repo url, can be any url git will accept
           url: ssh://git@bitbucket.org/team/repo1.git
       group-2:
         repo2:
           url: ssh://git@bitbucket.org/team/repo2.git
