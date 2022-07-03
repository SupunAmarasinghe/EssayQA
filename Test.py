import codecs


def extract_verb(chunk, tag_affixes=['VFM', 'VNF', 'VP', 'VNN', 'JVB', 'NVB']): #chunk is tagged text
    verb_sentence = []
    for word, tag in chunk:
        for element in tag_affixes:
            if element in tag:
                verb_sentence.append((word, tag))
    return verb_sentence


def check(word):
    with codecs.open("List of Nouns.txt", encoding='utf-8') as f:
        content = f.read()
    sentences = content.split('\r\n')
    found = False
    for line in sentences:
        if word == line:
            found = True
            break
    return found


print(check('ෙසෙල'))