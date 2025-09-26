from django.db import models

class SparqlResult(models.Model):
    """
    A model to store consolidated results from a SPARQL query.
    
    The subject stores the entity's name (Scientist), and the object stores 
    all consolidated details (dates, works, fields).
    """
    # Stores the name of the Scientist/Subject
    subject = models.CharField(max_length=500)
    
    # Stores the consolidated, multi-line information block from GROUP_CONCAT
    object = models.CharField(max_length=5000)

    def __str__(self):
        """
        String representation of the model instance.
        """
        return self.subject

    class Meta:
        pass