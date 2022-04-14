import os


if __name__ == '__main__':
    fns = set()
    for root, dirs, files in os.walk('_build/html/api'):
        for name in files:
            fns.add(os.path.join(root, name))
    for fn in fns:
        with open(fn, 'r') as f:
            content = f.read()
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if '\u00a0' in line:
                print(fn, i, line)
        content = content.replace('\u00a0', ' ')
        with open(fn, 'w') as f:
            f.write(content)
