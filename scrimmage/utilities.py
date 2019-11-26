
#IP = '134.129.91.220'
#IP = '134.129.91.211'
IP = '127.0.0.1'
PORT = 5007
BUFFER_SIZE = 4096

REGISTER_COMMANDS = ['register', '-r']
SUBMIT_COMMANDS = ['submit', '-s']
VIEW_STATS_COMMANDS = ['view stats', 'view', '-v']


def file_to_binary(filename):
    res = None
    with open(filename, 'rb') as f:
        res = f.read()

    return res


def binary_to_file(filename, ba):
    with open(filename, 'wb') as f:
        for b in ba:
            f.write(b)
