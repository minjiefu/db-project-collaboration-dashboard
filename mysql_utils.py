import mysql.connector
import pandas as pd

cnx = mysql.connector.connect(user='root', password='root_test',
                              host='127.0.0.1',
                              database='academicworld')


cursor = cnx.cursor()   


def get_keywords():
    query = "SELECT name FROM keyword order by name asc"
    cursor.execute(query)
    result = [item[0] for item in cursor.fetchall()]
    return result


def get_trends(kword = "deep learning"):
    
    query = "select year, count(id) as publications from publication, publication_keyword " \
            "where id = publication_id and keyword_id = (select id from keyword where name = %s) " \
            "group by year order by year"
    values = (kword, )
    cursor.execute(query, values)
    result = pd.DataFrame.from_records(cursor.fetchall(), columns= [des[0] for des in cursor.description])
    
    #cursor.close()
    #cnx.close()
    return result

def create_potential_research_keywords_table():
    query = ("CREATE TABLE potential_research_keywords (name varchar(512) NOT NULL, PRIMARY KEY (name))")
    cursor.execute(query)


def potential_research_keywords_table_exists():
    query = "SHOW TABLES LIKE 'potential_research_keywords'"
    cursor.execute(query)
    result = cursor.fetchall()
    return bool(result)
        
def get_potential_research_keywords():
    if not potential_research_keywords_table_exists():
        create_potential_research_keywords_table()
    query = "SELECT * FROM potential_research_keywords"
    cursor.execute(query)
    result = cursor.fetchall()
    return [row[0] for row in result]



def add_potential_keyword(keyword):
    query = "INSERT INTO potential_research_keywords (name) VALUES (%s)"
    values = (keyword, )
    cursor.execute(query, values)
    cnx.commit()
    
def get_top10_faculty_related_favorite_keywords():
    if not potential_research_keywords_table_exists():
        return
    query = ("SELECT faculty.name AS name, count(*) AS count, SUM(score) AS score "
                 "FROM faculty_keyword, faculty, potential_research_keywords, keyword "
                 "WHERE faculty_id = faculty.id AND keyword_id = keyword.id AND keyword.name = potential_research_keywords.name "
                 "GROUP BY name "
                 "ORDER BY score DESC "
                 "LIMIT 10")
    cursor.execute(query)
    result  = cursor.fetchall()
    top10_faculty_related_favorite_keywords = [row[0] for row in result]
    return top10_faculty_related_favorite_keywords
    
def delete_potential_keyword(keyword):
    query = "DELETE FROM potential_research_keywords WHERE name = %s"
    values = (keyword, )
    cursor.execute(query, values)
    cnx.commit()

def get_faculty_info(name):
    query = "select * from partner_info WHERE name = %s"
    values = (name, )
    cursor.execute(query, values)
    result = cursor.fetchall()
    return [row for row in result]

def queryFaculties():
    query = "select name from partner_info order by name asc"
    cursor.execute(query)
    result = [item[0] for item in cursor.fetchall()]
    return result

def notes_table_exists():
    query = "SHOW TABLES LIKE 'notes'"
    cursor.execute(query)
    result = cursor.fetchall()
    return bool(result)

def create_notes_table():
    query = ("CREATE TABLE notes (name varchar(512), note varchar(1024))")
    cursor.execute(query)


def get_notes():
    if not notes_table_exists():
        create_notes_table()
    query = ("SELECT * from notes")
    cursor.execute(query)
    result  = cursor.fetchall()
    return [(row[0], row[1]) for row in result]

def add_to_notes(v1, v2):
    query = "INSERT INTO notes (name, note) VALUES (%s, %s)"
    values = (v1, v2)
    cursor.execute(query, values)
    cnx.commit()

def delete_from_notes(v1, v2):
    query = "DELETE FROM notes where name = %s and note = %s"
    values = (v1, v2)
    cursor.execute(query, values)
    cnx.commit()




    