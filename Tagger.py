from nltk.corpus.reader import TaggedCorpusReader
from nltk.tag import hmm
from nltk.chunk import RegexpParser
from PreProcessing import cleaning
import codecs


def tagging(sent):
    reader = TaggedCorpusReader('.', r'.*\.pos')
    train_data = reader.tagged_sents()[:3000]
    trainer = hmm.HiddenMarkovModelTrainer()
    tagger = trainer.train_supervised(train_data)
    print(sent)
    text = tagger.tag(sent.split())
    print(text)
    return text


def extract_sov(data):
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
                similar = check(so)
                if similar:
                    so_list.append(so) # Problematic in situations like ෙසෙලඉන්ද්‍රයිකා හා ව්‍යුහ   and when not lemmatized
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


pre_processed_text = cleaning()


def call_extract_sov(tagged_text):
    for sent in tagged_text:
        extracted_triples = extract_sov(sent)
        print(extracted_triples)


def call_tagging(pre_processed_text):
    fully_tagged = []
    for sent in pre_processed_text:
        tagged_text = tagging(sent)
        fully_tagged.append(tagged_text)
    return fully_tagged


text_tagged = call_tagging(pre_processed_text)
call_extract_sov(text_tagged)


