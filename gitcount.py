#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'

from pipes import quote
from subprocess import Popen, PIPE
from datetime import date, timedelta

def shell(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    p.wait()
    return p.stdout.read()[:-1]

def count_git_log(range='', paths=None, options=None):

    if options is None:
        options = {}

    options['oneline'] = True

    shell_args = []

    for k, v in options.items():
        if isinstance(v, bool) and v:
            shell_args.append('--%s' % k.replace('_', '-'))
        elif v:
            shell_args.append('--%s=%s' % (k.replace('_', '-'), quote(v)))

    if paths:
        shell_args.append('-- %s' % paths)

    return int(shell('git log %s %s | wc -l' % (range, ' '.join(shell_args))))

DAY = timedelta(days=1)
WEEK = timedelta(weeks=1)
DATE_FORMAT  = '%Y-%m-%d 00:00:00'

def count(author=None, period='weekly', first='monday', number=None, range='', paths=None, no_all=False, merges=False, **options):
    '''It counts the commits in a Git repository.

        -a, --author=<str>  Specify an author.
        -p, --period=<str>  Specify the period: daily (d), weekly (w), monthly
                            (m) or yearly (y). It is weekly, by default.
        -f, --first=<str>   Specify the first day of weeks: monday (mon), sunday (sun), saturday (sat). It is monday, by default.
        -n, --number=<int>  How many periods?
        -r, --range=<str>   Specify the range, ex. master..dev.
        -t, --paths=<str>   Specify the paths, ex. .gitignore.
        --not-all           Count the commits in current branch only.
        --merges            Include the merge commits.

    The other arguments will be passed to the command, ``git log``.
    '''

    assert period[0] in 'dwmy', "option 'period' should be daily (d), weekly (w), monthly (m) or yearly (y)"

    today = date.today()

    if period.startswith('d'):
        until = today
        if not number: number = 14
    elif period.startswith('w'):
        until = today - today.weekday()*DAY + WEEK
        if first[:3] == 'sun':
            until -= DAY
        elif first[:3] == 'sat':
            until -= 2*DAY
        if not number: number = 8
    elif period.startswith('m'):
        until = date(
            today.year+(today.month+1 > 12),
            today.month+1 % 12,
            1
        )
        if not number: number = 12
    elif period.startswith('y'):
        until = date(today.year+1, 1, 1)
        if not number: number = 5

    options['author']    = author
    options['all']       = not no_all
    options['no_merges'] = not merges

    while number > 0:

        if period.startswith('d'):
            since = until - DAY
        elif period.startswith('w'):
            since = until - WEEK
        elif period.startswith('m'):
            since = date(
                until.year-(until.month-1 <= 0),
                1 + ((12+(until.month-1)-1) % 12),
                1
            )
        elif period.startswith('y'):
            since = date(until.year-1, 1, 1)

        options['since'] = since.strftime(DATE_FORMAT)
        options['until'] = until.strftime(DATE_FORMAT)

        print '%s\t%s' % (since, count_git_log(range, paths, options))

        until = since

        number -= 1

def main():

    clime = None

    try:
        import clime
    except ImportError:
        pass

    if not clime or clime.__version__ < '0.1.5':
        print >> sys.stderr, 'It works better with Clime (>= 0.1.5). Visit http://clime.mosky.tw/ for more details.'

    if clime:
        if clime.__version__ < '0.2.3':
            try:
                from inspect import cleandoc
            except ImportError:
                clime.Program({'count': count}, doc=count.__doc__).main()
            else:
                clime.Program({'count': count}, doc=cleandoc(count.__doc__)).main()
        else:
            clime.start({'count': count})
    else:

        import sys

        if len(sys.argv) <= 1:
            count()
        else:
            count(sys.argv[1])

if __name__ == '__main__':
    main()
