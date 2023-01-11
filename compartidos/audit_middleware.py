from apps.backoffice.models import AuditModel
from django.contrib.gis.geos import Point


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        method = request.method
        user = request.user
        headers = request.headers
        location = headers["Location"]

        point_location = Point(float(location.split(",")[0]), float(location.split(",")[1]))

        user_id = None

        if user.is_authenticated:
            user_id = user.id

        response = self.get_response(request)

        try:
            response_data = response.data
        except AttributeError:
            response_data = None

        AuditModel.objects.create(
            request_method=method,
            created_by_id=user_id,
            table_modified="",
            columns_modified="",
            row_modified=None,
            location=point_location
        )

        print(method, user_id, response_data)

        return response
