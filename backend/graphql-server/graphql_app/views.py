from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from .schemas import schema


@csrf_exempt
def graphql_endpoint(request):
    view = GraphQLView.as_view(graphiql=True, schema=schema)
    return view(request)