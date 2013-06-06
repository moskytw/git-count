#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipes import quote
from subprocess import Popen, PIPE
from datetime import date, timedelta

def shell(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    p.wait()
    return p.stdout.read()[:-1]

def count_git_log(**kargs):
    shell_args = []
    for k, v in kargs.items():
        if isinstance(v, bool) and v:
            shell_args.append('--%s' % k.replace('_', '-'))
        elif v:
            shell_args.append('--%s=%s' % (k.replace('_', '-'), quote(v)))
    return int(shell('git log %s | wc -l' % ' '.join(shell_args)))

DAY = timedelta(days=1)
WEEK = timedelta(weeks=1)
DATE_FORMAT  = '%Y/%m/%d'

def count_cmd(author=None, period='weekly', number=6, no_all=False, merges=False, **kargs):

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

    while number:

        if period.startswith('w'):
            since = until - WEEK + DAY
        elif period.startswith('m'):
            since = date(until.year, until.month, 1)
        elif period.startswith('y'):
            since = date(until.year, 1, 1)

        print '%s\t%s' % (since, count_git_log(
            oneline   = True,
            author    = author,
            all       = not no_all,
            no_merges = not merges,
            since     = since.strftime(DATE_FORMAT),
            until     = until.strftime(DATE_FORMAT),
            **kargs
        ))

        until = since-DAY

        number -= 1

if __name__ == '__main__':
    import clime
    #clime.start(white_pattern=clime.CMD_SUFFIX, debug=True)
    clime.start(white_pattern=clime.CMD_SUFFIX)
