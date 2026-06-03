from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re

from .models import Solicitacao


def validar_pdf(arquivo):

    if not arquivo:
        return

    extensao = arquivo.name.split('.')[-1].lower()

    if extensao != 'pdf':
        raise ValidationError(
            'Somente arquivos PDF são permitidos.'
        )


class SolicitacaoForm(forms.ModelForm):

    class Meta:

        model = Solicitacao

        exclude = [
            'status',
            'parecer_operacional',
            'aprovado_por',
            'data_aprovacao',
            'protocolo',
            'usuario',
            'assinado_por',
            'data_assinatura',
            'criado_em'
        ]

        widgets = {

            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'maxlength': '14'
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(99) 99999-9999',
                'maxlength': '15'
            }),

            'data_evento': forms.DateInput(attrs={
                'type': 'date'
            }),

            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time'
            }),

            'hora_fim': forms.TimeInput(attrs={
                'type': 'time'
            }),
        }

    def clean_telefone(self):

        telefone = self.cleaned_data.get('telefone')

        padrao = r'^\(\d{2}\)\s\d{5}-\d{4}$'

        if not re.match(padrao, telefone):

            raise forms.ValidationError(
                'Telefone inválido. Use (99) 99999-9999'
            )

        return telefone

    def clean_cpf(self):

        cpf = self.cleaned_data.get('cpf')

        cpf = re.sub(r'[^0-9]', '', cpf)

        if len(cpf) != 11:
            raise forms.ValidationError(
                'CPF inválido.'
            )

        if cpf == cpf[0] * 11:
            raise forms.ValidationError(
                'CPF inválido.'
            )

        soma = 0

        for i in range(9):
            soma += int(cpf[i]) * (10 - i)

        digito = (soma * 10) % 11

        if digito == 10:
            digito = 0

        if digito != int(cpf[9]):
            raise forms.ValidationError(
                'CPF inválido.'
            )

        soma = 0

        for i in range(10):
            soma += int(cpf[i]) * (11 - i)

        digito = (soma * 10) % 11

        if digito == 10:
            digito = 0

        if digito != int(cpf[10]):
            raise forms.ValidationError(
                'CPF inválido.'
            )

        return cpf

    def clean_data_evento(self):

        data_evento = self.cleaned_data.get(
            'data_evento'
        )

        limite = timezone.now().date() + timedelta(days=3)

        if data_evento < limite:

            raise forms.ValidationError(
                'O evento deve ser solicitado com pelo menos 72 horas de antecedência.'
            )

        return data_evento

    def clean(self):

        cleaned_data = super().clean()

        publico = cleaned_data.get(
            'publico_estimado'
        )

        prefeitura = cleaned_data.get(
            'oficio_prefeitura'
        )

        bombeiro = cleaned_data.get(
            'oficio_bombeiro'
        )

        if not prefeitura:

            raise forms.ValidationError(
                'O Documento Sanitário é obrigatório.'
            )

        if publico and publico > 2000 and not bombeiro:

            raise forms.ValidationError(
                'Eventos acima de 2000 pessoas precisam do documento do Corpo de Bombeiros.'
            )

        return cleaned_data

    def clean_oficio_prefeitura(self):

        arquivo = self.cleaned_data.get(
            'oficio_prefeitura'
        )

        if arquivo:
            validar_pdf(arquivo)

        return arquivo

    def clean_oficio_bombeiro(self):

        arquivo = self.cleaned_data.get(
            'oficio_bombeiro'
        )

        if arquivo:
            validar_pdf(arquivo)

        return arquivo