from neomodel import StructuredNode, StringProperty, RelationshipTo


class TrailJunction(StructuredNode):
    unique_id = StringProperty(unique_index=True)


class TrailSegment(StructuredNode):
    unique_id = StringProperty(unique_index=True)
    start_junction = RelationshipTo('TrailJunction', 'STARTS')
    end_junction = RelationshipTo('TrailJunction', 'ENDS')