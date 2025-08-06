def get_label(reseau_semantique, node, relation):
    node_relation_edges = [edge["from"] for edge in reseau_semantique["edges"] if (edge["to"] == node["id"] and edge["label"] == relation)]
    node_relation_edges_label = [node["label"] for node in reseau_semantique["nodes"] if node["id"] in node_relation_edges]
    if node_relation_edges_label:
        reponse = "il y a un lien entre les 2 noeuds : " + ", ".join(node_relation_edges_label)
    else:
        reponse = "il n'y a pas de lien entre les 2 noeuds"
    return reponse

def propagation_de_marqueurs(reseau_semantique, requetes):
    nodes = reseau_semantique["nodes"]
    edges = reseau_semantique["edges"]
    solutions_found = []

    for req in requetes:
        node1, node2, relation = req
        solution_found = False

        try:
            M1 = [node for node in nodes if node["label"] == node1][0]
            M2 = [node for node in nodes if node["label"] == node2][0]

            # Vérification directe de la relation recherchée (hors exception)
            direct_relation = any(
                edge for edge in edges
                if edge["from"] == M1["id"] and edge["to"] == M2["id"] and edge["label"] == relation and edge.get("edge_type") != "exception"
            )
            if direct_relation:
                solution_found = True
            else:
                propagation_edges = [
                    edge for edge in edges
                    if (edge["to"] == M1["id"] and edge["label"] == "is a" and edge.get("edge_type") != "exception")
                ]
                while propagation_edges and not solution_found:
                    temp_edge = propagation_edges.pop()
                    temp_node_contient_edges = [
                        edge for edge in edges
                        if (edge["from"] == temp_edge["from"] and edge["label"] == relation and edge.get("edge_type") != "exception")
                    ]
                    solution_found = any(d['to'] == M2["id"] for d in temp_node_contient_edges)
                    if not solution_found:
                        temp_node_is_a_edges = [
                            edge for edge in edges
                            if (edge["to"] == temp_edge["from"] and edge["label"] == "is a" and edge.get("edge_type") != "exception")
                        ]
                        propagation_edges.extend(temp_node_is_a_edges)

            solutions_found.append(get_label(reseau_semantique, M2, relation) if solution_found else "il n'y a pas de lien entre les 2 noeuds")
        except IndexError:
            solutions_found.append("Aucune reponse n'est fournie par manque de connaissances.")

    return solutions_found

