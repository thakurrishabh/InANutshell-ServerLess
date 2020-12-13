from django.contrib import admin
from django.urls import path,include
from  . import views
# from inanutshell_app.views import GoogleLogin

from django.conf.urls import url
from inanutshell import settings
from django.contrib.auth import views as auth_views

urlpatterns = [

    #path('', GoogleLogin.as_view(), name='google_login'),
    path('', views.login, name='login'),
    #path('login/', auth_views.LoginView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='login_to_home'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout_to_home'),
    path('<slug:un>', views.frm_docupload_view, name='index'),
    #path('index/', views.frm_docupload_view, name='index'),
    # path('', views.frm_docupload_view, name='index'),
    # path('', views.index, name=''),
    path('<slug:un>/fn/<int:fn>/del', views.delete_doc, name='delete_doc'),
    path('<slug:un>/documents', views.documents, name='documents'),
    path('<slug:un>/cy/<str:cy>', views.category, name='category'),
    path('<slug:un>/fn/<int:fn>', views.webview, name='webview'),
    path('<slug:un>/about', views.about, name='about'),
    path('<slug:un>/contact', views.contact, name='contact'),
]
