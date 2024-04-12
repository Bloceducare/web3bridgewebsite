from rest_framework import response
from django.http import JsonResponse
from utils.exceptions.requests import QuerySetException

class Utils:
    @staticmethod
    def get_object_or_raise_error(class_, *args, **kwargs):
        queryset= Utils._get_queryset(class_)

        if not hasattr(queryset, "get"):
            class_name= (class_.__name__ if isinstance(class_, type) else class_.__class__.__name__)
            raise ValueError(f"First arguement to get_object_or_raise_error() must be a Model or Manager or Queryset not {class_name}")

        try:
            queryset.get(*args, **kwargs)    
        except queryset.model.DoesNotExist:
            raise QuerySetException(["Queryset error"], f"No {queryset.model._meta.object_name} matches the given query") 

    @staticmethod
    def _get_queryset(class_):
        # If it is a model class or anything else with ._default_manager
        if hasattr(class_, "_default_manager"):
            return class_._default_manager.all()
        return class_
    
    @staticmethod
    def success_response(data, http_status):
        return JsonResponse(
            {"success": True,
             "data": data}, status=http_status)
    
    @staticmethod
    def error_response(message, errors, http_status):
        return JsonResponse(
            {"success": False,
            "message": message,
            "errors": errors}, status=http_status)