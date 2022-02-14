from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown
from . import util
from bs4 import BeautifulSoup
from django import forms
import random

class EntryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=500)


def index(request):
    entries = util.list_entries()
    q = request.GET.get('q')
    if q:
        filtered = list(filter(lambda entry: q.lower() in entry.lower(), entries))
        exact = list(filter(lambda entry: q.lower() == entry.lower(), entries))
        if len(exact) > 0:
            entry = util.get_entry(exact[0])
            html = markdown.markdown(entry)
            soup = BeautifulSoup(html, "html.parser")
            title = None if soup.h1 else "No title"
            return render(request, "encyclopedia/entry.html", {
                "head": exact[0],
                "html":html,
                "title":title
                    })
        return render(request, "encyclopedia/index.html", {
        "entries": filtered
            })
    return render(request, "encyclopedia/index.html", {
        "entries": entries
            })


def get_entry(request, filename): 
        entry = util.get_entry(filename)
        if entry:
            html = markdown.markdown(entry)
            soup = BeautifulSoup(html, "html.parser")
            title = None if soup.h1 else "No title"
            return render(request, "encyclopedia/entry.html",{
                "head": filename,
                "title": title,
                "html":html,
                    })
        return render(request, "encyclopedia/error.html", {
            "message": 'The requested page was not found.'
        })       

def create(request):
    if request.method == "POST":
        filename = request.POST['filename']
        if filename.lower() in map(lambda entries: entries.lower(), util.list_entries()):
            return render(request, "encyclopedia/error.html", {
                'message': "The page already exists."    
            })
        description = request.POST['description']
        util.save_entry(filename, description)
        return HttpResponseRedirect(filename)
    return render(request, "encyclopedia/create.html", {
        "action": "creation",
        "title": "New entry"
    })

def edit(request, filename):
    if request.method == "POST":
        description = request.POST['description']
        util.save_entry(filename, description)
        return HttpResponseRedirect("/wiki/"+filename)
    content = util.get_entry(filename)
    return render(request, "encyclopedia/edit.html", {
       # "action": "edition",
        "filename" : filename,
        "title" : "Edit " + filename + " content",
        "content": content,
        })

def redirect(request):
    filename = random.choice(util.list_entries())
    return HttpResponseRedirect('/wiki/' + filename)