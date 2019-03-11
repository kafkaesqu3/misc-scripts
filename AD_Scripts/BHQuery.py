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
            elif queryType == "firstdegree_localadmin":
                query = "MATCH p=(m:Group {name: '%s'})-[r:AdminTo]->(n:Computer) RETURN n.name" % object
            elif queryType == "groupdelegated_localadmin":
                query = "MATCH p = (g1:Group {name:'%s'})-[r1:MemberOf*1..]->(g2:Group)-[r2:AdminTo]->(n:Computer) RETURN n.name" % object
            elif queryType == "deriv-admin": 
                query = "MATCH p = shortestPath((g:Group {name:'%s'})-[r:MemberOf|AdminTo|HasSession*1..]->(n:Computer)) RETURN n.name" % object
         #   elif arguments.outbound:
         #       query = "MATCH (n) WHERE NOT n.name='%s' WITH n MATCH p = shortestPath((u:User {name:'%s'})-[r1:MemberOf|AddMembers|AllExtendedRights|ForceChangePassword|GenericAll|GenericWrite|WriteDacl|WriteOwner*1..]->(n)) RETURN p" % object
         #   elif arguments.inbound:
         #       query = "MATCH (n) WHERE NOT n.name='%s' WITH n MATCH p = shortestPath((n)-[r:MemberOf|AddMembers|AllExtendedRights|ForceChangePassword|GenericAll|GenericWrite|WriteDacl|WriteOwner*1..]->(g:Group {name: '%s'})) RETURN p" % object
            elif queryType == "sessions":
                query = "MATCH (n:Computer)-[r:HasSession]->(m:User {name:'%s'}) RETURN n.name" % object
            else: 
                pass
            print("%s - %s: %s") % (object, queryType, query)
            results = json.loads(self.doCurl(query))['results'][0]['data']
            results_return = []
            for result in results:
                results_return.append(str(result['row']).encode("utf-8")[3:-2])
            return results_return
