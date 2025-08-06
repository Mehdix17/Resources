import networkx as nx
from sympy import symbols, Not, Or, Implies, Equivalent

# --- Kripke Model Core Logic ---
# These functions are general and will be used across all scenarios.

# Define modal functions
def box(formula, world, graph):
    """
    Evaluates □formule (opérateur de nécessité) dans le monde 'world' donné
    basé sur le 'graph' fourni (cadre de Kripke).
    □formule est vraie dans 'world' si 'formule' est vraie dans tous les mondes accessibles depuis 'world'.
    """
    # Get all worlds accessible from the current 'world'
    accessible_worlds = list(graph.successors(world))
    
    # If there are no accessible worlds, □formula is vacuously true.
    if not accessible_worlds:
        return True
    
    # Check if the formula holds for all successors of the current world
    return all(formula(w_prime) for w_prime in accessible_worlds)

def dia(formula, world, graph):
    """
    Evaluates ◇formule (opérateur de possibilité) dans le monde 'world' donné
    basé sur le 'graph' fourni (cadre de Kripke).
    ◇formule est vraie dans 'world' si 'formule' est vraie dans au moins un monde accessible depuis 'world'.
    """
    # Get all worlds accessible from the current 'world'
    accessible_worlds = list(graph.successors(world))

    # If there are no accessible worlds, ◇formula is vacuously false.
    if not accessible_worlds:
        return False

    # Check if the formula holds for any successor of the current world
    return any(formula(w_prime) for w_prime in accessible_worlds)

# --- Scenario 1: Epistemic Logic (Knowledge) ---
def scenario_knowledge():
    """
    Demonstrates epistemic logic, focusing on what an agent (Alice) knows.
    """
    print("\n--- Scénario : Logique Épistémique (Connaissance) ---")
    print("Contexte : Alice essaie de savoir s'il pleut ou s'il fait beau.")
    print("Les mondes représentent différents états de la météo et la perception d'Alice.")

    # Worlds:
    # rs: Raining, Alice thinks it's sunny
    # rr: Raining, Alice thinks it's raining
    # ss: Sunny, Alice thinks it's sunny
    # sr: Sunny, Alice thinks it's raining
    W_k = ["rs", "rr", "ss", "sr"]

    # Accessibility Relation (R_A for Alice's knowledge):
    # Alice considers world w' accessible from w if w' is consistent with what Alice knows in w.
    # Here, Alice cannot distinguish between 'rs' and 'ss' (she thinks it's sunny)
    # and cannot distinguish between 'rr' and 'sr' (she thinks it's raining).
    R_k = [("rs", "rs"), ("rs", "ss"),  # S'il pleut mais qu'Alice pense qu'il fait beau, elle ne peut pas distinguer
           ("rr", "rr"), ("rr", "sr"),  # S'il pleut et qu'Alice pense qu'il pleut, elle ne peut pas distinguer
           ("ss", "rs"), ("ss", "ss"),  # S'il fait beau et qu'Alice pense qu'il fait beau, elle ne peut pas distinguer
           ("sr", "rr"), ("sr", "sr")]  # S'il fait beau mais qu'Alice pense qu'il pleut, elle ne peut pas distinguer

    # Valuation:
    # 'R' is true if it's raining in that world
    # 'S' is true if it's sunny in that world
    V_k = {
        "R": {"rs", "rr"},
        "S": {"ss", "sr"}
    }

    # Create Kripke frame for this scenario
    G_k = nx.DiGraph()
    G_k.add_nodes_from(W_k)
    G_k.add_edges_from(R_k)

    # Propositional variables for this scenario
    R_prop, S_prop = symbols('R S')

    def valuation_k(world):
        """Returns valuation for knowledge scenario."""
        return {
            R_prop: world in V_k['R'],
            S_prop: world in V_k['S']
        }

    # Epistemic operator: K_A (Alice knows) is represented by Box
    # K_A(phi) means "Alice knows that phi"
    K_A = lambda formula, world: box(formula, world, G_k)

    # Belief operator: P_A (Alice believes) is represented by Dia
    # P_A(phi) means "Alice believes that phi"
    P_A = lambda formula, world: dia(formula, world, G_k)

    # Formulas to evaluate
    # 1. K_A(R_prop): Alice knows it's raining.
    # 2. K_A(S_prop): Alice knows it's sunny.
    # 3. K_A(R_prop) OR K_A(S_prop): Alice knows whether it's raining or sunny.
    # 4. R_prop IMPLIES K_A(R_prop): If it's raining, Alice knows it's raining. (Factivity)
    # 5. P_A(R_prop) IMPLIES K_A(R_prop): If Alice believes it's raining, she knows it's raining.

    print("\nFormules à évaluer :")
    print("1. K_A(R) : Alice sait qu'il pleut.")
    print("2. K_A(S) : Alice sait qu'il fait beau.")
    print("3. K_A(R) ∨ K_A(S) : Alice sait s'il pleut ou s'il fait beau.")
    print("4. R → K_A(R) : S'il pleut, Alice sait qu'il pleut (Factivité).")
    print("5. P_A(R) → K_A(R) : Si Alice croit qu'il pleut, elle sait qu'il pleut.")

    while True:
        world_choice = input(f"\nEntrez un monde parmi {W_k} à évaluer (ou 'back' pour revenir au menu principal) : ").strip().lower()
        if world_choice == 'back':
            break
        if world_choice not in W_k:
            print("Monde invalide. Veuillez choisir dans la liste.")
            continue

        val = valuation_k(world_choice)
        print(f"\n--- Évaluation dans le Monde : {world_choice} ---")
        print(f"  Est-ce qu'il pleut ? (R): {R_prop.subs(val)}")
        print(f"  Est-ce qu'il fait beau ? (S): {S_prop.subs(val)}")

        # Formula 1: K_A(R)
        formula1_result = K_A(lambda x: R_prop.subs(valuation_k(x)), world_choice)
        print(f"  Alice sait qu'il pleut (K_A(R)): {formula1_result}")

        # Formula 2: K_A(S)
        formula2_result = K_A(lambda x: S_prop.subs(valuation_k(x)), world_choice)
        print(f"  Alice sait qu'il fait beau (K_A(S)): {formula2_result}")

        # Formula 3: K_A(R) OR K_A(S)
        formula3_result = Or(formula1_result, formula2_result)
        print(f"  Alice sait s'il pleut ou s'il fait beau (K_A(R) ∨ K_A(S)): {formula3_result}")

        # Formula 4: R_prop IMPLIES K_A(R_prop)
        formula4_result = Implies(R_prop.subs(val), K_A(lambda x: R_prop.subs(valuation_k(x)), world_choice))
        print(f"  S'il pleut, Alice sait qu'il pleut (R → K_A(R)): {formula4_result}")

        # Formula 5: P_A(R_prop) IMPLIES K_A(R_prop)
        formula5_result = Implies(P_A(lambda x: R_prop.subs(valuation_k(x)), world_choice), K_A(lambda x: R_prop.subs(valuation_k(x)), world_choice))
        print(f"  Si Alice croit qu'il pleut, elle sait qu'il pleut (P_A(R) → K_A(R)): {formula5_result}")

# --- Scenario 2: Temporal Logic (Future Possibilities) ---
def scenario_time():
    """
    Demonstrates temporal logic, focusing on future events.
    """
    print("\n--- Scénario : Logique Temporelle (Possibilités Futures) ---")
    print("Contexte : Le parcours d'un étudiant à travers un processus d'examen.")
    print("Les mondes représentent des points dans le temps/étapes du processus.")

    # Worlds:
    # t0: Before studying
    # t1: Studied, before exam
    # t2: Took exam, before results
    # t3: Passed exam
    # t4: Failed exam
    W_t = ["t0", "t1", "t2", "t3", "t4"]

    # Accessibility Relation (R_F for Future):
    # Represents the flow of time. From a world, you can access future worlds.
    R_t = [("t0", "t1"),
           ("t1", "t2"),
           ("t2", "t3"), ("t2", "t4")] # De 't2' (examen passé), on peut aller à 't3' (réussi) ou 't4' (échoué)

    # Valuation:
    # 'Study': true if the student has studied
    # 'Exam': true if the student has taken the exam
    # 'Pass': true if the student has passed
    # 'Fail': true if the student has failed
    V_t = {
        "Study": {"t1", "t2", "t3", "t4"},
        "Exam": {"t2", "t3", "t4"},
        "Pass": {"t3"},
        "Fail": {"t4"}
    }

    # Create Kripke frame for this scenario
    G_t = nx.DiGraph()
    G_t.add_nodes_from(W_t)
    G_t.add_edges_from(R_t)

    # Propositional variables for this scenario
    Study, Exam, Pass, Fail = symbols('Study Exam Pass Fail')

    def valuation_t(world):
        """Returns valuation for temporal scenario."""
        return {
            Study: world in V_t['Study'],
            Exam: world in V_t['Exam'],
            Pass: world in V_t['Pass'],
            Fail: world in V_t['Fail']
        }

    # Temporal operators:
    # F(phi) (Eventually phi) is represented by Dia
    # G(phi) (Always in the future phi) is represented by Box
    F = lambda formula, world: dia(formula, world, G_t)
    G_op = lambda formula, world: box(formula, world, G_t)

    # Formulas to evaluate
    # 1. F(Pass): Eventually, I will pass the exam.
    # 2. G_op(Study): I will always study (in the future).
    # 3. Study → F(Pass): If I study, I will eventually pass.
    # 4. F(Pass) AND F(Fail): It is possible that I pass AND possible that I fail (from t2).

    print("\nFormules à évaluer :")
    print("1. F(Pass) : Finalement, je réussirai l'examen.")
    print("2. G(Study) : J'étudierai toujours (à l'avenir).")
    print("3. Study → F(Pass) : Si j'étudie, je réussirai finalement.")
    print("4. F(Pass) ∧ F(Fail) : De t2, il est possible que je réussisse ET possible que j'échoue.")

    while True:
        world_choice = input(f"\nEntrez un monde parmi {W_t} à évaluer (ou 'back' pour revenir au menu principal) : ").strip().lower()
        if world_choice == 'back':
            break
        if world_choice not in W_t:
            print("Monde invalide. Veuillez choisir dans la liste.")
            continue

        val = valuation_t(world_choice)
        print(f"\n--- Évaluation dans le Monde : {world_choice} ---")
        print(f"  Étudié ? (Study): {Study.subs(val)}")
        print(f"  Examen passé ? (Exam): {Exam.subs(val)}")
        print(f"  Réussi ? (Pass): {Pass.subs(val)}")
        print(f"  Échoué ? (Fail): {Fail.subs(val)}")

        # Formula 1: F(Pass)
        formula1_result = F(lambda x: Pass.subs(valuation_t(x)), world_choice)
        print(f"  Finalement, je réussirai l'examen (F(Pass)): {formula1_result}")

        # Formula 2: G(Study)
        formula2_result = G_op(lambda x: Study.subs(valuation_t(x)), world_choice)
        print(f"  J'étudierai toujours (G(Study)): {formula2_result}")

        # Formula 3: Study → F(Pass)
        formula3_result = Implies(Study.subs(val), F(lambda x: Pass.subs(valuation_t(x)), world_choice))
        print(f"  Si j'étudie, je réussirai finalement (Study → F(Pass)): {formula3_result}")

        # Formula 4: F(Pass) AND F(Fail) (specifically from t2)
        if world_choice == "t2":
            formula4_result = Or(F(lambda x: Pass.subs(valuation_t(x)), world_choice), F(lambda x: Fail.subs(valuation_t(x)), world_choice))
            print(f"  De t2 : Possible de Réussir ∧ Possible d'Échouer (F(Pass) ∧ F(Fail)): {formula4_result}")
        else:
            print(f"  La formule F(Pass) ∧ F(Fail) est la plus pertinente depuis le monde t2.")


# --- Scenario 3: Deontic Logic (Obligation/Permissibility) ---
def scenario_obligation():
    """
    Demonstrates deontic logic, focusing on obligations and permissions.
    """
    print("\n--- Scénario : Logique Déontique (Obligation/Permissibilité) ---")
    print("Contexte : Règles dans une société simple ou un ménage.")
    print("Les mondes représentent des états moralement idéaux ou permissibles.")

    # Worlds:
    # w_ideal: All obligations met, no forbidden acts
    # w_tax_not_paid: Taxes not paid, but otherwise ideal
    # w_littered: Littered, but otherwise ideal
    # w_all_bad: Taxes not paid and littered
    W_o = ["w_ideal", "w_tax_not_paid", "w_littered", "w_all_bad"]

    # Accessibility Relation (R_O for Obligation):
    # From any world, you can only access worlds that are morally ideal (or permissible).
    # This is a common interpretation for deontic logic, where accessibility points to "ideal" worlds.
    R_o = [("w_ideal", "w_ideal"),
           ("w_tax_not_paid", "w_ideal"),
           ("w_littered", "w_ideal"),
           ("w_all_bad", "w_ideal")]

    # Valuation:
    # 'PayTax': true if taxes are paid
    # 'NoLitter': true if no littering occurred
    V_o = {
        "PayTax": {"w_ideal", "w_littered"},
        "NoLitter": {"w_ideal", "w_tax_not_paid"}
    }

    # Create Kripke frame for this scenario
    G_o = nx.DiGraph()
    G_o.add_nodes_from(W_o)
    G_o.add_edges_from(R_o)

    # Propositional variables for this scenario
    PayTax, NoLitter = symbols('PayTax NoLitter')

    def valuation_o(world):
        """Returns valuation for obligation scenario."""
        return {
            PayTax: world in V_o['PayTax'],
            NoLitter: world in V_o['NoLitter']
        }

    # Deontic operators:
    # O(phi) (Obligatory phi) is represented by Box
    # P(phi) (Permissible phi) is represented by Dia
    # F(phi) (Forbidden phi) is represented by O(Not(phi)) or Not(P(phi))
    O = lambda formula, world: box(formula, world, G_o)
    P = lambda formula, world: dia(formula, world, G_o)
    F = lambda formula, world: O(lambda x: Not(formula(x)), world) # Forbidden is Obligatory Not

    # Formulas to evaluate
    # 1. O(PayTax): It is obligatory to pay taxes.
    # 2. P(NoLitter): It is permissible not to litter.
    # 3. F(PayTax): It is forbidden to pay taxes. (Should be false)
    # 4. O(PayTax AND NoLitter): It is obligatory to pay taxes AND not litter.

    print("\nFormules à évaluer :")
    print("1. O(PayTax) : Il est obligatoire de payer les impôts.")
    print("2. P(NoLitter) : Il est permis de ne pas jeter de déchets.")
    print("3. F(PayTax) : Il est interdit de payer les impôts. (Ceci devrait être Faux)")
    print("4. O(PayTax ∧ NoLitter) : Il est obligatoire de payer les impôts ET de ne pas jeter de déchets.")

    while True:
        world_choice = input(f"\nEntrez un monde parmi {W_o} à évaluer (ou 'back' pour revenir au menu principal) : ").strip().lower()
        if world_choice == 'back':
            break
        if world_choice not in W_o:
            print("Monde invalide. Veuillez choisir dans la liste.")
            continue

        val = valuation_o(world_choice)
        print(f"\n--- Évaluation dans le Monde : {world_choice} ---")
        print(f"  Impôts payés ? (PayTax): {PayTax.subs(val)}")
        print(f"  Pas de déchets ? (NoLitter): {NoLitter.subs(val)}")

        # Formula 1: O(PayTax)
        formula1_result = O(lambda x: PayTax.subs(valuation_o(x)), world_choice)
        print(f"  Il est obligatoire de payer les impôts (O(PayTax)): {formula1_result}")

        # Formula 2: P(NoLitter)
        formula2_result = P(lambda x: NoLitter.subs(valuation_o(x)), world_choice)
        print(f"  Il est permis de ne pas jeter de déchets (P(NoLitter)): {formula2_result}")

        # Formula 3: F(PayTax)
        formula3_result = F(lambda x: PayTax.subs(valuation_o(x)), world_choice)
        print(f"  Il est interdit de payer les impôts (F(PayTax)): {formula3_result}")

        # Formula 4: O(PayTax AND NoLitter)
        formula4_result = O(lambda x: And(PayTax.subs(valuation_o(x)), NoLitter.subs(valuation_o(x))), world_choice)
        print(f"  Il est obligatoire de payer les impôts ET de ne pas jeter de déchets (O(PayTax ∧ NoLitter)): {formula4_result}")


# --- Main Menu and Project Execution ---
def main_menu():
    """
    Presents the main menu for the modal logic project.
    """
    print("\n--- Bienvenue dans le Projet d'Exemples Concrets de Logique Modale ---")
    print("Explorez différentes applications de la logique modale dans divers scénarios.")

    while True:
        print("\nChoisissez un scénario :")
        print("1. Logique Épistémique (Connaissance)")
        print("2. Logique Temporelle (Possibilités Futures)")
        print("3. Logique Déontique (Obligation/Permissibilité)")
        print("4. Quitter")

        choice = input("Entrez votre choix (1-4) : ").strip()

        if choice == '1':
            scenario_knowledge()
        elif choice == '2':
            scenario_time()
        elif choice == '3':
            scenario_obligation()
        elif choice == '4':
            print("Quitter le projet. Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")

if __name__ == "__main__":
    # Ensure And is imported for scenario_obligation
    from sympy import And
    main_menu()
