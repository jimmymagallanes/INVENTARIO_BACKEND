import sqlite3

#crear conexión a la base de datos
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

#cursor

cur = connection.cursor()

cur.execute("INSERT INTO posts(title, content, tags, coments) VALUES (?,?,?,?)", 
            ('First Post', 'Content for the first post', 'post, article', 'añadir descripción de post')
            )

cur.execute("INSERT INTO posts(title, content, tags, coments) VALUES (?,?,?,?)", 
            ('Second Post', 'Content for the second post', 'post, article', 'añadir descripción de post')
            )
cur.execute("INSERT INTO users(username, pass, email) VALUES (?,?,?)", 
            ('EsthefaniaDC', '1234', 'esthefaniamedina.uc@gmail.com')
            )

connection.commit()
connection.close()