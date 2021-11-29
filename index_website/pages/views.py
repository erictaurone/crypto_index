from django.shortcuts import render
from django.views.generic.base import TemplateView


class PagesHomePage(TemplateView):
    template_name = 'pages/pages_home_page.html'


class PagesAboutTeam(TemplateView):
    template_name = 'pages/pages_about_team.html'


class PagesContactUs(TemplateView):
    template_name = 'pages/pages_contact_us.html'


class PagesJoinUs(TemplateView):
    template_name = 'pages/pages_join_us.html'


class PagesProjectRoadmap(TemplateView):
    template_name = 'pages/pages_project_roadmap.html'
