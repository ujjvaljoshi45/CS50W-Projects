import random
from django import forms
from django.shortcuts import redirect, render
from . import util
from markdown2 import Markdown

entries_list = util.list_entries()
markdowner = Markdown()

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    data = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "cols":10}))

class EditEntryForm(forms.Form):
    title = forms.CharField(label = "title")
    body = forms.CharField(label="body", widget=forms.Textarea(attrs={'rows':1,'cols':10}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def show_entry(request,title):
    mdcontent = util.get_entry(title)
    htmlcontent = markdowner.convert(mdcontent)
    return render(request,"encyclopedia/show_entry.html", {
        "entry":htmlcontent, "title" : title,
    })

def edit_entry(request,title):
    if request.POST:       
        editEntryForm = EditEntryForm(request.POST)
        if editEntryForm.is_valid():
            title = editEntryForm.cleaned_data.get("title")
            body = editEntryForm.cleaned_data.get("body")
            util.save_entry(title,body)
            htmlContent = markdowner.convert(body)
            return render(request,"encyclopedia/show_entry.html", {
                "title" : title, "entry":htmlContent
            })
    else:
        editform = EditEntryForm({"title":title, "body": util.get_entry(title)})
        return render(request, "encyclopedia/edit_entry.html", {
            "editform" : editform
        })

def random_entry(request):
    return render(request,"encyclopedia/show_entry.html", {
        "entry":util.get_entry(random.choice(entries_list))
    })
def add_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].replace(" ","")
            data = form.cleaned_data["data"]
            util.save_entry(title,data)
            return redirect("index")
        else:
            return render(request,"encyclopedia/add_entry.html", {
                "form":form
            })
    else:
        return render(request,"encyclopedia/add_entry.html",{
            "form":NewEntryForm()
        })