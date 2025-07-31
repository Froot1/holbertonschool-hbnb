from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services import facade


api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(
        description='Amenity ID'
        ),
    'name': fields.String(
        description='Name of the amenity'
        )
})

user_model = api.model('PlaceUser', {
    'id': fields.String(
        description='User ID'
        ),
    'first_name': fields.String(
        description='First name of the owner'
        ),
    'last_name': fields.String(
        description='Last name of the owner'
        ),
    'email': fields.String(
        description='Email of the owner'
        )
})

review_model = api.model('PlaceReview', {
    'id': fields.String(
        description='Review ID'
        ),
    'text': fields.String(
        description='Text of the review'
        ),
    'rating': fields.Integer(
        description='Rating of the place (1-5)'
        ),
    'user_id': fields.String(
        description='ID of the user'
        )
})

place_model = api.model('Place', {
    'title': fields.String(
        required=True,
        description='Title of the place'
        ),
    'description': fields.String(
        description='Description of the place'
        ),
    'price': fields.Float(
        required=True,
        description='Price per night'
        ),
    'latitude': fields.Float(
        required=True,
        description='Latitude of the place'
        ),
    'longitude': fields.Float(
        required=True,
        description='Longitude of the place'
        ),
    'owner_id': fields.String(
        required=True,
        description='ID of the owner'
        ),
    'amenities': fields.List(
        fields.Nested(amenity_model),
        description='List of amenities'
        ),
    'reviews': fields.List(
        fields.Nested(review_model),
        description='List of reviews'
        )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        place_data = api.payload
        user = facade.get_user(place_data.get('owner_id'))
        if user is None:
            return {'error': 'Invalid owner_id.'}, 400

        if not (claims.get('is_admin') is True or current_user_id == user.id):
            return {'error': 'Unauthorized action.'}, 403

        if place_data.get('amenities'):
            amenity_instances = []
            for amenity in place_data.get('amenities'):
                amenity_instance = facade.get_amenity(amenity['id'])
                if amenity_instance is None:
                    return {'error': 'Invalid amenity ID.'}, 400
                amenity_instances.append(amenity_instance)
            place_data['amenities'] = amenity_instances

        # Remove 'reviews' from place_data if present, as reviews should not be set on creation
        if 'reviews' in place_data:
            del place_data['reviews']

        try:
            place = facade.create_place(place_data)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': int(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner_id,
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = []
        for place in facade.get_all_places():
            places.append({
                'id': place.id,
                'name': place.title,
                'description': place.description,
                'price_by_night': int(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude
                })
        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place:
            owner = facade.get_user(place.owner_id)
            # Fetch reviews for this place
            reviews = facade.get_reviews_by_place(place_id)
            reviews_list = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                } for review in reviews
            ]
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': str(place.price),
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                } if owner else None,
                'amenities': [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    } for amenity in place.amenities
                ],
                'reviews': reviews_list
            }, 200
        return {'error': 'Place not found.'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if place is None:
            return {'error': 'Place not found.'}, 404

        place_data = api.payload
        for key in place_data:
            if key not in ['title',
                           'price',
                           'description',
                           'latitude',
                           'longitude',
                           'owner_id',
                           'amenities',
                           'reviews']:
                return {'error': f"Invalid input data: '{key}' is not allowed."}, 400

        # Remove 'reviews' from place_data before update to avoid SQLAlchemy error
        if 'reviews' in place_data:
            del place_data['reviews']

        # Convert amenities dicts to Amenity instances if present
        if place_data.get('amenities'):
            amenity_instances = []
            for amenity in place_data.get('amenities'):
                amenity_instance = facade.get_amenity(amenity['id'])
                if amenity_instance is None:
                    return {'error': 'Invalid amenity ID.'}, 400
                amenity_instances.append(amenity_instance)
            place_data['amenities'] = amenity_instances

        # Trust no one
        claims = get_jwt()
        if claims.get('is_admin') is True:
            is_admin = facade.get_user(current_user_id).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            user = facade.get_user(place_data.get('owner_id'))
            if user is None:
                return {'error': 'Invalid owner_id.'}, 400

            is_admin = facade.get_user(current_user_id).is_admin
            if not is_admin and current_user_id != user.id:
                return {'error': 'Unauthorized action.'}, 403

            if place_data is place:
                return {'error': 'Invalid input data.'}, 400

            if place_data.get('amenities'):
                for amenity in place_data.get('amenities'):
                    if facade.get_amenity(amenity['id']) is None:
                        return {'error': 'Invalid amenity ID.'}, 400

        try:
            facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'message': 'Place updated successfully.'}, 200

    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user or not user.is_admin:
            return {'error': 'Admin privileges required.'}, 403

        place = facade.get_place(place_id)
        if place is None:
            return {'error': 'Place not found.'}, 404

        facade.delete_place(place_id)
        return {'message': 'Place successfully deleted.'}, 200
