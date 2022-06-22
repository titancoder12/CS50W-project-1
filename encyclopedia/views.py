from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponseRedirect
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
        # Render template and provide variables
        return render(request, "encyclopedia/entry.html", {
            "text": markdown2.markdown(entry),
            "title": title,
        })
    else:
        # Render template and provide variables
        return render(request, "encyclopedia/error.html", {
            "error": 404,
            "message": "Not Found",
            "submessage": "The page you appear to be looking for does not exist.",
        })

# Allows users to search for entries.
# Fix error on line 40
def search(request, q):
    if request.method == "GET":
        # Check if request matches any entry. If it does, redirect to entry
        if util.get_entry(q) is not None:
            return redirect("wiki/"+q) # Fix this. Error: returns url localhost:8000/search/wiki instead of localhost:8000/wiki/ENTRY_TITLE
        
        entries = util.list_entries()
        results = []
        num_results = 0
        # lowercase q
        original_q = q
        q.lower

        # Keep on checking if the words in entries are in q
        for i in range(len(entries)):
            # Words in entry are in q then add entry to list of results
            if q in entries[i].lower():
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
            "query": original_q,
            "s": s
        })
    
    # Return to index if method is not GET
    return HttpResponseRedirect("/")


