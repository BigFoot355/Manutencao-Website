from django.urls import path
from .views import lista_equipamentos, criar_equipamento, editar_equipamento, excluir_equipamento, detalhes_equipamento, alterar_status, entregar_equipamento, confirmar_exclusao
from .views import lista_intervencoes, criar_intervencao, editar_intervencao, excluir_intervencao
from .views import lista_tecnicos, criar_tecnico, editar_tecnico, detalhes_tecnico, excluir_tecnico
from .views import relatorios
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('', lista_equipamentos, name='lista_equipamentos'),
    path('novo/', criar_equipamento, name='criar_equipamento'),
    path('editar/<int:pk>/', editar_equipamento, name='editar_equipamento'),
    path('excluir/<int:pk>/', excluir_equipamento, name='excluir_equipamento'),
    path('detalhes/<int:pk>/', detalhes_equipamento, name='detalhes_equipamento'),
    path('equipamento/alterar_status/<int:pk>/', alterar_status, name='alterar_status'),
    path('equipamento/<int:equipamento_id>/entregar/', entregar_equipamento, name='entregar_equipamento'),
    path('equipamento/<int:pk>/confirmar_exclusao/', confirmar_exclusao, name='confirmar_exclusao'),
    
    
    path('intervencoes/', lista_intervencoes, name='lista_intervencoes'),
    path('intervencoes/novo/<int:equipamento_id>/', criar_intervencao, name='criar_intervencao'),
    path('intervencoes/editar/<int:pk>/', editar_intervencao, name='editar_intervencao'),
    path('intervencoes/excluir/<int:pk>/', excluir_intervencao, name='excluir_intervencao'),
    
       
    path('tecnicos/', lista_tecnicos, name='lista_tecnicos'),
    path('tecnicos/criar/', criar_tecnico, name='criar_tecnico'),
    path('tecnicos/editar/<int:pk>/', editar_tecnico, name='editar_tecnico'),
    path('tecnicos/detalhes/<int:pk>/', detalhes_tecnico, name='detalhes_tecnico'),
    path('tecnicos/excluir/<int:pk>/', excluir_tecnico, name='excluir_tecnico'),
    
    path('relatorios/', relatorios, name='relatorios'),
]
