from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, senha=None):
        if not email:
            raise ValueError("O usuário deve ter um email válido")
        user = self.model(email=self.normalize_email(email), nome=nome)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, senha):
        user = self.create_user(email, nome, senha)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome

class Aluno(Usuario):
    matricula = models.CharField(max_length=50, unique=True)
    cursos_inscritos = models.ManyToManyField('Curso', related_name='alunos', blank=True)
    aulas_assistidas = models.ManyToManyField('Aula', related_name='alunos_assistiram', blank=True)

class Professor(Usuario):
    cursos_ministrados = models.ManyToManyField('Curso', related_name='professores', blank=True)

class Curso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='cursos')
    idioma = models.CharField(max_length=100)
    duracao = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo

class Aula(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    duracao = models.PositiveIntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='aulas')

    def __str__(self):
        return self.titulo

class Certificado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='certificados')
    curso = models.OneToOneField(Curso, on_delete=models.CASCADE, related_name='certificado')
    data_emissao = models.DateField(auto_now_add=True)

class Tutoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='tutorias_solicitadas')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='tutorias')
    horario = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')])
