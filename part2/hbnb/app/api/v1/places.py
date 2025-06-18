from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')

})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid input')
    def post(self):
        data = api.payload
        try:
            place = facade.create_place(data)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner.id
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Places retrieved')
    def get(self):
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'latitude': p.latitude,
                'longitude': p.longitude
            } for p in places
        ], 200

@api.route('/<string:place_id>')
@api.param('place_id', 'Place ID')
class PlaceResource(Resource):
    @api.response(200, 'Place found')
    @api.response(404, 'Not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(404, 'Not found')
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        place = facade.update_place(place_id, api.payload)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'message': 'Place updated successfully'}, 200

