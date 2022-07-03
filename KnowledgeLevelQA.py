from owlready2 import *
from Phrases import knowledge_level_question_phrase


class KnowledgeLevelQA:
    def __init__(self):
        my_world = World()
        my_world.get_ontology("file://C:\\Users\\Supun\\PycharmProjects\\Tagger2\\Ontology\\bio-ontology.owl").load()  # path to the owl file is given here
        # sync_reasoner(my_world)  #reasoner is started and synchronized here, reasoner name: HermiT
        self.graph = my_world.as_rdflib_graph()

    def knowledge_level_questions(self, class_from_text):
        count = 0
        answer_query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                SELECT ?domain ?range ?property 
                                WHERE{
                                ?property rdfs:domain ?domain;
                                    rdfs:range ?range.
                                FILTER (regex(str(?domain), '""" + class_from_text + """'))
                                }"""

        results_list = self.graph.query(answer_query)  # query result will be stored in a variable
        selected_results = []
        for item in results_list:
            predicate = str(item['property'].toPython())
            predicate = re.sub(r'.*#', "", predicate)

            domain = str(item['domain'].toPython())
            domain = re.sub(r'.*#', "", domain)

            range_class = str(item['range'].toPython())
            range_class = re.sub(r'.*#', "", range_class)

            selected_results.append(
                {'subject': domain, 'object': range_class, 'predicate': predicate})  # create a dictionary

            for element in selected_results:
                if element['subject'] == class_from_text:
                    count = count+1
        if count >= 1:
            question = class_from_text + ' ' + knowledge_level_question_phrase[0]
            print(question)
            self.knowledge_level_answers(class_from_text)

    def knowledge_level_answers(self, class_from_text):
        answer_query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
                                SELECT ?domain ?range ?property 
                                WHERE{
                                ?property rdfs:domain ?domain;
                                    rdfs:range ?range.
                                FILTER (regex(str(?domain), '""" + class_from_text + """'))
                                }"""

        results_list = self.graph.query(answer_query)  # query result will be stored in a variable
        selected_results = []
        answer = ''
        for item in results_list:
            predicate = str(item['property'].toPython())
            predicate = re.sub(r'.*#', "", predicate)

            domain = str(item['domain'].toPython())
            domain = re.sub(r'.*#', "", domain)

            range_class = str(item['range'].toPython())
            range_class = re.sub(r'.*#', "", range_class)

            selected_results.append(
                {'subject': domain, 'object': range_class, 'predicate': predicate})  # create a dictionary

            for element in selected_results:
                if element['subject'] == class_from_text:
                    answer = element['subject'] + ' ' + element['object'] + ' ' + element['predicate']
            print(answer)
