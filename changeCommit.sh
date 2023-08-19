  # changeCommit.sh
  git filter-branch --commit-filter '
    if [ "$GIT_AUTHOR_EMAIL" = "ranxi@163.com" ];
    then
            GIT_AUTHOR_NAME="ranxi2001";
            GIT_AUTHOR_EMAIL="ranxi169@163.com";
            git commit-tree "$@";
    else
            git commit-tree "$@";
    fi' HEAD
