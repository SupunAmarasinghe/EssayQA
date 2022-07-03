from owlready2 import *
import types


from Phrases import subclass_phrase

onto_path.append("C:/Users/Supun/PycharmProjects/Tagger2/Ontology")
onto = get_ontology("file:C:/Users/Supun/PycharmProjects/Tagger2/Ontology/bio-ontology.owl").load()


def clear_onto():
    target = open("C:/Users/Supun/PycharmProjects/Tagger2/Ontology/root-ontology.owl", 'w')
    target.truncate()
    print('abc:', target)


def create_tuples(subj_class, obj_class, predicate):
    print(subj_class, obj_class, predicate)
    with onto:

        NewClass_subject = types.new_class(subj_class, (Thing,))
        NewClass_object = types.new_class(obj_class, (Thing,))
        NewProperty_predicate = types.new_class(predicate, (NewClass_subject >> NewClass_object,))

        if predicate == subclass_phrase[0] or predicate == subclass_phrase[1]:
            NewClass_subject = types.new_class(subj_class, (NewClass_object,))

        for x in NewClass_subject.is_a:
            if isinstance(x, Restriction) and (x.property is NewProperty_predicate) and (x.type == ONLY):
                break
        else:
            NewClass_subject.is_a.append(NewProperty_predicate.only(NewClass_object))

    onto.save()
    #onto.save(file="C:/Users/Supun/PycharmProjects/Tagger2/Ontology/root-ontology.owl", format="rdfxml")





