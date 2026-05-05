from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = [
        ('PROSPECCAO', 'Garimpo'),
        ('CONTATO', 'Primeiro Contato'),
        ('BRIEFING', 'Reunião/Briefing'),
        ('PROPOSTA', 'Proposta Enviada'),
        ('FECHADO', 'Contrato Assinado'),
        ('PERDIDO', 'Perdido'),
    ]

    NICHO_CHOICES = [
        ('RESTAURANTE', 'Restaurantes & Lanchonetes'),
        ('ESTETICA', 'Salões & Estética'),
        ('SERVICOS', 'Prestadores de Serviço'),
        ('OUTROS', 'Outros'),
    ]

    nome_cliente = models.CharField(max_length=200)
    nome_empresa = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROSPECCAO')
    nicho = models.CharField(max_length=100, default='Outros')
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    link_google_maps = models.URLField(blank=True)
    ultima_interacao = models.DateTimeField(auto_now=True)
    proximo_contato = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)

    # Diagnóstico Técnico
    tem_site = models.BooleanField(default=False)
    nota_performance = models.IntegerField(null=True, blank=True) # 0-100
    tem_pixel = models.BooleanField(default=False)
    nota_google_meu_negocio = models.FloatField(null=True, blank=True)

    # Integração Google Analytics 4
    ga4_property_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="ID da propriedade do Google Analytics 4 (apenas números, ex: 534388123)"
    )

    def __str__(self):
        return f"{self.nome_cliente} - {self.nome_empresa}"

class Interaction(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interactions')
    data = models.DateTimeField(auto_now_add=True)
    nota = models.TextField()

    def __str__(self):
        return f"Nota para {self.lead.nome_cliente} em {self.data.strftime('%d/%m/%Y')}"

class Task(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_vencimento = models.DateTimeField()
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return f"Tarefa: {self.titulo} ({self.lead.nome_cliente})"

class Project(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, primary_key=True, related_name='project')
    data_inicio = models.DateField(auto_now_add=True)
    link_figma = models.URLField(blank=True)
    link_github = models.URLField(blank=True)
    credenciais_info = models.TextField(blank=True, help_text="Cuidado: Não guarde senhas puras aqui. Use um gestor de senhas.")
    valor_recorrente = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Checklists básicos
    dominio_registrado = models.BooleanField(default=False)
    setup_servidor = models.BooleanField(default=False)
    design_aprovado = models.BooleanField(default=False)
    copywriting_finalizado = models.BooleanField(default=False)
    go_live = models.BooleanField(default=False)

    def __str__(self):
        return f"Projeto: {self.lead.nome_empresa}"
