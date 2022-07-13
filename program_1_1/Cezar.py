file = open('text_cezar.txt')
text = file.read()


def encrypt_caesar_cipher(not_encrypted_text: str):
    alphabet = {
        'a': 'd',
        'b': 'e',
        'c': 'f',
        'd': 'g',
        'e': 'h',
        'f': 'i',
        'g': 'j',
        'h': 'k',
        'i': 'l',
        'j': 'm',
        'k': 'n',
        'l': 'o',
        'm': 'p',
        'n': 'q',
        'o': 'r',
        'p': 's',
        'q': 't',
        'r': 'u',
        's': 'v',
        't': 'w',
        'u': 'x',
        'v': 'y',
        'w': 'z',
        'x': 'a',
        'y': 'b',
        'z': 'c',
        ' ': ' ',
        '.': '.',
        ',': ',',
        '!': '!',
        '?': '?',
        '\n': '\n'
        }
    encrypt_text = ''
    for i in not_encrypted_text:
        encrypt_text += alphabet[i]
    return encrypt_text


encrypt_text = encrypt_caesar_cipher(text)
print(encrypt_text)


def break_ceaser_cipher(encrypted_text: str):
    alphabet = {
        'a': 'x',
        'b': 'y',
        'c': 'z',
        'd': 'a',
        'e': 'b',
        'f': 'c',
        'g': 'd',
        'h': 'e',
        'i': 'f',
        'j': 'g',
        'k': 'h',
        'l': 'i',
        'm': 'j',
        'n': 'k',
        'o': 'l',
        'p': 'm',
        'q': 'n',
        'r': 'o',
        's': 'p',
        't': 'q',
        'u': 'r',
        'v': 's',
        'w': 't',
        'x': 'u',
        'y': 'v',
        'z': 'w',
        ' ': ' ',
        '.': '.',
        ',': ',',
        '!': '!',
        '?': '?',
        '\n': '\n'
    }
    decrypted_text = ''
    for i in encrypted_text:
        decrypted_text += alphabet[i]
    return decrypted_text


decrypted_text = break_ceaser_cipher(encrypt_text)
print(decrypted_text)

file.close()