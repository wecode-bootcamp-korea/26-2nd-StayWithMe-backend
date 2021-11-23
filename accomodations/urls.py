from django.urls import path

from accomodations.views import AccomodationDetailView, AccomodationListView

urlpatterns = [
    path('', AccomodationListView.as_view()),
    path('/<int:accomodation_id>', AccomodationDetailView.as_view())
]