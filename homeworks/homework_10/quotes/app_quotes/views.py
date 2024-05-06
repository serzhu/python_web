from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag
from collections import Counter


@login_required
def add_author(request: HttpRequest):
    form = AuthorForm(instance=Author())
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            form.save()
            return redirect(to="app_quotes:quotes")
    return render(request, "app_quotes/add_author.html", context={"form": form})


@login_required
def add_quote(request: HttpRequest):
    form = QuoteForm(instance=Quote())
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=False)
            author_name = request.POST.get("author", "").strip()
            author, created = Author.objects.get_or_create(fullname=author_name)
            quote.author = author
            quote.save()
            if created:
                messages.info(request, "Created new author. Add more info!")
            for tag in request.POST.get("tags").split():
                tag_obj, _ = Tag.objects.get_or_create(tag=tag)
                quote.tags.add(tag_obj)
            messages.success(request, "Quote added successfully!")
            return redirect("app_quotes:add_quote")
    return render(request, "app_quotes/add_quote.html", context={"form": form})


def author_info(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "app_quotes/author_info.html", {"author": author})


def main(request, page=1):
    quotes = Quote.objects.all().prefetch_related("tags")
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    counter = Counter(quotes.values_list("tags", flat=True))
    most_common = [item[0] for item in counter.most_common(10)]
    top10 = [Tag.objects.get(pk=tag_id) for tag_id in most_common]
    return render(
        request,
        "app_quotes/index.html",
        context={"quotes": quotes_on_page, "tags": top10},
    )


def quotes_by_tag(request, tag_id, page=1):
    tag = get_object_or_404(Tag, pk=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "app_quotes/quotes_by_tag.html",
        context={"quotes": quotes_on_page, "tag_id": tag_id},
    )
