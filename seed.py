from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.environ.get("COGNODB_URI"),
    auth=(
        os.environ.get("COGNODB_USER"),
        os.environ.get("COGNODB_PASSWORD")
    )
)


seed_queries = [

    # =========================================================
    # SKILLS
    # =========================================================

    # Programming
    "MERGE (:Skill {name: 'Python Basics', category: 'Programming'})",
    "MERGE (:Skill {name: 'Data Structures', category: 'Programming'})",
    "MERGE (:Skill {name: 'Object Oriented Programming', category: 'Programming'})",

    # Data
    "MERGE (:Skill {name: 'SQL', category: 'Data'})",
    "MERGE (:Skill {name: 'Pandas', category: 'Data'})",
    "MERGE (:Skill {name: 'Data Visualization', category: 'Data'})",
    "MERGE (:Skill {name: 'Statistics', category: 'Data'})",

    # AI / ML
    "MERGE (:Skill {name: 'Machine Learning', category: 'AI/ML'})",
    "MERGE (:Skill {name: 'Deep Learning', category: 'AI/ML'})",

    # Backend
    "MERGE (:Skill {name: 'Flask', category: 'Web Development'})",
    "MERGE (:Skill {name: 'REST APIs', category: 'Web Development'})",

    # Engineering
    "MERGE (:Skill {name: 'Git', category: 'Developer Tools'})",
    "MERGE (:Skill {name: 'Docker', category: 'DevOps'})",


    # =========================================================
    # CAREERS
    # =========================================================

    "MERGE (:Career {title: 'Data Analyst'})",
    "MERGE (:Career {title: 'ML Engineer'})",
    "MERGE (:Career {title: 'Backend Developer'})",
    "MERGE (:Career {title: 'Data Scientist'})",
    "MERGE (:Career {title: 'Python Developer'})",


    # =========================================================
    # PYTHON LEARNING PATH
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Python Basics'}),
        (b:Skill {name:'Data Structures'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Python Basics'}),
        (b:Skill {name:'Object Oriented Programming'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,


    # =========================================================
    # DATA ANALYST PATH
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Python Basics'}),
        (b:Skill {name:'SQL'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'SQL'}),
        (b:Skill {name:'Pandas'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Pandas'}),
        (b:Skill {name:'Data Visualization'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Data Visualization'}),
        (b:Career {title:'Data Analyst'})
    MERGE (a)-[:REQUIRED_FOR]->(b)
    """,


    # =========================================================
    # ML ENGINEER PATH
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Data Structures'}),
        (b:Skill {name:'Machine Learning'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Machine Learning'}),
        (b:Skill {name:'Deep Learning'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Deep Learning'}),
        (b:Career {title:'ML Engineer'})
    MERGE (a)-[:REQUIRED_FOR]->(b)
    """,


    # =========================================================
    # BACKEND DEVELOPER PATH
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Python Basics'}),
        (b:Skill {name:'Flask'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Flask'}),
        (b:Skill {name:'REST APIs'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'REST APIs'}),
        (b:Career {title:'Backend Developer'})
    MERGE (a)-[:REQUIRED_FOR]->(b)
    """,


    # =========================================================
    # DATA SCIENTIST PATH
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Python Basics'}),
        (b:Skill {name:'Statistics'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Statistics'}),
        (b:Skill {name:'Machine Learning'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Machine Learning'}),
        (b:Career {title:'Data Scientist'})
    MERGE (a)-[:REQUIRED_FOR]->(b)
    """,


    # =========================================================
    # PYTHON DEVELOPER PATH
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Object Oriented Programming'}),
        (b:Skill {name:'Flask'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'Flask'}),
        (b:Career {title:'Python Developer'})
    MERGE (a)-[:REQUIRED_FOR]->(b)
    """,


    # =========================================================
    # COMMON DEVELOPER SKILLS
    # =========================================================

    """
    MATCH
        (a:Skill {name:'Object Oriented Programming'}),
        (b:Skill {name:'Git'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """,

    """
    MATCH
        (a:Skill {name:'REST APIs'}),
        (b:Skill {name:'Docker'})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """

]


# =============================================================
# RUN SEED
# =============================================================

try:

    with driver.session() as session:

        for query in seed_queries:

            session.run(query)

    print("======================================")
    print("Seed data loaded successfully!")
    print("Career graph is ready.")
    print("======================================")


except Exception as e:

    print("======================================")
    print("Error while loading seed data:")
    print(e)
    print("======================================")


finally:

    driver.close()