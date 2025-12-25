from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth.models import  User
from django.contrib.auth import  get_user_model
from rest_framework import status

from .models import ResearchSession
from .tasks import run_research_task


User = get_user_model()

# Create your views here.

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class StartResearchView(APIView):
    def post(self, request):
        query = request.data.get("query")

        if not query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.order_by("id").first()
        if  not user:
            return Response(
                {"error": "No users available to associate with the research session."},
                status=status.HTTP_400_BAD_REQUEST
            ) 

        research = ResearchSession.objects.create(
            user=user,
            query=query,
            status='PENDING'
        )

        run_research_task.delay(research.id)

        return Response(
            {
                "research_id": research.id,
                "status": research.status
            },
            status=status.HTTP_201_CREATED
        )