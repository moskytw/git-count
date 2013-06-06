#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
DATE_FORMAT  = '%Y/%m/%d'

def count_cmd(author=None, range='', paths=None, period='weekly', number=6, no_all=False, merges=False, **options):
    '''It counts the commits in a Git repository.

        -a, --author=<str>  Specify an author.
        -r, --range=<str>   Specify the range, ex. master..dev.
        -p, --paths=<str>   Specify the paths, ex. .gitignore.
        -p, --period=<str>  Specify the period: weekly (w), monthly (m) or yearly (y). It is weekly, by default.
        -n, --number=<int>  How many periods?
        --not-all           Count the commits in current branch only.
        --merges            Include the merge commits.

    The other arguments will be passed to the command ``git log``.
    '''

    assert period[0] in 'wmy', "option 'period' should be weekly (w), monthly (m) or yearly (y)"

    today = date.today()

    if period.startswith('w'):
        until = today - today.isoweekday()*DAY + WEEK
    elif period.startswith('m'):
        until = date(
            today.year+(today.month+1 > 12),
            today.month+1 % 12,
            1
        ) - DAY
    elif period.startswith('y'):
        until = date(today.year+1, 1, 1) - DAY

    options['author']    = author
    options['all']       = not no_all
    options['no_merges'] = not merges

    while number > 0:

        if period.startswith('w'):
            since = until - WEEK + DAY
        elif period.startswith('m'):
            since = date(until.year, until.month, 1)
        elif period.startswith('y'):
            since = date(until.year, 1, 1)

        options['since'] = since.strftime(DATE_FORMAT)
        options['until'] = until.strftime(DATE_FORMAT)

        print '%s\t%s' % (since, count_git_log(range, paths, options))

        until = since-DAY

        number -= 1

if __name__ == '__main__':

    clime = None

    try:
        import clime
    except ImportError:
        pass

    if clime and clime.__version__ >= '0.2':
        clime.start(white_pattern=clime.CMD_SUFFIX)
    else:

        import sys

        print >> sys.stderr, 'It works better with Clime (>= 0.2). Visit http://clime.mosky.tw/ for more details.'

        if len(sys.argv) <= 1:
            count_cmd()
        else:
            count_cmd(sys.argv[1])
