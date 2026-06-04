from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
import os   
from reportlab.pdfgen import canvas
from .models import Solicitacao
from .forms import SolicitacaoForm
from django.http import HttpResponse
import traceback
from django.shortcuts import render

def nova_solicitacao(request):

    if request.method == 'POST':

        form = SolicitacaoForm(request.POST, request.FILES)

        if form.is_valid():

            try:

                solicitacao = form.save(commit=False)
                solicitacao.status = 'PENDENTE'
                solicitacao.save()

                send_mail(
                    'Solicitação Recebida',
                    'Teste',
                    settings.DEFAULT_FROM_EMAIL,
                    [solicitacao.email],
                    fail_silently=False
                )

                return render(
                    request,
                    'solicitacoes/sucesso.html',
                    {'protocolo': solicitacao.protocolo}
                )

            except Exception as e:

                erro = traceback.format_exc()

                return HttpResponse(
                    f"<pre>{erro}</pre>"
                )

        else:

            return HttpResponse(
                str(form.errors)
            )

    form = SolicitacaoForm()

    return render(
        request,
        'solicitacoes/nova.html',
        {'form': form}
    )
    

def home(request):
    return render(request, 'home.html')