
import uuid

from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User



class Solicitacao(models.Model):

    STATUS = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]

    parecer_operacional = models.TextField(
        blank=True,
        null=True
    )

    aprovado_por = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    data_aprovacao = models.DateTimeField(
        blank=True,
        null=True
    )

    protocolo = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nome_evento = models.CharField(
        max_length=200
    )

    solicitante = models.CharField(
        max_length=200
    )

    cpf = models.CharField(
    max_length=14,
    blank=True,
    null=True
    )

    email = models.EmailField()

    telefone = models.CharField(
        max_length=20
    )

    data_evento = models.DateField()

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    local = models.TextField()

    publico_estimado = models.IntegerField()

    observacoes = models.TextField(
        blank=True
    )

    documento_sanitario = models.FileField(
        upload_to='documentos/sanitario/',
        validators=[
        FileExtensionValidator(
            allowed_extensions=['pdf']
        )
    ]
    )

    documento_meio_ambiente = models.FileField(
        upload_to='documentos/meio_ambiente/',
        validators=[
        FileExtensionValidator(
            allowed_extensions=['pdf']
        )
    ]
    )

    oficio_bombeiro = models.FileField(
        upload_to='documentos/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf']
            )
        ]
    )

    documento_pessoal = models.FileField(
        upload_to='documentos/pessoal/',
        blank=True,
        null=True
    )

    assinado_por = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    data_assinatura = models.DateTimeField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDENTE'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.protocolo:

            self.protocolo = str(
                uuid.uuid4()
            )[:8].upper()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.nome_evento