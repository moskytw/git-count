Git Count
---------

It provides a command, ``git-count``, that can count commits in a Git repository
in days, weeks, months or years.

Installations
-------------

It is uploaded to PyPI, thus you can install it by this command:

::

    # pip install git-count

Or install it from the source code:

::

    # python setup.py install

Usage
-----

::

    DESKTOP ~/mosql (dev) $ git-count --help
    usage: [-a | --author=<str>] [-p | --period=<str>] [-f | --first=<str>] [-n | --number=<int>] [-r | --range=<str>] [-t | --paths=<str>] [--no-all] [--merges] [--<key>=<value>...]
       or: count [-a | --author=<str>] [-p | --period=<str>] [-f | --first=<str>] [-n | --number=<int>] [-r | --range=<str>] [-t | --paths=<str>] [--no-all] [--merges] [--<key>=<value>...]

    It counts the commits in a Git repository.

        -a, --author=<str>  Specify an author.
        -p, --period=<str>  Specify the period: daily (d), weekly (w), monthly
                            (m) or yearly (y). It is weekly, by default.
        -f, --first=<str>   Specify the first day of weeks: monday (mon), sunday
                            (sun), saturday (sat). It is monday, by default.
        -n, --number=<int>  How many periods?
        -r, --range=<str>   Specify the range, ex. master..dev.
        -t, --paths=<str>   Specify the paths, ex. .gitignore.
        --not-all           Count the commits in current branch only.
        --merges            Include the merge commits.

    The other arguments will be passed to the command, ``git log``.

Examples
--------

::

    DESKTOP ~/mosql (dev) $ git-count mosky
    2013-06-03  20
    2013-05-27  108
    2013-05-20  117
    2013-05-13  0
    2013-05-06  3
    2013-04-29  0
    2013-04-22  37
    2013-04-15  83

::

    DESKTOP ~/mosql (dev) $ git-count mosky -pm -n3
    2013-06-01  23
    2013-05-01  225
    2013-04-01  153

::

    DESKTOP ~/mosql (dev) $ git-count mosky -r v0.5..dev -pd -n5
    2013-06-06  0
    2013-06-05  5
    2013-06-04  11
    2013-06-03  4
    2013-06-02  0





