package TP4;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class exo1 {

    // Default Rule class
    static class DefaultRule {
        String prerequisite;
        String justification;
        String consequence;

        public DefaultRule(String prerequisite, String justification, String consequence) {
            this.prerequisite = prerequisite;
            this.justification = justification;
            this.consequence = consequence;
        }

        @Override
        public String toString() {
            return "(" + prerequisite + " : " + justification + " / " + consequence + ")";
        }
    }

    // Reasoner
    static class DefaultReasoner {
        private Set<String> world;
        private List<DefaultRule> rules;

        public DefaultReasoner(Set<String> world, List<DefaultRule> rules) {
            this.world = world;
            this.rules = rules;
        }

        public Set<String> computeExtension() {
            Set<String> extension = new HashSet<>(world);
            boolean changed;

            do {
                changed = false;
                for (DefaultRule rule : rules) {
                    if (extension.contains(rule.prerequisite) &&
                        !extension.contains(negate(rule.justification)) &&
                        !extension.contains(rule.consequence)) {
                        extension.add(rule.consequence);
                        changed = true;
                    }
                }
            } while (changed);

            return extension;
        }

        private String negate(String literal) {
            return literal.startsWith("¬") ? literal.substring(1) : "¬" + literal;
        }
    }

    public static void main(String[] args) {
        // Define default rules
        List<DefaultRule> rules = new ArrayList<>();
        rules.add(new DefaultRule("A", "B", "C"));   // d1
        rules.add(new DefaultRule("A", "¬C", "D"));  // d2

        // Define test worlds (Java 8 compatible)
        List<Set<String>> worlds = new ArrayList<>();

        Set<String> w1 = new HashSet<>();
        w1.add("¬A");
        worlds.add(w1);

        Set<String> w2 = new HashSet<>();
        w2.add("A");
        w2.add("¬B");
        worlds.add(w2);

        Set<String> w3 = new HashSet<>();
        w3.add("A");
        w3.add("¬C ∨ ¬D");
        worlds.add(w3);

        Set<String> w4 = new HashSet<>();
        w4.add("A");
        w4.add("¬B ∧ C");
        worlds.add(w4);

        // Run reasoner
        for (int i = 0; i < worlds.size(); i++) {
            Set<String> w = worlds.get(i);
            DefaultReasoner reasoner = new DefaultReasoner(w, rules);
            Set<String> extension = reasoner.computeExtension();

            System.out.println("==== World W" + (i + 1) + " ====");
            System.out.println("Input: " + w);
            System.out.println("Extension: " + extension);
            System.out.println();
        }
    }
}
