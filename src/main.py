import sys
import subprocess

def print_help():
    print('Usage: dc-debug [dc-file] <input-file>')

def parse(dc):
    commands = []
    idx, sz = 0, len(dc)
    
    while idx < sz:
        if dc[idx] in 'pnPf?+-*/%~^|vcdrRkioKIOaxqQZXz':
            commands.append(dc[idx])
        elif dc[idx] == '[':
            need = 1
            for i in range(idx + 1, sz):
                if dc[i] == '[':
                    need += 1
                elif dc[i] == ']':
                    need -= 1
                if need == 0:
                    commands.append(dc[idx : i + 1])
                    idx = i
                    break
            else:
                commands.append(dc[idx:])
                idx = sz - 1
        elif dc[idx] in 'slSL<>=:;' or (idx != sz - 1 and dc[idx : idx + 2] in ('!>', '!<', '!=')):
            frm = idx
            if dc[idx] == '!':
                idx += 1
            if idx != sz - 1:
                idx += 1
            commands.append(dc[frm : idx + 1])
        elif dc[idx] in '!#':
            if idx == sz - 1:
                commands.append(dc[idx])
            else:
                for i in range(idx + 1, sz):
                    if dc[i] == '\n':
                        commands.append(dc[idx : i + 1])
                        idx = i
                        break
                else:
                    commands.append(dc[idx:])
                    idx = sz - 1
        elif dc[idx] == '.':
            if idx == sz - 1:
                commands.append(dc[idx])
            else:
                for i in range(idx + 1, sz):
                    if dc[i] not in '0123456789ABCDEF':
                        commands.append(dc[idx : i])
                        idx = i - 1
                        break
                else:
                    commands.append(dc[idx:])
                    idx = sz - 1
        elif dc[idx] in '0123456789ABCDEF_':
            if idx == sz - 1:
                commands.append(dc[idx])
            else:
                dot = False
                for i in range(idx + 1, sz):
                    if dc[i] not in '0123456789ABCDEF' or (dot and dc[i] == '.'):
                        commands.append(dc[idx : i])
                        idx = i - 1
                        break
                    if dc[idx] == '.':
                        dot = True
                else:
                    commands.append(dc[idx:])
                    idx = sz - 1
        idx += 1

    return commands

def print_command(commands, colorize_idx=-1, nl=False):
    if colorize_idx == -1:
        print(''.join(commands), end='\n' if nl else '')
    else:
        print(''.join(commands[:colorize_idx]), end='')
        print('\033[44m' + commands[colorize_idx] + '\033[0m', end='')
        print(''.join(commands[colorize_idx + 1:]), end='\n' if nl else '')

def load_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        print('Error: file "{}" not found'.format(filename))
        exit(1)

def run_dc(command, inp=''):
    ret = subprocess.run('echo "{}" | dc -e "{}"'.format(inp, command), shell=True, stdout=subprocess.PIPE).stdout.decode('utf8').split('\n')
    ret = list(c for c in ret if not c.startswith('dc: '))
    if len(ret) != 0 and ret[-1] == '':
        ret = ret[:-1]
    return ret

def main():
    if len(sys.argv) == 1:
        print_help()
        return

    dc = load_file(sys.argv[1])
    commands = parse(dc)

    inp = ''
    if '?' in commands:
        if len(sys.argv) < 3:
            print('Error: need input file')
            exit(1)
        inp = load_file(sys.argv[2])
    
    print('\033[32m' + 'Running : ' + ''.join(commands) + '\033[0m')
    for i in range(len(commands)):
        print_command(commands, i)
        print('\033[35m | \033[0m', end='')
        com = ''.join(c for c in commands[: i + 1] if c not in 'pnPf')
        res = run_dc(com + 'f', inp)[::-1]
        print(res)
    print('* RIGHT HAND SIDE IS TOP')

if __name__ == '__main__':
    main()
