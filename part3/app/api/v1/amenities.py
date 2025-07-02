from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(
        required=True,
        description='Name of the amenity'
        )
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        # Trust no one
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            return {'error': 'Admin privileges required.'}, 403

        amenity_data = api.payload
        try:
            amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {
            'id': amenity.id,
            'name': amenity.name
            }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = []
        for amenity in facade.get_all_amenities():
            amenities.append(
                {
                    'id': amenity.id,
                    'name': amenity.name
                })
        return amenities, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found.'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
            }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            return {'error': 'Admin privileges required.'}, 403

        amenity_data = api.payload
        if facade.get_amenity(amenity_id) is None:
            return {'error': 'Amenity not found.'}, 404

        try:
            facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'message': 'Amenity updated successfully.'}, 200

    @api.response(204, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity"""
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            return {'error': 'Admin privileges required.'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found.'}, 404
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully.'}, 204
