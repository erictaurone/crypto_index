from django.urls import path
from . import views

urlpatterns = [
    path('Signup/', views.AccountsSignup.as_view(), name='accounts_signup'),
    path('Dashboard/<str:pk>/', views.AccountsUserDashboard.as_view(), name='accounts_user_dashboard'),
    path('Dashboard/<str:pk>/Profile_Settings/', views.AccountsUserDashboardProfileSettings.as_view(),
         name='accounts_user_dashboard_profile_settings'),
    path('Dashboard/<str:pk>/Historical_Transactions/', views.AccountsUserDashboardHistoricalTransactions.as_view(),
         name='accounts_user_dashboard_historical_transactions'),
]
