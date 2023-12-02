"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200

class Brevet(Resource):
    def get(self, id):
        brevet = Brevet.objects.get(id=id).to_json()
        return Response(brevet, mimetype="application/json", status=200)

    def put(self, id):
        input_json = request.json
        Brevet.objects.get(id=id).update(**input_json)
        return '', 200

    def delete(self, id):
        Brevet.objects.get(id=id).delete()
        return '', 200 