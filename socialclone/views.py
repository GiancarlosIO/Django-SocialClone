from django.views.generic import TemplateView

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanskPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = 'home.html'