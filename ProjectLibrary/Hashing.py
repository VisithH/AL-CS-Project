import hashlib

def hashingGiven(text):
    digest = hashlib.md5(text.encode('utf-8')).hexdigest()
    return digest

if __name__ == '__main__':
    text = 'Hello world'
    print(hashingGiven(text))
