# GitSubDirCmd
Run a Git command on multiple repositories.

## Usage
GitSubDirCmd -d \<Directory\> -c "\<git command\>"
 
	-d, --directory A directory to start the scan, all sub directories will be scanned.
	-c, --command   The git command to execute on each repository found.
	-g, --git       The path to you git executable. This can be omitted if it's in your path.
	-h, --help      Show this usage message.

e.g:

	GitSubDirCmd -d "/usr/repositories" -c "pull"

Will run 'git pull' on all repositories in '/usr/repositories', it will recursively scan
all subdirectories.
