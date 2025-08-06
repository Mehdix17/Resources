import subprocess
import tempfile
import os

def read_file(fichier):
    """
    Lit un fichier DIMACS CNF.
    Retourne : liste des clauses, nombre de variables
    """
    clauses = []
    nb_vars = 0

    try:
        with open(fichier, "r") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne.startswith("c") or ligne == "":
                    continue  # ignorer les commentaires
                elif ligne.startswith("p"):
                    # ex: p cnf 200 860
                    _, _, nb_vars_str, _ = ligne.split()
                    nb_vars = int(nb_vars_str)
                else:
                    # ligne de clause
                    clause = list(map(int, ligne.split()[:-1]))  # enlever le 0 final
                    clauses.append(clause)
        return clauses, nb_vars
                
    except FileNotFoundError:
        print(f"\n❌ Erreur : le fichier '{fichier}'' n'existe pas.")
        return [], 0

def create_temp_file(clauses, nb_vars):
    """
    Crée un fichier temporaire .cnf en DIMACS avec les clauses données.
    """
    content = f"p cnf {nb_vars} {len(clauses)}\n"
    for clause in clauses:
        content += " ".join(map(str, clause)) + " 0\n"

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".cnf", mode="w")
    temp.write(content)
    temp.close()
    return temp.name

def check_inference(file, literal, ubcsat_path="./ubcsat"):
    """
    Vérifie si le fichier CNF d'origine + clauses supplémentaires est insatisfiable.
    """
    bc_clauses, nb_vars = read_file(file)

    if bc_clauses: # Vérifier si le fichier a été lu correctement

        # Ajouter l'inverse du literal φ
        all_clauses = bc_clauses + [[-1*literal]]

        # Ajuster le nombre de variables si nécessaire
        max_var_utilisee = max(abs(lit) for clause in all_clauses for lit in clause)
        nb_vars = max(nb_vars, max_var_utilisee)

        # Écrire dans un fichier temporaire
        cnf_temp = create_temp_file(all_clauses, nb_vars)

        try:
            result = subprocess.run(
                [ubcsat_path, "-alg", "saps", "-i", cnf_temp, "-solve"],
                capture_output=True, text=True
            )

            output = result.stdout
            x = "{{{}}}".format(-1*literal)
            if "Solution Found" not in output:
                print(f"\n✅ BC U {x} est insatisfiable, donc BC infère bien {literal} (BC ⊨ {literal})")
                return True
            else:
                print(f"\n❌ BC U {x} est satisfiable, donc BC n'infère pas {literal} (BC ⊭ {literal})")
                return False

        finally: # Nettoyer le fichier temporaire
            os.remove(cnf_temp)

# Exemple d'utilisation

while True:
    try:
        fichier = input("\nEntrer le fichier CNF : ")
        phi = int(input("\nEntrer un literal φ (ex: 3 pour c, -3 pour ¬c) : "))
        check_inference(fichier, phi)
    except ValueError:
        print("\n❌ Erreur : le literal φ doit être un entier.")
