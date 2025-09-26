from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON
from .models import SparqlResult

# Create your views here.

def fetch_and_store_data(request):
    """
    Fetches data from a SPARQL endpoint and stores it in the database.
    This version fetches painters and their birth dates.
    """
    # A SPARQL query to get painters and their birth dates.
    query_string = """
    SELECT ?painter ?painterLabel ?date WHERE {
      ?painter wdt:P31 wd:Q5;  # instance of human
               wdt:P106 wd:Q1028181; # occupation is painter
               wdt:P569 ?date.       # date of birth
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 10
    """

    # Set up the SPARQL endpoint
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        
        # Clear existing data to avoid duplicates for this example
        SparqlResult.objects.all().delete()

        # Iterate through the results and save to the database
        for result in results["results"]["bindings"]:
            subject = result["painterLabel"]["value"]
            predicate = "date of birth"
            object_val = result["date"]["value"]
            
            # Check if a similar record already exists to prevent duplicates
            if not SparqlResult.objects.filter(subject=subject, object=object_val).exists():
                SparqlResult.objects.create(
                    subject=subject,
                    predicate=predicate,
                    object=object_val
                )

        message = "Data successfully fetched and stored in the database!"
    except Exception as e:
        message = f"An error occurred: {e}"
    
    return HttpResponse(message)

def display_data(request):
    """
    Fetches all stored data and displays it on a web page.
    """
    # Retrieve all objects from the SparqlResult collection
    data = SparqlResult.objects.all()
    # Pass the retrieved data to the template for rendering
    return render(request, 'data_display.html', {'data': data})
