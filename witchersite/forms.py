from .models import StartData, Action
from django.forms import ModelForm, NumberInput
from django import forms


class StartDataForm(ModelForm):
    class Meta:
        model = StartData
        fields = ['witcher_level', 'enemy_level', 'enemy_amount']

        widgets = {

            'witcher_level': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Уровень Ведьмака'}),
            'enemy_level': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Уровень Противников'}),
            'enemy_amount': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество Противников'}),

        }


class ActionForm(ModelForm):
    class Meta:
        model = Action
        fields = ['action']

        widgets = {'action': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Выберите действие',
                                                'id': 'action'})}
