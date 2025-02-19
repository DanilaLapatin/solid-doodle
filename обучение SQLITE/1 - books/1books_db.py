import sqlite3


def create_books_db():
    books_data_list = [
        (1, 'The Catcher in the Rye'),
        (2, 'Nine Stories'),
        (3, 'Franny and Zooey'),
        (4, 'The Great Gatsby'),
        (5, 'Tender id the Night'),
        (6, 'Pride and Prejudice'),
        (7, 'Professional ASP.NET 4.5 in C# and VB')
        ]

    conn = sqlite3.connect('books_and_authors.db')
    cursor = conn.cursor()
    #cursor.execute('DROP TABLE books')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER NOT NULL,
        name VARCHAR(70) NOT NULL,
        PRIMARY KEY(id))
    ''')

    for book_data in books_data_list:
        cursor.execute("INSERT INTO books(id,name) VALUES (?,?)",(book_data[0],book_data[1]))

    conn.commit()
    conn.close()

def print_books():
    conn = sqlite3.connect('books_and_authors.db')
    cursor = conn.execute('''SELECT * FROM books''')
    books = cursor.fetchall()

    for row in books:
        print(f"{row[0]} - {row[1]}")
    

    conn.close()



def create_authors():
    authors_list = [
        ('J.D. Salinger', 'USA'),
        ('F. Scott. Fitzgerald', 'USA'),
        ('Jane Austen', 'UK'),
        ('Scott Hanselman', 'USA'),
        ('Jason N. Gaylord', 'USA'),
        ('Pranav Rastogi', 'India'),
        ('Todd Miranda', 'USA'),
        ('Christian Wenz', 'USA')
    ]

    conn = sqlite3.connect('books_and_authors.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE authors')
    cursor.execute('''
        CREATE TABLE authors (
        id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(70) NOT NULL,
        country VARCHAR(100) NOT NULL
        )
    ''')

    cursor.executemany("INSERT INTO authors (name, country) VALUES (?,?)",authors_list)

    conn.commit()
    conn.close()

def print_authors():
    conn = sqlite3.connect('books_and_authors.db')
    cursor = conn.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    for row in authors:
        print(f"{row[0]} - {row[1]}/{row[2]}")
        
    conn.close()
    
#conn = sqlite3.connect('books_and_authors.db')
#cursor = conn.cursor()

#create_authors()
#print_authors()

def create_books_authors():
    
    books_authors_data = [
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 2),
        (5, 2),
        (6, 3),
        (7, 4),
        (7, 5),
        (7, 6),
        (7, 7),
        (7, 8)
    ]
    conn = sqlite3.connect('books_and_authors.db')
    cursor =conn.cursor()
    cursor.execute('DROP TABLE booksAuthors')
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('''
        CREATE TABLE booksAuthors (
        authorId INTEGER,
        bookId INTEGER,
        FOREIGN KEY (authorId) REFERENCES authors(id),
        FOREIGN KEY (bookId) REFERENCES books(id)
        )
            
        ''')
    cursor.executemany("INSERT INTO booksAuthors (bookId,authorId) VALUES (?,?)",books_authors_data)

    conn.commit()
    conn.close()

def print_books_authors():
    conn = sqlite3.connect('books_and_authors.db')
    cursor = conn.execute('''
        SELECT
        booksAuthors.authorId,
        authors.name,
        booksAuthors.bookId,
        books.name
        FROM booksAuthors
        INNER JOIN authors ON authors.id = booksAuthors.authorId
        INNER JOIN books ON books.id = booksAuthors.bookId
        ''')
    books_authors = cursor.fetchall()

    for row in books_authors:
        print(f"Author: {row[0]} - {row[1]}, Book: {row[2]} - {row[3]}")
        
    conn.close()

print_books_authors()
