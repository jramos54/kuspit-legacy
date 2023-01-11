from drf_yasg import openapi

location_header = openapi.Parameter(
    'location',
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_NUMBER),
    description='Location header',
    required=False,
)
