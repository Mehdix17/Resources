from owlready2 import *

# Création d'une ontologie
onto = get_ontology("http://smartcity.org/onto.owl")

with onto:
    # Concepts atomiques (classes de base)
    class Ville(Thing): pass
    class VilleIntelligente(Ville): pass
    class CyberVille(VilleIntelligente): pass
    class TIC(Thing): pass
    class Service(Thing): pass
    class Couts(Thing): pass
    class UrbanisationResponsable(Thing): pass
    class TechnologieCapteursSF(Thing): pass
    class ChangementClimatique(Thing): pass
    class RestructurationEco(Thing): pass
    class DeveloppementDurable(Thing): pass
    class MobiliteIntelligente(Thing): pass

    # Rôles (propriétés)
    class utilise(Ville >> TIC): pass
    class améliore(Ville >> Service): pass
    class réduire(Ville >> Couts): pass
    class integre(Ville >> TechnologieCapteursSF): pass
    class developpe(Thing >> VilleIntelligente): pass
    class repond_a(Ville >> Thing): pass  # générique pour les changements
    class doit_developper(Ville >> Thing): pass

    # Définition du concept de VilleIntelligente (TBox a)
    VilleIntelligente.equivalent_to.append(
        Ville
        & utilise.some(TIC)
        & (améliore.some(Service) | réduire.some(Couts))
    )

    # TBox b : VilleIntelligente doit développer des choses
    VilleIntelligente.is_a.append(doit_developper.some(DeveloppementDurable))
    VilleIntelligente.is_a.append(doit_developper.some(MobiliteIntelligente))
    VilleIntelligente.is_a.append(doit_developper.some(UrbanisationResponsable))

    # TBox c : CyberVille est sous-classe de VilleIntelligente (déjà fait via héritage)

    # TBox d : VilleIntelligente répond à des changements
    VilleIntelligente.is_a.append(repond_a.some(ChangementClimatique))
    VilleIntelligente.is_a.append(repond_a.some(RestructurationEco))

    # TBox e : Toute ville intelligente intègre la technologie capteurs SF
    VilleIntelligente.is_a.append(integre.only(TechnologieCapteursSF))

    # TBox f : Une urbanisation responsable ne développe pas de ville intelligente
    UrbanisationResponsable.is_a.append(Not(developpe.some(VilleIntelligente)))

    # ABox g-h
    amsterdam = VilleIntelligente("Amsterdam")

# Raisonnement
sync_reasoner_pellet(infer_property_values=True)

# Sauvegarde de l'ontologie
onto.save(file="smart_city.owl", format="rdfxml")



