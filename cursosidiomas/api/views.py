from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from ..models import Curso, Aluno

from cursosidiomas.models import Curso, Aluno, Professor, Aula, Certificado, Tutoria

from cursosidiomas.api.serializers import CursoSerializer, AlunoSerializer, ProfessorSerializer, AulaSerializer, CertificadoSerializer, TutoriaSerializer

class CursoViewSet(ModelViewSet):
    serializer_class = CursoSerializer
    queryset = Curso.objects.all()

    @action(detail=False, methods=['post'], url_path='inscrever')
    def inscrever_aluno(self, request):
        curso_id = request.data.get("curso_id")
        aluno_id = request.data.get("aluno_id")

        # Validar se ambos os IDs foram enviados
        if not curso_id or not aluno_id:
            return Response(
                {"detail": "Os campos 'curso_id' e 'aluno_id' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            curso = Curso.objects.get(pk=curso_id)
            aluno = Aluno.objects.get(pk=aluno_id)

            # Verificar se o aluno já está inscrito
            if curso.alunos.filter(id=aluno.id).exists():
                return Response({"detail": "Aluno já está inscrito neste curso."}, status=status.HTTP_200_OK)

            # Verificar se o curso tem vagas disponíveis (caso haja limite)
            vagas_maximas = 100  # Defina um limite, se necessário
            if curso.alunos.count() >= vagas_maximas:
                return Response({"detail": "Não há mais vagas disponíveis neste curso."}, status=status.HTTP_400_BAD_REQUEST)

            # Inscrever o aluno no curso
            curso.alunos.add(aluno)
            return Response({"detail": "Inscrição concluída com sucesso."}, status=status.HTTP_201_CREATED)

        except Curso.DoesNotExist:
            return Response({"detail": "Curso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Aluno.DoesNotExist:
            return Response({"detail": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"detail": "Erro durante a inscrição. Tente novamente.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AlunoViewSet(ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class ProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class AulaViewSet(ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

class CertificadoViewSet(ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer

class TutoriaViewSet(ModelViewSet):
    queryset = Tutoria.objects.all()
    serializer_class = TutoriaSerializer

