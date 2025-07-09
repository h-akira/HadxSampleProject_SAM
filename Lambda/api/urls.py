from hadx.urls import Path, Router
from .views import token_exchange, auth_status, logout

urlpatterns = [
    Path("auth/token", token_exchange, name="token_exchange"),
    Path("auth/status", auth_status, name="auth_status"),
    Path("auth/logout", logout, name="logout"),
] 