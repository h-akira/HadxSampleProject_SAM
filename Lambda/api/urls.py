from hadx.urls import Path, Router
from .views import token_exchange, auth_status, logout, sample

urlpatterns = [
    Path("auth/token", token_exchange, name="token_exchange"),
    Path("auth/status", auth_status, name="auth_status"),
    Path("auth/logout", logout, name="logout"),
    Path("sample", sample, name="sample"),
] 