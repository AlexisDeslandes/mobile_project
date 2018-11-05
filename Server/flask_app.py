from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import flask
import json
import MySQLdb

app = Flask(__name__)
api = Api(app)

class DB:
  conn = None

  def connect(self):
    self.conn = MySQLdb.connect(host="renaudcosta.mysql.pythonanywhere-services.com", user="renaudcosta", passwd="elimelimelim", db="renaudcosta$podocollect")

  def query(self, sql):
    try:
      cursor = self.conn.cursor()
      cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute(sql)
    return cursor

  def commit(self):
      self.conn.commit()

class Articles(Resource):
    def get(self):
        db = DB()
        cur = db.query("SELECT * FROM articles;")
        json_output = []
        for row in cur.fetchall():
            json_output.append({"id":row[0],"nom":row[1]})
        return json_output

class Distances(Resource):
    def post(self):
        db = DB()
        distances = request.get_json()
        for obj_distance in distances:
            startId = obj_distance['startId']
            endId = obj_distance['endId']
            distance = obj_distance['distance']
            db.query("INSERT INTO distances (startId, endId, distance) VALUES ("+str(startId)+", "+str(endId)+", "+str(distance)+");")
            db.commit()
        return {"status": 200}
    def get(self):
        db = DB()
        cur = db.query("SELECT * FROM distances;")
        json_output = []
        for row in cur.fetchall():
            json_output.append({"id":row[0],"startId":row[1],"endId":row[2],"distance":row[3]})
        return json_output

class HelloWorld(Resource):
    def get(self):
        return {"Hello":"World"}

api.add_resource(HelloWorld, '/') # GET
api.add_resource(Articles, '/articles') # GET
api.add_resource(Distances, '/distances') # POST

if __name__ == '__main__':
     app.run(port='5002')





