from django.db import models

# Create your models here.

class SparqlResult(models.Model):
    """
    A model to store the results from a SPARQL query.
    
    Since SPARQL queries often return a set of subject-predicate-object triples,
    this model is designed to store one such triple per instance.
    """
    subject = models.CharField(max_length=255)
    predicate = models.CharField(max_length=255)
    object = models.CharField(max_length=255)

    def __str__(self):
        """
        String representation of the model instance.
        """
        return f'{self.subject} - {self.predicate} - {self.object}'

    class Meta:
        # Djongo doesn't require a primary key to be explicitly defined,
        # it will use MongoDB's `_id` field automatically.
        # This is here as an example, but can be omitted.
        pass
