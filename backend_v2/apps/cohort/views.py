from rest_framework import decorators, response, status, viewsets
from . import serializers, models

class CouresViewSet(viewsets.ViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    
    def get_required_fields(self):
        if self.action == "all":
            return ["name", "description", "venue", "extra_info", "images"]
    
    @decorators.action(detail=False, methods=["post"])
    def create(self, request, *args, **kwargs):
        pass
    
    @decorators.action(detail=False, methods=["get"])
    def all(self):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return response.Responsestatus(status.HTTP_200_OK, data=serializer.data())
    
    @decorators.action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        pass
    
    @decorators.action(detail=False, methods=["put"])
    def edit(self, request, *args, **kwargs):
        pass
    
    @decorators.action(detail=False, methods=["delete"])
    def delete(self, request, *args, **kwargs):
        pass

    
class RegistrationViewSet(viewsets.ViewSet):
    pass

class ParticipantViewSet(viewsets.ViewSet):
    pass

class TestimonialViewSet(viewsets.ViewSet):
    pass