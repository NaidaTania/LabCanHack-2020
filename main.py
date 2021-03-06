import http.server
import socketserver
import requests, json
from flask import Flask,request,jsonify
from flask_restful import Resource,Api
import nlping
import aprioring
import re

PORT = 4444
Handler = http.server.SimpleHTTPRequestHandler

app = Flask(__name__)
api = Api(app)



class NLP(Resource):

    def __init__(self):
        self.uid = ""
        self.text = ""
        self.image = "" #url
        self.suggestions = [] #list of symptoms, keep track
        self.diagnosis = {}

    def NLPing(self):
        nlping.samplestring = self.text 
        print("nlping BEFORE",nlping.samplestring)
        print("SELF.TEXT",self.text)
        print("nlping AFTER",nlping.samplestring)
        '''
        Using text,
        I clean it up (filter stop words, rid punctuations, tokenize and maybe stem)
        use wordnet to find synonyms 

        '''
        return nlping.returnMeSymps()


    def get(self,user_id):
        #not implemented yet, but ideally look to DB and return the current data
        fakedata = {
        "Name" : "MomoHinamomoo",
        "Age" : "1000",
        "OHIP" : "xxx123yyy",
        "Last diagnosed" : "03 March 2020",
        "Last diagnosis" : "Abdominal bleeding"
        }
        resp = jsonify(fakedata)
        resp.status_code = 200
        return resp

    def post(self):
        if "image" in request.json:
            sendload = {
              "imageurl" : request.json["image"]
            }
            imageendpoint = "http://localhost:4445/image"
            r = requests.post(url = imageendpoint, data = json.dumps(sendload))
            rjson = json.loads(r.text)
            #then needs to process info before returning
            return rjson
        #else we NLP and then return appropriate thing
        self.uid = request.json["uid"]
        self.text = request.json["text"]
        self.suggestions = request.json["suggestions"] #list of symptoms, keep tra
        thesymptoms = self.NLPing()
        returnjson = {
            "uid" : self.uid,
            "suggestions" : thesymptoms
        }
        resp = jsonify(returnjson)
        resp.status_code = 200
        return resp 


class Home(Resource):
    def get(self):
        return "HELLO WORLD"

    def post(self):
        print(request.json)
        print("UP AND RUNNING AND HAPPY")
        return "UP AND RUNNING AND HAPPY"

#a shitty alternative to database :D
confirmedsymps = {}

class Predict(Resource):
    def __init__(self):
        self.uid = ""
        self.confirmedsymps = []
    # def get(self):
    #     self.uid = request.json["uid"]
    #     #return our current statistics
    #     if self.uid not in confirmedsymps.keys():
    #         return "no diagnosis yet!"
    #     #else we apriori the heck out of this
    #     itemsets = aprioring.apriit(confirmedsymps[self.uid])
    #     print("ITEMSETS:",itemsets)
    #     return itemsets
    def post(self):
        self.uid = request.json["uid"]
        for s in request.json["suggestions"]:
            if self.uid not in confirmedsymps:
                confirmedsymps[self.uid] = []
            if s not in confirmedsymps[self.uid]:
                confirmedsymps[self.uid].append(s)
        #then we predict the heck outta it and return
        itemsets = aprioring.apriit(confirmedsymps[self.uid])
        returnjson = {
            "uid" : self.uid,
            "text":"You may experience these commonly related symptoms?",
            "suggestions" : [x for x in itemsets.keys()]
        }
        resp = jsonify(returnjson)
        resp.status_code = 200
        return resp 
        #update the confirmed stats?

class Confirmed(Resource):
    def __init__(self):
        self.uid = ""
    def get(self):
        self.uid = request.json["uid"]
        #return our current statistics
        if self.uid not in confirmedsymps.keys():
            return "no diagnosis yet!"
        #else we apriori the heck out of this
        diagperc = aprioring.getdiagnosed(confirmedsymps[self.uid])
        cleandiagperc = {}
        for k in diagperc.keys():
            newk = re.sub("\u000b",":",k)
            cleandiagperc[newk] = diagperc[k]
        returnjson = {
            "uid" : self.uid,
            "text":"Your possible diagnosis based on percentage of symptoms",
            "diagnosis" : cleandiagperc
        }
        resp = jsonify(returnjson)
        resp.status_code = 200
        return resp 

api.add_resource(NLP, '/symptoms/<user_id>', '/symptoms') # First pass when I pass you everything
api.add_resource(Home, '/') # Route_1
api.add_resource(Predict, '/predict') # 2nd pass when
api.add_resource(Confirmed, '/diagnosis') # 2nd pass when 


if __name__ == '__main__':
     app.run(port='4444',host='0.0.0.0')


'''
with socketserver.TCPServer(("",PORT),Handler) as httpd:
    print("SERVING AT PORT", PORT)
    httpd.serve_forever()
'''

'''
Ideally we want the list of confirmed symtomps to be 


'''

