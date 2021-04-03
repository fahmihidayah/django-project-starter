from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

class AdminView(TemplateView):
    template_name = 'admin/base.html'