from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
        ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
        ),
    'email': fields.String(
        required=True,
        description='Email of the user'
        ),
    'password': fields.String(
        required=True,
        description='Password of the user'
        )
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user"""
        # Trust no one
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            return {'error': 'Admin privileges required.'}, 403

        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered.'}, 400

        try:
            user = facade.create_user(user_data)
        except Exception as e:
            return {'error': str(e)}, 400
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = []
        for user in facade.get_all_users():
            users.append({
                 'id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email
                 })
        return users, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if user:
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                }, 200
        return {'error': 'User not found.'}, 404

    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        for key in user_data:
            if key not in ['first_name', 'last_name', 'email', 'password']:
                return {'error': 'Invalid input data.'}, 400

        # Trust no one
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403

            if user_data.get('email'):
                if facade.get_user_by_email(user_data['email']):
                    return {'error': 'Email already registered.'}, 400
        else:
            if user_data.get('email') or user_data.get('password'):
                return {'error': 'You cannot modify email or password.'}, 403

            if current_user['id'] != user_id:
                return {'error': 'Unauthorized action.'}, 403

        if not facade.get_user(user_id):
            return {'error': 'User not found.'}, 404

        try:
            facade.update_user(user_id, user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        return self.get(user_id)

    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, user_id):
        """Delete user"""
        # Trust no one
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            if current_user['id'] != user_id:
                return {'error': 'Unauthorized action.'}, 403

        if not facade.get_user(user_id):
            return {'error': 'User not found.'}, 404

        try:
            facade.delete_user(user_id)
        except Exception as e:
            return {'error': str(e)}, 400

        return {'message': 'User successfully deleted.'}, 200
