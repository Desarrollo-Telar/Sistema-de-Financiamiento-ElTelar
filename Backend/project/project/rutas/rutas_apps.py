

# URLS
from django.urls import path, include

urlpatterns_apps = [
    path('users/', include('apps.users.urls')),
    path('roles_permisos/', include('apps.roles.urls')),
    path('customers/', include('apps.customers.urls')),
    path('addresses/', include('apps.addresses.urls')),
    path('codes/', include('apps.codes.urls')),
    path('financial_information/', include('apps.FinancialInformation.urls')),
    path('plan_inversion/', include('apps.InvestmentPlan.urls')),
    path('imagen/', include('apps.pictures.urls')),
    path('documents/', include('apps.documents.urls')),
    path('contable/', include('apps.accountings.urls')),
    path('financings/',include('apps.financings.urls')),
    path('actividades/',include('apps.actividades.urls')),
]