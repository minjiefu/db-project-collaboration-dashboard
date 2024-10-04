from neo4j import GraphDatabase


# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

def findFacultyPath(tx, faculty1, faculty2):
    q = 'profile match (f1:FACULTY), (f2:FACULTY), path=shortestPath((f1)-[:PUBLISH*]-(f2)) WHERE f1.name=$name1 and ' \
        'f2.name=$name2 return path limit 5'
    paths = tx.run(q, name1=faculty1, name2=faculty2)
    
    nodes = []
    for path in paths:
        allNodes = path['path'].nodes
        tempNodes = []
        for node in allNodes[::2]:
            tempNodes.append({"data": {"id": node["id"], "label": node["name"]}})
        len_nodes = len(tempNodes)
        for i in range(len_nodes - 1):
            tempNodes.append({"data": {"source": tempNodes[i]['data']['id'], "target": tempNodes[i + 1]['data']['id'],
                                       "label": 'Co-Authors'}})
        nodes.extend(tempNodes)
    return nodes


def getConnectionsToFaculty(knownFaculty, unknownFaculty):
    with driver.session(database="academicworld") as session:
        result = session.execute_read(findFacultyPath, knownFaculty, unknownFaculty)
        return result


