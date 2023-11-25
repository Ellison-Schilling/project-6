"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one


class Brevets(Resource):
    def get(self):
        json_object = Brevets.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json

        ## Because input_json is a dictionary, we can do this:
        #distance = input_json["distance"] # Should be a string
        #date_time = input_json["date_time"] # Should be a string
        #checkpoints = input_json["checkpoints"] # Should be a list of dictionaries
        #result = Brevet(distance=distance, date_time=date_time, checkpoints=checkpoints).save()

        result = Brevets(**input_json).save()
        return {'_id': str(result.id)}, 200