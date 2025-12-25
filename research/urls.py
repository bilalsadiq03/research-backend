from django.urls import path
from .views import HealthCheckView, StartResearchView


urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path("start/", StartResearchView.as_view(), name="start-research"),
]
