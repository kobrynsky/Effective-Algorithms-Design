from random import randint


def parse_int(s, base=10, val=False):
    if s.isdigit():
        return int(s, base)
    else:
        return val


def ptype(value):
    print(type(value))


def get_all_ints_from_string(value):
    array = []
    for t in value.split():
        try:
            array.append(int(t))
        except ValueError:
            pass
    return array


INF = 2147483647


def generate_random_number():
    return randint(0, INF)


def copy_array(source, destination):
    for i in range(0, len(source)):
        destination[i] = source[i]