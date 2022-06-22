from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from random import choice

from . import util

# Index page. Displays list of entries.
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


# Allows for users to create pages.
def create(request):
    # Check if method is post
    if request.method == "POST":
        
        # Get title and entry from form
        title = request.POST.get("title")
        entry = request.POST.get("entry")

        # Check if entry name already exists.
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error": 409,
                "message": "Conflict",
                "submessage": "The page you are trying to create has the same title as another page."
            })

        # Save entry
        util.save_entry(title, entry)
        
        # Redirect back to page index
        return redirect("/")
    else:
        # Render form
        return render(request, "encyclopedia/create.html")


# Allows users to edit existing entries.
def edit(request, title):
    # Get all titles
    titles = util.list_entries()
    
    # Check if title exists
    if title not in titles:
        # Render template with error message
        return render(request, "encyclopedia/error.html", {
            "error": 404,
            "message": "Not Found",
            "submessage": "The file you are trying to edit does not exist."
        })
    
    # Check if method is post
    if request.method == "POST":
        # Get title and entry from form
        entry = request.POST.get("entry")
        # Save entry
        util.save_entry(title, entry)
        
        # Redirect back to page index
        return redirect("/")
    else:
        # Get title
        entry_titles = util.list_entries()
        for entry_title in entry_titles:
            if entry_title == title:
                break
        
        # Get content
        content = util.get_entry(title)

        # Render template and provide variables
        return render(request, "encyclopedia/edit.html", {
            "title": entry_title,
            "content": content
        })


# Allows users to look at a random page.
def random(request):
    entries = util.list_entries()
    print(entries)
    random_entry = choice(entries)
    print(random_entry)
    return redirect("wiki/"+random_entry)
