from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from django.conf import settings

page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

desc_available_operators_dates = 'Available operators: gt, gte, lt, lte. Without operator the comparation is equal to. Format: yyyy-mm-dd'
desc_available_operators_text = 'Available operators: contains, icontains, exact, iexact, in, startswith, istartswith, endswith, iendswith. Without operator the comparation is equal to.'
desc_available_operators_numbers = 'Available operators: gt, gte, lt, lte. Without operator the comparation is equal to.'
desc_available_operators_in = 'Available operators: in.'

schema_authorization = [
    OpenApiParameter(
        name='Authorization',
        location=OpenApiParameter.HEADER,
        description='The structure to authenticate is: "JWT " + idToken)',
        required=True,
        type=OpenApiTypes.STR
    ),
]

schema_locale = [
    OpenApiParameter(
        name='Accept-Language',
        location=OpenApiParameter.HEADER,
        description=f'Example: Accept-Language=pt-PT.',
        required=True,
        type=OpenApiTypes.STR
    ),
]

schema_software_type = [
    OpenApiParameter(
        name='Software-Type',
        location=OpenApiParameter.HEADER,
        description=f'Options are: Web or Application. Example: Software-Type=Web.',
        required=True,
        type=OpenApiTypes.STR
    ),
]

schema_sort_by = [
    OpenApiParameter(
        name='sort_by',
        location=OpenApiParameter.QUERY,
        description='Sort the queries. Example: sort_by=asc[field_name] or sort_by=asc[field_name_1],desc[field_name_2]',
        required=False,
        type=OpenApiTypes.STR
    ),
]

schema_pagination = [
    OpenApiParameter(
        name='page',
        location=OpenApiParameter.QUERY,
        description=f'Get {page_size} elements for the asked page.',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='page_size',
        location=OpenApiParameter.QUERY,
        description='A numeric value indicating the page size. If set, this overrides the default PAGE_SIZE setting.',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='offset',
        location=OpenApiParameter.QUERY,
        description='The offset indicates the starting position of the query in relation to the complete set of unpaginated items.',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='limit',
        location=OpenApiParameter.QUERY,
        description='The limit indicates the maximum number of items to return',
        required=False,
        type=OpenApiTypes.INT
    ),
]

schema_show_time = [
    OpenApiParameter(
        name='start_date[operator]',
        location=OpenApiParameter.QUERY,
        description=f'Show object after this date. {desc_available_operators_dates}',
        required=False,
        type=OpenApiTypes.DATE
    ),
    OpenApiParameter(
        name='end_date[operator]',
        location=OpenApiParameter.QUERY,
        description=f'Hide object after this date. {desc_available_operators_dates}',
        required=False,
        type=OpenApiTypes.DATE
    ),
]

schema_status = [
    OpenApiParameter(
        name='status',
        location=OpenApiParameter.QUERY,
        description=f'Status of the object. Possible options: 0 -> Invisible; 1 -> Visibile; 2 -> Inactive; 3 -> Deleted;',
        required=False,
        type=OpenApiTypes.INT
    ),
]

schema_hero = [
    OpenApiParameter(
        name='hero',
        location=OpenApiParameter.QUERY,
        required=False,
        type=OpenApiTypes.BOOL
    ),
]

# All schemas
schema_lists = schema_sort_by + schema_authorization + schema_pagination
schema_lists += schema_show_time + schema_status + schema_locale
schema_lists += schema_software_type + schema_hero
