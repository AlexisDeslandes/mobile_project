from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import flask
import json
import MySQLdb
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)
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

class ArticlesPositions(Resource):
    def get(self):
        db = DB()
        cur = db.query("SELECT * FROM ceihm_articles;")
        json_output = []
        for row in cur.fetchall():
            json_output.append({"id":row[0],"nom":row[1], "position":str(row[2])+":"+str(row[5])})
        return json_output

class Process(Resource):
    def post(self):
        global allPaths
        db = DB()
        data = request.get_json()
        articles = []
        token = ""
        articles = [1] + data['articles']
        if data['token']:
            token = data['token']
        if token == "wakandaforeva":
            graph = []
            for article in articles:
                cur = db.query("SELECT * FROM distances WHERE startId = '"+ str(article) +"' OR endId = '"+ str(article) + "';");
                for row in cur.fetchall():
                    graph.append({"startId":row[1], "endId":row[2], "distance":row[3]})
            path = shortest(articles, clean_graph(articles, graph))
            path_with_names = []
            for article in path:
                cur = db.query("SELECT nom FROM articles WHERE id = "+ str(article) +";")
                for row in cur.fetchall():
                    path_with_names.append({"id": article, "nom":row[0]})
            return path_with_names



class Distances(Resource):
    def post(self):
        db = DB()
        data = request.get_json()
        distances = []
        token = ""
        if data['distances']:
            distances = data['distances']
        if data['token']:
            token = data['token']
        if token == "wakandaforeva":
            for obj_distance in distances:
                startId = obj_distance['startId']
                endId = obj_distance['endId']
                distance = obj_distance['distance']
                db.query("INSERT INTO distances (startId, endId, distance) VALUES ("+str(startId)+", "+str(endId)+", "+str(distance)+");")
                db.commit()
            return {"status": 200}
        else:
            return {"status": 400}
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


def clean_graph(articles, graph):
    new_graph = []
    processed = []
    for article in articles:
        edges = {}
        for distance in graph:
            if distance['startId'] in articles and distance['endId'] in articles:
                if distance['startId'] == article and distance['endId'] not in processed:
                    if distance['endId'] not in edges.keys():
                        edges[distance['endId']] = [distance['distance']]
                    else:
                        edges[distance['endId']].append(distance['distance'])
                elif distance['endId'] == article and distance['startId'] not in processed:
                    if distance['startId'] not in edges.keys():
                        edges[distance['startId']] = [distance['distance']]
                    else:
                        edges[distance['startId']].append(distance['distance'])
        for other_article,distances in edges.items():
            new_graph.append({"startId":article, "endId":other_article, "distance":average(distances)})
        processed.append(article)
    return new_graph


def average(list):
    if len(list) > 0:
        avg = 0
        for item in list:
            avg += int(item)
        avg /= len(list)
        variance = 0
        for item in list:
            variance += (item-avg)**2
        variance /= len(list)
        sigma = math.sqrt(variance)
        new_avg = 0
        count = 0
        for item in list:
            if int(item) < avg+sigma and int(item) > avg-sigma:
                new_avg += int(item)
                count += 1
        if count == 0:
            return avg
        new_avg /= count
        return new_avg
    return -1

class Test(Resource):
    def get(self):
        data = [7, 8, 39, 40, 40, 42, 42, 43, 50]
        return average(data)

def shortest(articles, graph):
    current_article = 1 # Entrée
    processed = [1]
    while len(processed) < len(articles):
        min_dist = 99999999
        min_article = 0
        for article in articles:
            if article not in processed:
                distance = get_distance(current_article, article, graph)
                if distance != None and distance < min_dist:
                    min_dist = distance
                    min_article = article
        processed.append(min_article)
        current_article = min_article
    if 0 in processed:
        processed.remove(0)
    return processed


def browse_graph(articles, graph, processed, totalDistance):
    if len(processed) == len(articles):
        allPaths.append(processed)
    for article in articles:
        if len(processed) > 0:
            totalDistance += get_distance(article, processed[-1], graph)
        processed.append(articles)
        browse_graph(articles, graph, processed, totalDistance)

def get_distance(n1, n2, graph):
    for edge in graph:
        if (int(edge['startId']) == int(n1) and int(edge['endId']) == int(n2)) or (int(edge['startId']) == int(n2) and int(edge['endId']) == int(n1)):
            return edge['distance']



api.add_resource(HelloWorld, '/') # GET
api.add_resource(Articles, '/articles') # GET
api.add_resource(ArticlesPositions, '/articlespositions') #GET
api.add_resource(Distances, '/distances') # POST
api.add_resource(Process, '/process') # POST
api.add_resource(Test, '/test') # GET

if __name__ == '__main__':
     app.run(port='5002')





