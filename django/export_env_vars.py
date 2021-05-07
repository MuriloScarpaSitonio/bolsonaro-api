from sys import exit

data = []
with open('.env', encoding='UTF-8') as file_:
    for line in file_:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)

        v = v.strip()
        if len(v) >= 2 and ((v[0] == "'" and v[-1] == "'") or (v[0] == '"' and v[-1] == '"')):
            v = v.strip('\'"')
        data.append(f'{k.strip()}={v}')

exit("test", "t", "a")