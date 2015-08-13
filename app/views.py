"""
Definition of views.
"""

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest
from django.shortcuts import render
from django.template import RequestContext

from app.models import ReaperResult

def home(request):
    """Renders the home page."""
    results = ReaperResult.objects.all()
    paginator = Paginator(results.order_by('-created_at'), 100)

    page = request.GET.get('page', 1)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(1)

    ppage = None
    npage = None
    if results.has_previous():
            ppage = results.previous_page_number()
    if results.has_next():
        npage = results.next_page_number()

    return render(
            request,
            'app/index.html',
            context_instance=RequestContext(request,
            {
                'year': datetime.now().year,
                'projects': ReaperResult.objects.filter(score__gte=60).count(),
                'results': results,
                'tpages': paginator.num_pages,
                'ppage': ppage,
                'npage': npage,
                'cpage': page,
            }
        )
    )

def contact(request):
    """Renders the contact page."""
    return render(
        request,
        'app/contact.html',
        context_instance=RequestContext(request,
            {
                'year': datetime.now().year,
            }
        )
    )