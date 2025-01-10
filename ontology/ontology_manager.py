from owlready2 import get_ontology

class OntologyManager:
    """
    Classe per gestire l'ontologia della qualità dell'aria.
    """
    def __init__(self, ontology_path):
        """
        Inizializza l'ontologia.
        Args:
            ontology_path (str): Percorso del file OWL dell'ontologia.
        """
        self.ontology = get_ontology(ontology_path).load()

    def get_classes(self):
        """
        Ottieni tutte le classi definite nell'ontologia.
        Returns:
            list: Elenco delle classi.
        """
        return [cls.name for cls in self.ontology.classes()]

    def get_individuals(self, class_name):
        """
        Ottieni tutte le istanze di una determinata classe.
        Args:
            class_name (str): Nome della classe.
        Returns:
            list: Elenco delle istanze della classe.
        """
        for cls in self.ontology.classes():
            if cls.name == class_name:
                return [individual.name for individual in cls.instances()]
        return []

    def query_sparql(self, query):
        """
        Esegui una query SPARQL sull'ontologia.
        Args:
            query (str): Query SPARQL.
        Returns:
            list: Risultati della query.
        """
        results = self.ontology.sparql(query)
        return results
