target = 'streamlabs.com'


endpoints = f'{target}/{target}_endpoints.txt'

chars = ['#','?','&']

with open(endpoints, 'r') as f:
    file = f'{target}_params.html'
    path = f'{target}/{file}'
    Lines = [line for line in f.readlines() if line.strip()]
    for line in Lines:
        for char in chars:
            if char in line:
                line = f'<a href="{line}">{line}</a><br \>'
                with open(path, 'a') as newf:
                    newf.write(line)
                    newf.close()
