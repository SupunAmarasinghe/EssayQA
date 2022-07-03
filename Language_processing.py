from nltk.corpus.reader import TaggedCorpusReader
from nltk.tag import hmm
from nltk.chunk import RegexpParser
import codecs


def tagging(sent):  # method that tag a preprocessed text
    reader = TaggedCorpusReader('.', r'.*\.pos')
    train_data = reader.tagged_sents()[:3000]
    trainer = hmm.HiddenMarkovModelTrainer()
    tagger = trainer.train_supervised(train_data)
    text = tagger.tag(sent.split())
    return text


def extract_sov(data):  # method which extract SOV from the text
    chunker = RegexpParser(r'''
        NP:
        {<JJ>*<NN.*>}
        VP:
        {<JVB>*<NVB>*<V.*>*}
    ''')
    parsed_tree = chunker.parse(data)
    count = 0
    so_list = []
    sub = ''
    ob = ''
    verb = ''
    triple = []

    for subtree in parsed_tree.subtrees(filter=lambda t: t.label() == 'NP'):
        count = count + 1
    if count < 2:
        print('sentence is not correct \n')
    else:
        for subtree in parsed_tree.subtrees(filter=lambda t: t.label() == 'NP'):
            first_so = []
            result = subtree.leaves()
            print(result)
            for word, tag in result:
                first_so.append(word)
                so = ' '.join(first_so)
            #similar = check(so)
            #if similar:
            so_list.append(so)  # Problematic in situations like ෙසෙලඉන්ද්‍රයිකා හා ව්‍යුහ and when not lemmatized
                    #similar = False
            print('SO List:' + str(so_list))
        if len(so_list) != 2:
            print('System has not taken the Subject-Object correctly')
        else:
            sub = so_list[0]
            ob = so_list[1]

    for subtree in parsed_tree.subtrees(filter=lambda t: t.label() == 'VP'):
        correct_verb = []
        result = subtree.leaves()
        for word, tag in result:
            correct_verb.append(word)
            ve = ' '.join(correct_verb)
        print('verb: ' + ve + '\n')
        verb = ve

    if sub and ob:
        triple = [sub, ob, verb]

    return triple


def check(word):  # method that check whether a given subject/object is available in the domain
    with codecs.open("C:/Users/Supun/PycharmProjects/Tagger2/Text_Files/List of Nouns.txt", encoding='utf-8') as f:
        content = f.read()
    sentences = content.split('\r\n')
    found = False
    for line in sentences:
        if word == line:
            found = True
            break
    return found




