from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade


api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description='Text of the review'
        ),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
        ),
    'user_id': fields.String(
        required=True,
        description='ID of the user'
        ),
    'place_id': fields.String(
        required=True,
        description='ID of the place'
        )
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            if current_user['id'] != review_data['user_id']:
                return {'error': 'You cannot review your own place.'}, 400

        place = facade.get_place(review_data['place_id'])
        if place is None:
            return {'error': 'Invalid place_id.'}, 400

        user = facade.get_user(review_data['user_id'])
        if user is None:
            return {'error': 'Invalid user_id.'}, 400

        if user.id in [review.user_id for review in place.reviews]:
            return {'error': 'You have already reviewed this place.'}, 400

        if current_user['id'] != place.owner_id:
            return {'error': 'Unauthorized action.'}, 403

        try:
            review = facade.create_review(review_data)
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
                }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = []
        for review in facade.get_all_reviews():
            reviews.append({
                "id": review.id,
                "text": review.text,
                "rating": review.rating
                })
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
                }, 200
        return {'error': 'Review not found.'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review_data = api.payload
        for key in review_data:
            if key not in ['text', 'rating', 'user_id', 'place_id']:
                return {'error': 'Invalid input data.'}, 400

        if current_user['id'] != review_data['user_id']:
            return {'error': 'Invalid input data.'}, 400

        review = facade.get_reviews_by_place(review_data['place_id'])
        if review.owner_id != current_user['id']:
            return {'error': 'Unauthorized action.'}, 403

        if review_data is facade.get_review(review_id):
            return {'error': 'Invalid input data.'}, 400

        try:
            facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'message': 'Review updated successfully.'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # Trust no one
        current_user = get_jwt_identity()
        if current_user.get('is_admin') is True:
            is_admin = facade.get_user(current_user['id']).is_admin
            if not is_admin:
                return {'error': 'Admin privileges required.'}, 403
        else:
            return {'error': 'Admin privileges required.'}, 403

        if facade.get_review(review_id):
            place = facade.get_place(review_id)
            if place:
                place.remove_review(review_id)
            facade.delete_review(review_id)
            return {'error': 'Review deleted successfully.'}, 200
        return {'error': 'Review not found.'}, 404
