from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipamento, Intervencao, Tecnico
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import EquipamentoForm, IntervencaoForm, TecnicoForm
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField, IntegerField


@login_required
def lista_equipamentos(request):
    # Obtém os parâmetros da query string
    nome = request.GET.get('nome', '')
    marca = request.GET.get('marca', '')
    #modelo = request.GET.get('modelo', '')
    numero_serie = request.GET.get('numero_serie', '')  # Novo campo
    status = request.GET.get('status', '')
    mostrar_entregues = request.GET.get('mostrar_entregues', '')  # Checkbox

    # Começamos com todos os equipamentos não apagados
    equipamentos = Equipamento.objects.filter(apagado=False)

    # Por padrão, ocultamos os equipamentos entregues, a menos que "Mostrar Entregues" esteja ativado ou o usuário filtre por "Entregue"
    if not (mostrar_entregues == 'on' or status == 'Entregue'):
        equipamentos = equipamentos.exclude(status='Entregue')

    # Aplicação dos filtros adicionais
    if nome:
        equipamentos = equipamentos.filter(nome__icontains=nome)

    if marca:
        equipamentos = equipamentos.filter(marca__icontains=marca)

    #if modelo:
    #    equipamentos = equipamentos.filter(modelo__icontains=modelo)
    if numero_serie:  # Aplica o novo filtro
        equipamentos = equipamentos.filter(numero_serie__icontains=numero_serie)

    if status:
        equipamentos = equipamentos.filter(status=status)

    return render(request, 'equipamentos/lista.html', {
        'equipamentos': equipamentos,
        'nome': nome,
        'marca': marca,
        #'modelo': modelo,
        'numero_serie': numero_serie,  
        'status': status,
        'mostrar_entregues': mostrar_entregues,  # Para manter o estado do checkbox
    })


@login_required
def criar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            equipamento = form.save(commit=False)  # Não salva ainda
            equipamento.created_by = request.user  # Define o usuário atual
            equipamento.created_at = timezone.now()  # Define a data/hora atual
            equipamento.updated_by = request.user  # Inicialmente o mesmo criador
            equipamento.updated_at = timezone.now()
            equipamento.save()  # Agora salva

            return redirect('lista_equipamentos')
        else:
            print(form.errors)  # Depuração

    else:
        form = EquipamentoForm()

    return render(request, 'equipamentos/form.html', {'form': form, 'titulo': 'Novo Equipamento'})


@login_required
def editar_equipamento(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            equipamento = form.save(commit=False)
            equipamento.updated_by = request.user
            equipamento.updated_at = timezone.now()
            equipamento.save()
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento)

    return render(request, 'equipamentos/form.html', {'form': form, 'titulo': 'Editar Equipamento', 'is_editing': True})


@login_required
def excluir_equipamento(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    if request.method == 'POST':
        # Marca o equipamento como apagado
        equipamento.apagado = True
        equipamento.updated_by = request.user  # Registra quem fez a exclusão
        equipamento.updated_at = timezone.now()  # Atualiza a data de modificação
        equipamento.save()
        #equipamento.delete()
        return redirect('lista_equipamentos')
    return render(request, 'equipamentos/confirmar_exclusao.html', {'equipamento': equipamento})


def confirmar_exclusao(request, pk):
    # Obtém o equipamento pelo ID (pk)
    equipamento = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        # Quando o formulário é enviado, marca o equipamento como "apagado"
        equipamento.apagado = True
        equipamento.save()
        return redirect('lista_equipamentos')  # Redireciona para a lista de equipamentos

    # Se for um GET, exibe a página de confirmação
    return render(request, 'equipamentos/confirmar_exclusao.html', {'equipamento': equipamento})


@login_required
def detalhes_equipamento(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)
    intervencao_list = Intervencao.objects.filter(equipamento=equipamento)
    return render(request, 'equipamentos/detalhes.html', {
        'equipamento': equipamento,
        'intervencao_list': intervencao_list,
    })
    

@login_required
def lista_intervencoes(request):    
    equipamentos = Equipamento.objects.all()
    tecnicos = Tecnico.objects.all()
    intervencoes = Intervencao.objects.filter(apagado=False).order_by('-hora_inicio')
    
    equipamento_filter = request.GET.get('equipamento')
    if equipamento_filter:
        intervencoes = intervencoes.filter(equipamento_id=equipamento_filter)
    
    tecnico_filter = request.GET.get('tecnico')
    if tecnico_filter:
        intervencoes = intervencoes.filter(tecnico_id=tecnico_filter)
    
    data_filter = request.GET.get('data')
    if data_filter:
        try:
            data_filter = datetime.strptime(data_filter, '%Y-%m-%d').date()
            intervencoes = intervencoes.filter(hora_inicio__date=data_filter)
        except ValueError:
            pass  # Caso o formato da data seja inválido, não faz nada
        
    return render(request, 'intervencoes/lista.html', {
            'intervencoes': intervencoes,
            'equipamentos': equipamentos,
            'tecnicos': tecnicos,
    })


@login_required
def criar_intervencao(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, id=equipamento_id)
    if request.method == "POST":
        form = IntervencaoForm(request.POST)
        if form.is_valid():
            intervencao = form.save(commit=False)
            intervencao.equipamento = equipamento
            intervencao.created_by = request.user  # Define quem criou a intervenção
            intervencao.created_at = timezone.now()  # Define a data/hora atual
            
            # Atualiza o status do equipamento
            equipamento.status = "Em Reparação"
            equipamento.updated_by = request.user  # Registra quem alterou o equipamento
            equipamento.updated_at = timezone.now()
            equipamento.save()

            intervencao.save()
            return redirect('detalhes_equipamento', pk=equipamento.id)
    else:
        form = IntervencaoForm()
    
    return render(request, 'intervencoes/form.html', {'form': form, 'equipamento': equipamento})

@login_required
def editar_intervencao(request, pk):
    intervencao = get_object_or_404(Intervencao, pk=pk)
    if request.method == "POST":
        form = IntervencaoForm(request.POST, instance=intervencao)
        if form.is_valid():
            intervencao = form.save(commit=False)
            intervencao.updated_by = request.user  # Define quem editou a intervenção
            intervencao.updated_at = timezone.now()  # Atualiza a data/hora da edição
            intervencao.save()
            return redirect('detalhes_equipamento', pk=intervencao.equipamento.id)
    else:
        form = IntervencaoForm(instance=intervencao)
    
    return render(request, 'intervencoes/form.html', {'form': form, 'equipamento': intervencao.equipamento})

@login_required
def excluir_intervencao(request, pk):
    intervencao = get_object_or_404(Intervencao, pk=pk)
    equipamento = intervencao.equipamento
    if request.method == "POST":
        intervencao.delete()
        
        # Atualizar status do equipamento se necessário
        if not equipamento.intervencao_set.exists():  # Se não houver mais intervenções
            equipamento.status = "Disponível"  # Ou outro status adequado
            equipamento.updated_by = request.user
            equipamento.updated_at = timezone.now()
            equipamento.save()

        return redirect('detalhes_equipamento', pk=equipamento.id)
    
    return render(request, 'intervencoes/confirmar_exclusao.html', {'intervencao': intervencao})


# Lista de técnicos
def lista_tecnicos(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'tecnicos/lista.html', {'tecnicos': tecnicos})


# Detalhes do técnico
@login_required
def detalhes_tecnico(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    return render(request, 'tecnicos/detalhes.html', {'tecnico': tecnico})


# Criar ou editar técnico
@login_required
def criar_tecnico(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tecnicos')
    else:
        form = TecnicoForm()
    return render(request, 'tecnicos/form.html', {'form': form})

@login_required
def editar_tecnico(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    if request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            return redirect('detalhes_tecnico', pk=tecnico.pk)
    else:
        form = TecnicoForm(instance=tecnico)
    return render(request, 'tecnicos/form.html', {'form': form})

# Excluir técnico
@login_required
def excluir_tecnico(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    if request.method == 'POST':
        tecnico.delete()
        return redirect('lista_tecnicos')
    return render(request, 'tecnicos/confirmar_exclusao.html', {'tecnico': tecnico})


@login_required
def alterar_status(request, pk):
    equipamento = get_object_or_404(Equipamento, pk=pk)

    if request.method == 'POST':
        # Define o status diretamente como "Reparado"
        equipamento.status = "Reparado"
        equipamento.save()

        return redirect('detalhes_equipamento', pk=equipamento.pk)
    
    return HttpResponse(status=405)

@login_required
def entregar_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, pk=equipamento_id)

    if request.method == 'POST':
        # Define o status como "Entregue"
        equipamento.status = "Entregue"
        equipamento.save()

    return redirect('lista_equipamentos')  # Redireciona de volta para a lista



def relatorios(request):
    # Relatório de número de intervenções e tempo total por técnico (em minutos)
    intervencao_por_tecnico = Intervencao.objects.values('tecnico__nome').annotate(
        num_intervencoes=Count('id'),
        tempo_total=Sum(
            ExpressionWrapper(
                F('hora_fim') - F('hora_inicio'),
                output_field=DurationField()
            )
        )
    )

    # Calculando a duração total em minutos após obter o resultado
    for tecnico in intervencao_por_tecnico:
        total_duration = tecnico['tempo_total']
        if total_duration:
            # Extrair os minutos diretamente
            total_seconds = total_duration.total_seconds()
            tecnico['tempo_total_minutos'] = total_seconds // 60  # Converte segundos em minutos

    # Relatório de número de equipamentos por estado
    equipamentos_por_estado = Equipamento.objects.values('status').annotate(
        num_equipamentos=Count('id')
    ).order_by('-num_equipamentos')

    return render(request, 'relatorios.html', {
        'intervencao_por_tecnico': intervencao_por_tecnico,
        'equipamentos_por_estado': equipamentos_por_estado,
    })