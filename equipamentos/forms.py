from django import forms
from .models import Equipamento, Intervencao, Tecnico
from django.utils.timezone import now


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        #fields = '__all__'        
        fields = ['nome', 'telefone', 'email', 'tipo', 'equipamento', 'marca', 'modelo', 'numero_serie', 'problema', 'outro_equipamento_entregue', 'password', 'permite_abrir_pc', 'permite_apagar_dados', 'data_recepcao', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'equipamento': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'outro_equipamento_entregue': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'permite_abrir_pc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permite_apagar_dados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_recepcao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
class IntervencaoForm(forms.ModelForm):
    class Meta:
        model = Intervencao
        fields = ['tecnico', 'hora_inicio', 'hora_fim', 'descricao']
        widgets = {
            'tecnico': forms.Select(attrs={'class': 'form-control'}),  # Aplica Bootstrap ao dropdown
            'hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),            
            'hora_fim': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fim = cleaned_data.get("hora_fim")

        if hora_inicio and hora_fim:
            if hora_inicio >= hora_fim:
                raise forms.ValidationError("A hora de início deve ser anterior à hora de fim.")

            if hora_fim > now():
                raise forms.ValidationError("A hora de fim não pode ser superior à data/hora atual.")
        
        return cleaned_data

class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = ['nome', 'telefone', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }