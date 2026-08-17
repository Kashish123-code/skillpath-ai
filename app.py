from flask import Flask, render_template
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

driver = GraphDatabase.driver(
    os.environ.get("COGNODB_URI"),
    auth=(os.environ.get("COGNODB_USER"), os.environ.get("COGNODB_PASSWORD"))
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test-db")
def test_db():
    with driver.session() as session:
        result = session.run("RETURN 'Connected!' AS message")
        return result.single()["message"]

@app.route("/path/<skill_name>/<career_title>")
def find_path(skill_name, career_title):
    query = "MATCH (start:Skill {name: $skill_name}), (end:Career {title: $career_title}) MATCH p = shortestPath((start)-[:PREREQUISITE_OF|REQUIRED_FOR*]->(end)) RETURN [node in nodes(p) | coalesce(node.name, node.title)] AS path"
    with driver.session() as session:
        result = session.run(query, skill_name=skill_name, career_title=career_title)
        record = result.single()
        if record:
            return {"path": record["path"]}
        else:
            return {"path": None, "message": "No path found"}

if __name__ == "__main__":
    app.run(debug=True)