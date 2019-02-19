from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import flask
import json
import MySQLdb
from flask_cors import CORS
import math
import random
import sys

app = Flask(__name__)
CORS(app)
api = Api(app)

graph = []

pparent1 = None
pparent2 = None
penfant = None
ptournoi = None
pwinner = None

class DB:
  conn = None

  def connect(self):
    self.conn = MySQLdb.connect(host="renaudcosta.mysql.pythonanywhere-services.com",
                                user="renaudcosta", passwd="elimelimelim", db="renaudcosta$podocollect")

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
            json_output.append({"id": row[0], "nom": row[1]})
        return json_output


class ArticlesPositions(Resource):
    def get(self):
        db = DB()
        cur = db.query("SELECT * FROM ceihm_articles;")
        json_output = []
        for row in cur.fetchall():
            json_output.append(
                {"id": row[0], "nom": row[1], "position": str(row[2])+":"+str(row[5])})
        return json_output


class Process(Resource):
    def post(self):
        global allPaths
        global graph
        global pparent1
        global pparent2
        global penfant
        graph = []
        db = DB()
        data = request.get_json()
        articles = []
        token = ""
        articles = data['articles']
        if data['token']:
            token = data['token']
        if token == "wakandaforeva":
            for article in articles:
                cur = db.query("SELECT * FROM distances WHERE startId = '" +
                               str(article) + "' OR endId = '" + str(article) + "';");
                for row in cur.fetchall():
                    graph.append(
                        {"startId": row[1], "endId": row[2], "distance": row[3]})
            path = genetic(articles, clean_graph(articles, graph))
            path_with_names=[]
            for article in path:
                cur=db.query(
                    "SELECT nom FROM articles WHERE id = " + str(article) + ";")
                for row in cur.fetchall():
                    path_with_names.append({"id": article, "nom": row[0]})
            path_with_names = {"distance":path.getSumDistance(), "articles":path_with_names}

            with open("/home/renaudcosta/trace_algo.txt", "a") as file:
                file.write("Crossover:\n")
                file.write("Parent 1: ")
            pparent1.print_circuit()
            with open("/home/renaudcosta/trace_algo.txt", "a") as file:
                file.write("Parent 2: ")
            pparent2.print_circuit()
            with open("/home/renaudcosta/trace_algo.txt", "a") as file:
                file.write("========> ")
            penfant.print_circuit()

            with open("/home/renaudcosta/trace_algo.txt", "a") as file:
                file.write("\n\n\nTournoi:\n")
            ptournoi.print_population()
            with open("/home/renaudcosta/trace_algo.txt", "a") as file:
                file.write("Gagnant:\n")
            pwinner.print_circuit()

            return path_with_names

class Distances(Resource):
    def post(self):
        db=DB()
        data=request.get_json()
        distances=[]
        token=""
        if data['distances']:
            distances=data['distances']
        if data['token']:
            token=data['token']
        if token == "wakandaforeva":
            for obj_distance in distances:
                startId=obj_distance['startId']
                endId=obj_distance['endId']
                distance=obj_distance['distance']
                db.query("INSERT INTO distances (startId, endId, distance) VALUES (" +
                         str(startId)+", "+str(endId)+", "+str(distance)+");")
                db.commit()
            return {"status": 200}
        else:
            return {"status": 400}
    def get(self):
        db=DB()
        cur=db.query("SELECT * FROM distances;")
        json_output=[]
        for row in cur.fetchall():
            json_output.append(
                {"id": row[0], "startId": row[1], "endId": row[2], "distance": row[3]})
        return json_output

class HelloWorld(Resource):
    def get(self):
        return {"Hello": "World"}


def clean_graph(articles, graph):
    new_graph=[]
    processed=[]
    for article in articles:
        edges={}
        for distance in graph:
            if distance['startId'] in articles and distance['endId'] in articles:
                if distance['startId'] == article and distance['endId'] not in processed:
                    if distance['endId'] not in edges.keys():
                        edges[distance['endId']]=[distance['distance']]
                    else:
                        edges[distance['endId']].append(distance['distance'])
                elif distance['endId'] == article and distance['startId'] not in processed:
                    if distance['startId'] not in edges.keys():
                        edges[distance['startId']]=[distance['distance']]
                    else:
                        edges[distance['startId']].append(distance['distance'])
        for other_article, distances in edges.items():
            new_graph.append(
                {"startId": article, "endId": other_article, "distance": average(distances)})
        processed.append(article)
    return new_graph


def average(list):
    if len(list) > 0:
        avg=0
        for item in list:
            avg += int(item)
        avg /= len(list)
        variance=0
        for item in list:
            variance += (item-avg)**2
        variance /= len(list)
        sigma=math.sqrt(variance)
        new_avg=0
        count=0
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
        return 0

def shortest(articles, graph):
    current_article=1  # Entrée
    processed=[1]
    while len(processed) < len(articles):
        min_dist=99999999
        min_article=0
        for article in articles:
            if article not in processed:
                distance=get_distance(current_article, article, graph)
                if distance != None and distance < min_dist:
                    min_dist=distance
                    min_article=article
        processed.append(min_article)
        current_article=min_article
    if 0 in processed:
        processed.remove(0)
    return processed

def genetic(articles, graph):
    gc = GestionnaireCircuit()
     # Entrée
    gc.ajouterArticle(1)

    for article in articles:
        gc.ajouterArticle(article)

    with open("/home/renaudcosta/trace_algo.txt", "w") as file:
        file.write("")

    pop=Population(gc, 50, True)

    # On fait evoluer notre population sur 100 generations
    ga=GA(gc)
    pop=ga.evoluerPopulation(pop)
    for i in range(0, 25):
        if i == 24:
            pop=ga.evoluerPopulation(pop, True)
        else:
            pop=ga.evoluerPopulation(pop)

    meilleurePopulation=pop.getFittest()

    return meilleurePopulation


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

class GestionnaireCircuit:
   def __init__(self):
       self.articlesDestinations = []

   def ajouterArticle(self, article):
      if article not in self.articlesDestinations:
        self.articlesDestinations.append(article)

   def getArticle(self, index):
      return self.articlesDestinations[index]

   def nombreArticles(self):
      return len(self.articlesDestinations)


class Circuit:
   def __init__(self, gestionnaireCircuit, circuit=None):
      self.gestionnaireCircuit = gestionnaireCircuit
      self.circuit = []
      self.fitness = 0.0
      self.distance = 0
      if circuit is not None:
         self.circuit = circuit
      else:
         for i in range(0, self.gestionnaireCircuit.nombreArticles()):
            self.circuit.append(None)

   def print_circuit(self):
        with open("/home/renaudcosta/trace_algo.txt", "a") as file:
            for articleId in range(len(self.circuit)):
                article = self.circuit[articleId]
                if article != None:
                    if articleId < len(self.circuit)-1:
                        file.write(str(article)+" -> ")
                    else:
                        file.write(str(article))
            file.write("      ("+str(self.getSumDistance())+" pas)\n")

   def __len__(self):
      return len(self.circuit)

   def __getitem__(self, index):
     return self.circuit[index]

   def __setitem__(self, key, value):
     self.circuit[key] = value

   def genererIndividu(self):
     for indiceArticle in range(0, self.gestionnaireCircuit.nombreArticles()):
        self.setArticle(
            indiceArticle, self.gestionnaireCircuit.getArticle(indiceArticle))
     random.shuffle(self.circuit)
     #print(*self.circuit)

   def getArticle(self, circuitPosition):
     return self.circuit[circuitPosition]

   def setArticle(self, circuitPosition, article):
     self.circuit[circuitPosition] = article
     self.fitness = 0.0
     self.distance = 0

   def getFitness(self):
     if self.fitness == 0:
        if(self.circuit[0] != 1):
           self.fitness = 0
        else:
           self.fitness = 1/float(self.getSumDistance())
     return self.fitness

   def getSumDistance(self):
     global graph
     if self.distance == 0:
        circuitDistance = 0
        for indiceArticle in range(0, self.tailleCircuit()):
           articleOrigine = self.getArticle(indiceArticle)
           articleArrivee = None
           if indiceArticle+1 < self.tailleCircuit():
              articleArrivee = self.getArticle(indiceArticle+1)
           else:
              articleArrivee = self.getArticle(0)
           circuitDistance += get_distance(articleOrigine, articleArrivee, graph)
        self.distance = circuitDistance
     return self.distance

   def tailleCircuit(self):
     return len(self.circuit)

   def contientArticle(self, article):
     return article in self.circuit


class Population:
   def __init__(self, gestionnaireCircuit, taillePopulation, init):
      self.circuits = []
      for i in range(0, taillePopulation):
         self.circuits.append(None)

      if init:
         for i in range(0, taillePopulation):
            nouveauCircuit = Circuit(gestionnaireCircuit, None)
            nouveauCircuit.genererIndividu()
            nouveauCircuit.print_circuit()
            self.sauvegarderCircuit(i, nouveauCircuit)
         with open("/home/renaudcosta/trace_algo.txt", "a") as file:
            file.write("\n\n")

   def print_population(self):
       for circuit in self.circuits:
           circuit.print_circuit()
       with open("/home/renaudcosta/trace_algo.txt", "a") as file:
           file.write("\n\n")

   def __setitem__(self, key, value):
      self.circuits[key] = value

   def __getitem__(self, index):
      return self.circuits[index]

   def sauvegarderCircuit(self, index, circuit):
      self.circuits[index] = circuit

   def getCircuit(self, index):
      return self.circuits[index]

   def getFittest(self):
      fittest = self.circuits[0]
      for i in range(0, self.taillePopulation()):
         if fittest.getFitness() <= self.getCircuit(i).getFitness():
            fittest = self.getCircuit(i)
      return fittest

   def taillePopulation(self):
      return len(self.circuits)


class GA:
   def __init__(self, gestionnaireCircuit):
      self.gestionnaireCircuit = gestionnaireCircuit
      self.tauxMutation = 0.015
      self.tailleTournoi = 5
      self.elitisme = True
      self.print_cro = True
      self.print_tou = True

   def evoluerPopulation(self, pop, print_pop=False):
      nouvellePopulation = Population(
          self.gestionnaireCircuit, pop.taillePopulation(), False)
      elitismeOffset = 0
      if self.elitisme:
         nouvellePopulation.sauvegarderCircuit(0, pop.getFittest())
         elitismeOffset = 1

      for i in range(elitismeOffset, nouvellePopulation.taillePopulation()):
         parent1 = self.selectionTournoi(pop)
         parent2 = self.selectionTournoi(pop)
         enfant = self.crossover(parent1, parent2, self.print_cro)
         nouvellePopulation.sauvegarderCircuit(i, enfant)
         self.print_cro = False

      for i in range(elitismeOffset, nouvellePopulation.taillePopulation()):
         self.muter(nouvellePopulation.getCircuit(i))

      if print_pop:
          nouvellePopulation.print_population()

      return nouvellePopulation

   def crossover(self, parent1, parent2, print_cro=False):
      global pparent1
      global pparent2
      global penfant

      enfant = Circuit(self.gestionnaireCircuit)

      startPos = int(random.random() * parent1.tailleCircuit())
      endPos = int(random.random() * parent1.tailleCircuit())

      for i in range(0, enfant.tailleCircuit()):
         if startPos < endPos and i > startPos and i < endPos:
            enfant.setArticle(i, parent1.getArticle(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               enfant.setArticle(i, parent1.getArticle(i))

      for i in range(0, parent2.tailleCircuit()):
         if not enfant.contientArticle(parent2.getArticle(i)):
            for ii in range(0, enfant.tailleCircuit()):
               if enfant.getArticle(ii) == None:
                  enfant.setArticle(ii, parent2.getArticle(i))
                  break

      if print_cro:
        pparent1 = parent1
        pparent2 = parent2
        penfant = enfant

      return enfant

   def muter(self, circuit):
     for circuitPos1 in range(0, circuit.tailleCircuit()):
        if random.random() < self.tauxMutation:
           circuitPos2 = int(circuit.tailleCircuit() * random.random())

           article1 = circuit.getArticle(circuitPos1)
           article2 = circuit.getArticle(circuitPos2)

           circuit.setArticle(circuitPos2, article1)
           circuit.setArticle(circuitPos1, article2)

   def selectionTournoi(self, pop):
     global ptournoi
     global pwinner
     tournoi = Population(self.gestionnaireCircuit, self.tailleTournoi, False)
     for i in range(0, self.tailleTournoi):
        randomId = int(random.random() * pop.taillePopulation())
        tournoi.sauvegarderCircuit(i, pop.getCircuit(randomId))
     fittest = tournoi.getFittest()

     startWithOne = True
     for c in tournoi.circuits:
         if c.circuit[0] != 1:
             startWithOne = False
     if startWithOne:
         if self.print_tou:
                ptournoi = tournoi
                pwinner = fittest
                self.print_tou = False

     return fittest

api.add_resource(HelloWorld, '/')  # GET
api.add_resource(Articles, '/articles')  # GET
api.add_resource(ArticlesPositions, '/articlespositions')  # GET
api.add_resource(Distances, '/distances')  # POST
api.add_resource(Process, '/process')  # POST
api.add_resource(Test, '/test')  # GET

if __name__ == '__main__':
     app.run(port='5002')
