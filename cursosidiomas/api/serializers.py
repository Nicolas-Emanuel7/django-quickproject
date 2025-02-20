from rest_framework import serializers
from cursosidiomas.models import Curso, Aluno, Professor, Aula, Certificado, Tutoria

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"

class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = "__all__"

class CertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = "__all__"

class TutoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutoria
        fields = "__all__"

