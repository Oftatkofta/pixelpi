import string


def create_encoder(filename):
    """
    Generates a dict from a file with structure "subst letter\n"

    :param filename: name of file containing substitution cypher
    :return:
        dict that can be used in a Caesar/substitution cypher
    """

    out = {}

    with open(filename, "r") as f:
        linelist = f.readlines()

    for s in linelist:
        parts = s.split(" ")
        letter = parts[1][:-1] #gets rid of newline at end
        code = parts[0]

        # Workaround for space character
        if len(parts) == 3:
            letter = " "

        out[letter] = code

    return out

def encode_string(string, dict):
    """
    Uses the code in dict to encode each letter of the input string

    :param string: string to encode
    :param dict: letter:code
    :return: encoded string
    """
    out = ''
    for l in string:
        out += dict.get(l, '?') #unknown characters are replaced with '?'

    return out


if __name__ == "__main__":
    code = create_encoder("JCVI_code.txt")

    for key in code.keys():
        print(key, code[key])

    s = "TOOL IS SANTAS FAVOURITE BAND!"
    enc = encode_string(s, code)
    print(s)
    print(enc)