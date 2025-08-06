package TP4;

import java.util.HashSet;
import a.e;
import be.fnord.util.logic.DefaultReasoner;
import be.fnord.util.logic.WFF;
import be.fnord.util.logic.defaultLogic.DefaultRule;
import be.fnord.util.logic.defaultLogic.RuleSet;
import be.fnord.util.logic.defaultLogic.WorldSet;

public class exo6 {

    public static void exo6() {
        // Création de l'ensemble de règles (défauts)
        RuleSet rules = new RuleSet();

        // d1 : a:b/b
        DefaultRule d1 = new DefaultRule();
        d1.setPrerequisite("a");
        d1.setJustificatoin("b");
        d1.setConsequence("b");
        rules.addRule(d1);

        // d2 : :¬a/¬a
        DefaultRule d2 = new DefaultRule();
        d2.setPrerequisite(a.e.EMPTY_FORMULA);
        d2.setJustificatoin(a.e.NOT + "a");
        d2.setConsequence(a.e.NOT + "a");
        rules.addRule(d2);

        // d3 : :a/a
        DefaultRule d3 = new DefaultRule();
        d3.setPrerequisite(a.e.EMPTY_FORMULA);
        d3.setJustificatoin("a");
        d3.setConsequence("a");
        rules.addRule(d3);

        // Priorités (d1 ≺ d3 ≺ d2)
        // Ici on suppose que ta classe RuleSet peut stocker les priorités,
        // sinon tu les affiches juste (l'implémentation du raisonneur ne les gère peut-être pas)
        String priorities = "d1 \u2264 d3 \u2264 d2"; // \u2264 = symbole ≤ pour la relation de priorité

        // Monde initial W = ∅ (vide)
        WorldSet w = new WorldSet();
        w.addFormula(a.e.EMPTY_FORMULA);

        try {
            a.e.println("/**************** Execution de la théorie priorisée ****************/\n");

            // Affichage clair de W, D, Priorités
            a.e.println("W = ");
            a.e.println(w.toString());

            a.e.println("D = {");
            a.e.println("\td1: " + d1.toString() + " ;");
            a.e.println("\td2: " + d2.toString() + " ;");
            a.e.println("\td3: " + d3.toString());
            a.e.println("}");

            a.e.println("\nPriorités: " + priorities + "\n");

            a.e.println("Extensions classiques possibles :\n");

            // Création du raisonneur avec W et règles
            DefaultReasoner reasoner = new DefaultReasoner(w, rules);

            HashSet<String> extensions = reasoner.getPossibleScenarios();

            // Affichage des extensions classiques
            for (String ext : extensions) {
                a.e.println("E: Th(W \u222A (" + ext + "))");
                a.e.incIndent();
                WFF worldExt = new WFF("((" + w.getWorld() + ") & (" + ext + "))");
                a.e.println("= " + worldExt.getClosure());
                a.e.decIndent();
                a.e.println("");
            }

        } catch (Exception e) {
            a.e.println("Erreur lors de l'exécution : " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        exo6();
    }
}
