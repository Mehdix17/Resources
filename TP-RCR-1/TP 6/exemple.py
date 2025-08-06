from owlready2 import *

onto = get_ontology("http://testxyz.org/onto.owl")

with onto:

    # Définition des concepts (classes)
    class Personne(Thing): pass
    class Aliment(Thing): pass
    class University(Thing): pass

    AllDisjoint([Personne, Aliment, University])  # Disjonction stricte

    # Définition des propriétés (rôles)
    class mange(Personne >> Thing): pass
    class enseigne(Personne >> Thing): pass
    class enseigne_par(ObjectProperty): inverse_property = enseigne
    class mange_par(ObjectProperty): inverse_property = mange
    class PartieDe(Thing >> Thing): pass

    # Définition des entités composées
    class Faculty(Thing): equivalent_to = [Thing & PartieDe.some(University)]
    class Departement(Thing): equivalent_to = [Thing & PartieDe.some(Faculty)]
    class Enseignant(Personne): equivalent_to = [Personne & enseigne.only(Personne)]
    class Etudiant(Personne): equivalent_to = [Personne & enseigne_par.only(Enseignant)]

    # Définition d'instances génériques (ABox partielle)
    class Mohamed(Thing): equivalent_to = [Personne & mange.only(Aliment)]
    class Meriem(Personne): equivalent_to = [Enseignant & mange.some(Aliment) & enseigne.only(Etudiant)]
    class MalBouffe(Thing): equivalent_to = [Aliment & mange_par.some(Personne)]

    AllDisjoint([Etudiant, Enseignant])
    AllDisjoint([Meriem, Mohamed])
    AllDisjoint([MalBouffe, Departement, Faculty, University])

    sync_reasoner_pellet(infer_property_values=True)
    onto.save(file="tp_rc1.owl", format="rdfxml")

with onto:
    USTHB = onto.University()
    Sidali = onto.Etudiant()
    Chocolat = onto.Aliment()
    Belhadi = onto.Personne()

    SI = Thing()     # Département
    INFO = Thing()   # Faculté

    INFO.PartieDe.append(USTHB)
    SI.PartieDe.append(INFO)

    Sidali.mange = [Chocolat]
    Belhadi.enseigne = [Sidali]

    sync_reasoner_pellet(infer_property_values=True)
    onto.save(file="tp_rc2.owl", format="rdfxml")



