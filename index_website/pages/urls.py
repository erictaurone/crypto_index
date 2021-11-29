from django.urls import path
from .views import PagesHomePage, PagesJoinUs, PagesContactUs, PagesAboutTeam, PagesProjectRoadmap

urlpatterns = [
    path('', PagesHomePage.as_view(), name='pages_home_page'),
    path('Contact_Us', PagesContactUs.as_view(), name='pages_contact_us'),
    path('Project_Roadmap', PagesProjectRoadmap.as_view(), name='pages_project_roadmap'),
    path('About_Team', PagesAboutTeam.as_view(), name='pages_about_team'),
    path('Join_Us', PagesJoinUs.as_view(), name='pages_join_us'),
]
