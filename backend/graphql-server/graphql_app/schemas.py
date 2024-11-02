import graphene
from graphene import relay
from .models import TrailJunction, TrailSegment


class TrailJunctionType(graphene.ObjectType):
    unique_id = graphene.String()


class TrailSegmentType(graphene.ObjectType):
    unique_id = graphene.String()
    start_junction = graphene.Field(TrailJunctionType)
    end_junction = graphene.Field(TrailJunctionType)


class Query(graphene.ObjectType):
    all_junctions = graphene.List(TrailJunctionType)
    all_segments = graphene.List(TrailSegmentType)

    def resolve_all_junctions(self, info):
        return TrailJunction.nodes.all()

    def resolve_all_segments(self, info):
        return TrailSegment.nodes.all() 


schema = graphene.Schema(query=Query)