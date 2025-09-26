# data_app/views.py
from urllib.error import HTTPError
from django.shortcuts import render
from django.http import HttpResponse
from .models import SparqlResult
from SPARQLWrapper import SPARQLWrapper, JSON# <-- HTTPError is misplaced here!

# Define the SPARQL endpoint for Wikidata
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

def fetch_and_store_data(request):
    """
    Fetches consolidated data for the top 20 influential scientists from Wikidata
    using a robust SPARQL query and stores it in MongoDB.
    
    Includes a FILTER to ensure only entries with a defined English label are stored,
    preventing broken QID entries like "Q762".
    """
    # Define the SPARQL query to fetch Scientist data
    query = """
    SELECT ?scientist ?scientistLabel (GROUP_CONCAT(DISTINCT ?birthDateLabel; separator="; ") AS ?birthDates)
           (GROUP_CONCAT(DISTINCT ?deathDateLabel; separator="; ") AS ?deathDates)
           (GROUP_CONCAT(DISTINCT ?fieldOfWorkLabel; separator="; ") AS ?fieldsOfWork)
           (GROUP_CONCAT(DISTINCT ?notableWorkLabel; separator="; ") AS ?notableWorks)
    WHERE 
    {
      ?scientist wdt:P31 wd:Q5;        # Instance of Human
                 wdt:P106 wd:Q901;     # Occupation: Scientist
                 wdt:P569 ?birthDate.
      
      OPTIONAL { ?scientist wdt:P570 ?deathDate. }
      OPTIONAL { ?scientist wdt:P101 ?fieldOfWork. }
      OPTIONAL { ?scientist wdt:P800 ?notableWork. }
      
      # Labels Service: Get human-readable labels for everything
      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
        ?scientist rdfs:label ?scientistLabel.
        ?birthDate rdfs:label ?birthDateLabel.
        ?deathDate rdfs:label ?deathDateLabel.
        ?fieldOfWork rdfs:label ?fieldOfWorkLabel.
        ?notableWork rdfs:label ?notableWorkLabel.
      }
      
      # FIX for QID entries: Only include results where a scientistLabel is present
      FILTER(LANG(?scientistLabel) = "en")
    }
    GROUP BY ?scientist ?scientistLabel
    LIMIT 20
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        # CRITICAL: Delete old data before saving new consolidated data
        SparqlResult.objects.all().delete()
        
        results = sparql.query().convert()
        
        # Process and save the consolidated results
        for item in results["results"]["bindings"]:
            # Use scientistLabel, which is guaranteed to be present and in English due to the FILTER
            scientist_name = item.get("scientistLabel", {}).get("value", "N/A")
            
            # Aggregate all details into a single string for the 'object' field
            details = [
                f"Born: {item.get('birthDates', {}).get('value', 'Unknown')}",
                f"Died: {item.get('deathDates', {}).get('value', 'Still living')}",
                f"Fields: {item.get('fieldsOfWork', {}).get('value', 'N/A')}",
                f"Notable Works: {item.get('notableWorks', {}).get('value', 'N/A')}"
            ]
            consolidated_object = "\n".join(details)
            
            # Save the new, clean consolidated entry
            SparqlResult.objects.create(
                subject=scientist_name, 
                object=consolidated_object
            )
        
        return HttpResponse("Data successfully fetched, consolidated, and stored in the database! (20 clean entries)")

    except HTTPError as e:
        # Handle network/server errors from Wikidata
        return HttpResponse(f"Error fetching data from Wikidata (HTTP Error): {e.response.status} - {e.response.reason}", status=e.response.status)
    except Exception as e:
        # Catch-all for any other errors (e.g., database connection, query parsing)
        return HttpResponse(f"An unexpected error occurred during data fetching or storage: {e}", status=500)

def display_data(request):
    """
    Renders the data display template with all currently stored SPARQL results.
    """
    # Fetch all data stored in the database
    data = SparqlResult.objects.all()
    
    # Pass the data to the template for display
    context = {'data': data}
    return render(request, 'data_app/data_display.html', context)
