import markdown
import os

from django.http import Http404
from django.shortcuts import render


def list(request):
    return render(request, 'docs/list.html', {})


def detail(request, title='Not Found', source='notfound.md'):
    view_path = os.path.dirname(__file__)
    doc_path = os.path.join(view_path, source)

    if not os.path.exists(doc_path):
        raise Http404('No such documenation exist.')

    with open(doc_path) as doc:
        content = markdown.markdown(doc.read())

    return render(request, 'docs/detail.html', {
        'title': title,
        'content': content,
    })
