from flask_restx import Namespace, Resource, fields

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
        )
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        user = facade.get_user_by_email(user_data['email'])
        if user:
            return {'error': 'Email already registered'}, 400

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
            users.append(
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
                )
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
        return {'error': 'User not found'}, 404

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if user == facade.get_user(user_id):
            return {'error': 'No changes detected'}, 400

        if user.email != user_data['email']:
            user = facade.get_user_by_email(user_data['email'])
            if user:
                return {'error': 'Email already registered'}, 400

        try:
            facade.update_user(user_id, user_data)
        except Exception as e:
            return {'error': str(e)}, 400

        user = facade.get_user(user_id)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200
