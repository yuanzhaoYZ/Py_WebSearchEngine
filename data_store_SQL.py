import sqlite3

#conn = sqlite3.connect('big_table.db')
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute('''CREATE TABLE if not exists pages
             (url TEXT,priority INT,cache_path TEXT)''')
def put_page(url,priority,cache_path):
    cur.execute("INSERT INTO pages VALUES(?,?,?)",(url,priority,cache_path))
def get_page(url):
    cur.execute("SELECT * from pages where url = ?",url)
    output = cur.fetchall()
    return output

def get_page_content(url):
    cache_file_path = get_page(url)[2]
    with open (cache_file_path, "r") as page_file:
        page_content=page_file.read()
        page_file.close()
    return page_content
    
#===============================================================================
#get the next webpage with largest key_word counts
#===============================================================================
def get_next_seed():
    cur.execute("SELECT *,MIN(priority) as priority from pages")
    output = cur.fetchall()
    return output

def test():
    cur.execute("SELECT * from pages")
    print cur.fetchall()