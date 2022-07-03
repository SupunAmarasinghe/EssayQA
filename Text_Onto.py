from Evolve_Ontology import create_tuples, clear_onto


def send_data_to_onto(sov):  # method to send SOVs to ontology sentence by sentence
    #clear_onto()
    for element in sov:
        if len(element) != 0:  # If one set of SOV is not empty
            subject_of_sentence = element[0]
            object_of_sentence = element[1]
            verb_of_sentence = element[2]
            create_tuples(subject_of_sentence, object_of_sentence, verb_of_sentence)
