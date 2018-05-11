import requests
import json
import sys
import base64

class BHQuery():
    auth = ""
    def __init__(self): 
        username = 'neo4j'
        password = 'BloodHound'
        self.auth = base64.b64encode(username + ":" + password)


    def doCurl(self, statement):
        headers = { "Accept": "application/json; charset=UTF-8",
                    "Content-Type": "application/json",
                    "Authorization": self.auth }
        data = {"statements": [{'statement': statement}]}
        url = 'http://localhost:7474/db/data/transaction/commit'
        r = requests.post(url=url,headers=headers,json=data)
        return r.text

    def runQuery(self, queryType, objects):
        for object in objects: 
            object = object.upper().strip('\n')

            if queryType == "groups": 
                query = "MATCH p = (n:User {name:'%s'})-[r:MemberOf*1..]->(g:Group) RETURN g.name" % object
            elif queryType == "groupmembers":
                query = "MATCH p = (n)-[r:MemberOf*1..]->(g:Group {name:'%s'}) RETURN n.name" % object
            elif queryType == "deriv-admin": 
                query = "MATCH (c:Computer) WHERE NOT c.name='%s' WITH c MATCH p = shortestPath((n:User {name:'%s'})-[r:HasSession|AdminTo|MemberOf*1..]->(c)) RETURN c.name" % (object, object)
            elif queryType == "admin":
                query = "MATCH p=(n:User {name:'%s'})-[r1:MemberOf*1..]->(g:Group)-[r2:AdminTo]->(c:Computer) RETURN c.name" % object
         #   elif arguments.outbound:
         #       query = "MATCH (n) WHERE NOT n.name='%s' WITH n MATCH p = shortestPath((u:User {name:'%s'})-[r1:MemberOf|AddMembers|AllExtendedRights|ForceChangePassword|GenericAll|GenericWrite|WriteDacl|WriteOwner*1..]->(n)) RETURN p" % object
         #   elif arguments.inbound:
         #       query = "MATCH (n) WHERE NOT n.name='%s' WITH n MATCH p = shortestPath((n)-[r:MemberOf|AddMembers|AllExtendedRights|ForceChangePassword|GenericAll|GenericWrite|WriteDacl|WriteOwner*1..]->(g:Group {name: '%s'})) RETURN p" % object
            elif queryType == "sessions":
                query = "MATCH (n:Computer)-[r:HasSession]->(m:User {name:'%s'}) RETURN n.name" % object
            else: 
                pass
            results = json.loads(self.doCurl(query))['results'][0]['data']
            results_return = []
            for result in results:
                results_return.append(str(result['row']).encode("utf-8")[3:-2])
            return results_return
