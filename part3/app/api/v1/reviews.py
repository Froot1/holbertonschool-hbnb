from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
        user_id = get_jwt_identity()
        review_data = api.payload
        user = facade.get_user(user_id)
        if not (user and user.is_admin):
            if user_id != review_data['user_id']:
                return {'error': 'You cannot review your own place.'}, 400

        place = facade.get_place(review_data['place_id'])
        if place is None:
            return {'error': 'Invalid place_id.'}, 400

        user = facade.get_user(review_data['user_id'])
        if user is None:
            return {'error': 'Invalid user_id.'}, 400

        reviews_for_place = facade.get_reviews_by_place(review_data['place_id'])
        if any(r.user_id == user.id for r in reviews_for_place):
            return {'error': 'You have already reviewed this place.'}, 400

        if user_id == place.owner_id:
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
        user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if review is None:
            return {'error': 'Review not found.'}, 404

        review_data = api.payload
        allowed_keys = ['text', 'rating', 'user_id', 'place_id']
        for key in review_data:
            if key not in allowed_keys:
                return {'error': f"Invalid key in input data: '{key}'"}, 400

        user = facade.get_user(user_id)
        if not (user and user.is_admin):
            if user_id != review_data['user_id']:
                return {'error': f"user_id mismatch: JWT user_id '{user_id}' does not match payload user_id '{review_data['user_id']}'"}, 400

        

        

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
        user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not (user and user.is_admin):
            return {'error': 'Admin privileges required.'}, 403

        if facade.get_review(review_id):
            place = facade.get_place(review_id)
            if place:
                place.remove_review(review_id)
            facade.delete_review(review_id)
            return {'error': 'Review deleted successfully.'}, 200
        return {'error': 'Review not found.'}, 404
