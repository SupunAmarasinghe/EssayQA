from AnalysisLevelQA import load_ontology
from ComparisonQA import Comparison
from KnowledgeLevelQA import KnowledgeLevelQA
from Text_Onto import send_data_to_onto
from PreProcessing import cleaning
from Language_processing import extract_sov, tagging

# call for the method which do pre processing
pre_processed_text = cleaning()

sov_from_text = []  # Define a list to store extracted SOVs


def call_tagging(cleaned_text):   # call for the method, which tags the text
    fully_tagged = []
    for sent in cleaned_text:
        tagged_text = tagging(sent)
        fully_tagged.append(tagged_text)
    print(fully_tagged)
    return fully_tagged


def call_extract_sov(tagged_text):  # call for the method which extracts SOV from the text
    for sent in tagged_text:
        extracted_triples_from_text = extract_sov(sent)
        sov_from_text.append(extracted_triples_from_text)
    print(sov_from_text)
    return sov_from_text


def available_classes(sov_list):
    classes = []
    class_list = []
    for element in sov_list:
        if len(element) != 0:  # If one set of SOV is not empty
            classes.append(element[0])
            classes.append(element[1])
    class_set = set(classes)
    class_list.extend(class_set)
    print(class_list)
    return class_list


def call_knowledge_level(classes):
    run_query = KnowledgeLevelQA()
    for element in classes:
        run_query.knowledge_level_questions(element)


def call_comparison_qa(classes):
    run_query = Comparison()
    for element in classes:
        sub_classes = run_query.comparison_question(element)
        if sub_classes:
            answer = run_query.comparison_answer(sub_classes)


text_tagged = call_tagging(pre_processed_text)  # call for a calling methods in this python file
sov = call_extract_sov(text_tagged)  # call for a calling methods in this python file

send_data_to_onto(sov)  # call for the method which connects to ontology learning module

classes_in_text = available_classes(sov)  # call for the method which list only the classes of the text

#call_knowledge_level(classes_in_text)  # call for the calling method of knowledge level module

load_ontology(classes_in_text)  # connect to analysis level module

#call_comparison_qa(classes_in_text)  # call for the calling method of the comparison question module



