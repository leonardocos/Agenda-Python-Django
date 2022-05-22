from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    #muda a representação da classe para mostrar no site
    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=255)
    # blank=True - é possível deixar o campo em branco, tornando-o opcional
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    #relaciona as duas tabelas
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    #campo de marcação (Verdadeiro ou Falso)
    mostrar = models.BooleanField(default=True)
    #adicionar campo de imagem
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/%d')

    def __str__(self):
        return self.nome
