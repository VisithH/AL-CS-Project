import hashlib

def hashing_given(text):
    digest = hashlib.md5(text.encode('utf-8')).hexdigest()
    return digest

if __name__ == '__main__':
    text = 'Hello world'
    print(hashing_given(text))