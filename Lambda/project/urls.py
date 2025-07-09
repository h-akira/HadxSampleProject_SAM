from hadx.urls import Path, Router
from .views import home

urlpatterns = [
  Path("", home, name="home"),
  Router("api", "api.urls", name="api"),
  Router("accounts", "accounts.urls", name="accounts"),
]
