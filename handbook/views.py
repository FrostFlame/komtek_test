from django.shortcuts import render
from handbook.models import Handbook


from django.views import View


def main_page(request):
    return render(
        request,
        'handbook/main_page.html',
        {'handbooks': Handbook.objects.all(), 'popular_for_week': True}
    )


def custom_handler404(request, exception):
    return render(request, "handbook/base/page_not_found.html", status=404)


class HandbookView(View):
    def get(self, request, pk):
        handbook = Handbook.objects.get(pk=pk)
        return render(
            request,
            'handbook/handbook_page.html',
            {'handbook': handbook}
        )
