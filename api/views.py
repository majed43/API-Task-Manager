from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Project, Task
from .serializers import CategorySerializer, ProjectSerializer, TaskSerializer


class CategoryCBV(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(owner=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailCBV(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_category(self, pk, request):
        try:
            return Category.objects.get(pk=pk, owner=request.user)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_category(pk, request)
        if not category:
            return Response(
                {"message": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_category(pk, request)
        if not category:
            return Response(
                {"message": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_category(pk, request)
        if not category:
            return Response(
                {"message": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response("message: Category deleted successfully.")


class ProjectCBV(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(participants=request.user).distinct()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save(owner=request.user)
        project.participants.add(request.user)
        output_serializer = ProjectSerializer(project, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailCBV(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_project(self, request, pk):
        try:
            return Project.objects.get(owner=request.user, pk=pk)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        project = self.get_project(request, pk)
        if not project:
            return Response(
                {"message": "project not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_project(request, pk)
        if not project:
            return Response(
                {"message": "project not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(
            project, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        project = self.get_project(request, pk)
        if not project:
            return Response(
                {"message": "project not found"}, status=status.HTTP_404_NOT_FOUND
            )
        project.delete()
        return Response({"message": "Project deleted successfully."})


class TaskCBV(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(project__participants=request.user).distinct()
        serializer = TaskSerializer(tasks, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailCBV(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_task(self, pk, request):
        try:
            return Task.objects.get(pk=pk, project__participants=request.user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_task(pk, request)
        if not task:
            return Response(
                {"message": "task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(task, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_task(pk, request)
        if not task:
            return Response(
                {"message": "task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(
            task, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        task = self.get_task(pk, request)
        if not task:
            return Response(
                {"message": "task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        task.delete()
        return Response({"message": "Task deleted successfully."})
