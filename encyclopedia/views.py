from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "text": entry,
            "title": title,
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": 404,
            "message": "Not Found",
            "submessage": "The page you appear to be looking for does not exist.",
        })
        


