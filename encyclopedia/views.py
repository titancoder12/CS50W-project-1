from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponseRedirect, HttpResponse
from django import forms

from . import util

# Index page or home page. Displays list of entries.
def index(request):
    # Render template and provide list of entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Displays the entry.
def entry(request, title):
    # Get entry
    entry = util.get_entry(title)
    # Check if entry exists
    if entry is not None:
        # convert markdown to html
        text = markdown2.markdown(entry)
        # get title
        entry_titles = util.list_entries()
        for entry_title in entry_titles:
            if entry_title == title:
                break

        # Render template and provide variables
        return render(request, "encyclopedia/entry.html", {
            "text": text,
            "title": entry_title,
        })
    else:
        # Render template with error message and return status code 404 not found
        return HttpResponse(render(request, "encyclopedia/error.html", {
            "error": 404,
            "message": "Not Found",
            "submessage": "The page you appear to be looking for does not exist.",
        }), status=404) 

# Allows users to search for entries.
# Fix error on line 40
def search(request):
    if request.method == "GET":
        q = request.GET.get('q')
        # Check if request matches any entry. If it does, redirect to entry
        if util.get_entry(q) is not None:
            return redirect("wiki/"+q)
        
        # Initialize variables
        entries = util.list_entries()
        results = []
        num_results = 0
        # Lowercase q
        lower_q = q.lower()

        # Keep on checking if the words in entries are in q
        for i in range(len(entries)):
            # Words in entry are in q then add entry to list of results
            if lower_q in entries[i].lower():
                results.append(entries[i])
                num_results += 1
        # Add "s" to the word "result" if there is one result
        if num_results == 1:
            s = ""
        else:
            s = "s"

        # Render template and provide variables
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "num_results": num_results,
            "query": q,
            "s": s
        })
    
    # Return to index if method is not GET
    return HttpResponseRedirect("/")