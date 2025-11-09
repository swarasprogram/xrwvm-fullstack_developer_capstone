from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name = "djangoapp"

urlpatterns = [
    # Home / basic pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="djangoapp:home"), name="logout"),
    path("signup/", views.signup, name="signup"),

    # Dealers & reviews
    path("dealers/", views.dealers, name="dealers"),
    path("dealers/state/<str:state>/", views.dealers_by_state, name="dealers_by_state"),
    path("dealer/<int:dealer_id>/", views.dealer_detail, name="dealer_detail"),
    path("add-review/<int:dealer_id>/", views.add_review, name="add_review"),

    # Cars (for the car makes screenshot)
    path("cars/", views.cars, name="cars"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
