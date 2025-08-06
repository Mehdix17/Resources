from algorithms import propagation, heritage, exceptions
import json

MENU = """                  
                             _______________________________________________________________________
                            |                                                                       |
                            |                                Menu                                   |
                            | ______________________________________________________________________|
                            |                                                                       |
                            | 1) Partie 1 : L’algorithme de propagation de marqueurs                |
                            |                                                                       |
                            | 2) Partie 2 : L’algorithme d’héritage                                 |
                            |                                                                       |
                            | 3) Partie 3 : L’algorithme de propagation de marqueurs avec exception |
                            |                                                                       |
                            | 4) Quitter                                                            |
                            |_______________________________________________________________________|"""

# Load JSON files
propagation_json = open('Bases/propagation.json')
heritage_json = open('Bases/heritage.json')
exception_json = open('Bases/exception.json')

# Load the JSON data into Python dictionaries
reseau_semantique_propagation = json.load(propagation_json)
reseau_semantique_heritage = json.load(heritage_json)
reseau_semantique_exception = json.load(exception_json)

while True:

    print(MENU)
    choix = input("\nEntrer le numero de la partie : ")

    if choix == "1":
        print("\n*********************************** Partie 1 : L'algorithme de propagation de marqueurs ***********************************")
        requetes = [
            ["Modes Logiques", "Modes de Representations des connaissances", "is a"],
            ["Logique d'ordre 1", "Logiques Classiques", "is a"],
            ["Reseaux Semantique", "Modes Graphiques", "is a"],
            ["Modes de Representations des connaissances", "Axiome A9", "is a"]
        ]
        solutions = propagation.propagation_de_marqueurs(reseau_semantique_propagation, requetes)
        
        for i, req in enumerate(requetes):
            print(f"\n{req[0]} {req[2]} {req[1]} --> {solutions[i]}")

    elif choix == "2":
        print("\n*********************************** Partie 2 : L'algorithme d'heritage ***********************************")
        
        nodes = [node["label"] for node in reseau_semantique_heritage["nodes"]]
        print("\nNoeuds disponibles : " + ", ".join(nodes))

        while True:
            starting_node = input("\nEntrer le nom du noeud de départ : ")

            if starting_node not in nodes:
                print("\n❌ Noeud non valide")
            else:
                break

        nodes, properties = heritage.heritage(reseau_semantique_heritage, starting_node)
        
        print(f"\nInférence à partir de '{starting_node}' : \n")
        for l in nodes:
            print("- " + l, end="\n\n")
        
        print("Propriétés déduites : \n")
        if not properties: 
            print("aucune")
        for p in properties:
            print("- " + p, end="\n\n")

    elif choix == "3":
        print("\n*********************************** Partie 3 : L'algorithme de propagation de marqueurs avec exception ***********************************")
        requetes = [
            ["Logique d'ordre 1", "Logiques Classiques", "is a"],
            ["Modes de Representations des connaissances", "Axiome A7", "contient"],
            ["Reseaux Semantique", "Modes Graphiques", "is a"],
            ["Modes de Representations des connaissances", "Axiome A9", "is a"]
        ]
        solutions = exceptions.propagation_de_marqueurs(reseau_semantique_exception, requetes)
        for i, req in enumerate(requetes):
            print(f"\n{req[0]} {req[2]} {req[1]} --> {solutions[i]}")

    elif choix == "4":
        print("\nFin du programme.")
        break

    else:
        print("\n❌ Choix invalide")
