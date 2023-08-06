def _hist_format(args):
    import argparse, os

    argp = argparse.ArgumentParser(prog='hist-format', description="Format xonsh history to post it to Github or another page.")
    argp.add_argument('-f', '--format', default='md', help="Format: md, txt.")
    argp.add_argument('-c', '--count', default=10, help="Count of commands")
    argp.add_argument('-l', '--lines', action='store_true', help="Add additional lines before and after.")
    opt = argp.parse_args(args)

    opt.count = int(opt.count)

    formats = {
        'md': {'begin': '```python', 'end': '```', 'comment': '#'},
        'txt': {'begin': '', 'end': '', 'comment': '#'}
    }
    format = formats[opt.format]

    if opt.lines:
        try:
            ts = os.get_terminal_size()
            term_cols = ts.columns
        except Exception:
            term_cols = 10

    cmds = []
    cmds_idx = []
    for i in list(range(len(__xonsh__.history) - 1, -1, -1)):
        h = __xonsh__.history[i]
        if 'hist-format' in h.cmd or 'hist-md' in h.cmd:
            continue
        if len(cmds_idx) >= opt.count or h.cmd.rstrip() == 'clear':
            break
        cmds_idx.append(i)

    if opt.lines:
        print()
        print('-' * term_cols)

    if opt.format == 'md':
        print('\n<sub>[hist-format](https://github.com/anki-code/xontrib-hist-format) output:</sub>\n')
    else:
        print('\nOutput:\n')

    print(format['begin'])
    for i in cmds_idx[::-1]:
        h = __xonsh__.history[i]
        print(h.cmd.rstrip(), end='')
        if h.out:
            print()
            print('\n'.join([format['comment'] + l for l in str(h.out).rstrip().split('\n')]))
        print()
        cmds.append(h.cmd.rstrip())
    print(format['end'])

    if opt.format == 'md':
        print('\n<sub>[hist-format](https://github.com/anki-code/xontrib-hist-format) commands:</sub>\n')
    else:
        print('\nCommands:\n')

    print(format['begin'])
    for c in cmds:
        print(c)
    print(format['end'])

    if opt.lines:
        print()
        print('-' * term_cols)


aliases['hist-format'] = _hist_format
aliases['hist-md'] = ['hist-format', '-f', 'md']
aliases['hist-txt'] = ['hist-format', '-f', 'txt']
del _hist_format
