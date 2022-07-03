from owlready2 import *
from Phrases import analysis_level_question_phrase, adjoining_phrases

set_of_questions = []


def load_ontology(class_list):
    my_world = World()
    my_world.get_ontology("file://C:\\Users\\Supun\\PycharmProjects\\Tagger2\\Ontology\\bio-ontology.owl").load()  # path to the owl file is given here
    graph = my_world.as_rdflib_graph()
    get_class_pairs(graph, class_list)


def get_class_pairs(onto_graph, class_list):
    length = len(class_list)
    for i in range(length):
        start = ''.join(class_list[i])
        for j in range(i + 1, length):
            end = ''.join(class_list[j])
            analysis_level_answer(onto_graph, start, end)


def analysis_level_answer(onto_graph, start, end):
    answer_query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    select ?domain ?property ?range (count(?mid) as ?dist)
                    where {
                    ?property rdfs:domain ?domain;
                        rdfs:range ?range.
                    ?start (^rdfs:domain/rdfs:range)* ?domain .
                    ?range (^rdfs:domain/rdfs:range)* ?end .
                    ?start (^rdfs:domain/rdfs:range)* ?mid .
                    ?mid (^rdfs:domain/rdfs:range)* ?domain .
                    FILTER (regex(str(?start), '""" + start + """'))
                    FILTER (regex(str(?end), '""" + end + """'))
                    }
                    group by ?domain ?property ?range
                    order by ?dist
                    """

    results_list = onto_graph.query(answer_query)  # query result will be stored in a variable
    selected_results = []
    count = 0
    for item in results_list:
        predicate = str(item['property'].toPython())
        predicate = re.sub(r'.*#', "", predicate)

        domain = str(item['domain'].toPython())
        domain = re.sub(r'.*#', "", domain)

        range_class = str(item['range'].toPython())
        range_class = re.sub(r'.*#', "", range_class)

        selected_results.append(
            {'subject': domain, 'object': range_class, 'predicate': predicate})  # create a dictionary
        count = count + 1
    if count >= 1:
        question = start + adjoining_phrases[0] + end + analysis_level_question_phrase[0]
        set_of_questions.append(question)
        print('q: ' + question)

    for element in selected_results:
        answer = element['subject'] + ' ' + element['object'] + ' ' + element['predicate']
        print(answer)






