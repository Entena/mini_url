import sqlite3
import argparse
import hashlib
#Globals
con = sqlite3.connect("./urls.db")
cursor = con.cursor()

#Decode ID
def get_url(id):
    if verbose:
        print('Fetch URL for id ' + str(id))
    sql = 'SELECT url FROM urls WHERE hash_for_use = ' + str(id)
    cursor.execute(sql)
    row = cursor.fetchone()
    if(row is not None and len(row) > 0):
        return row[0]
    else:
        return 'INVALID ID'

#Hash our URL
def hash_url(url):
    if verbose:
        print('HASHING ' + url)
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    #See if our table has the hash
    sql = 'SELECT * FROM urls WHERE hash_key = "' + url_hash + '"'

    if verbose:
        print(sql)
    cursor.execute(sql)
    row = cursor.fetchone()
    if(row is not None and len(row) > 0):
        #If we find a matching row return the already found hash
        return row[2]
    else:
        new_id = get_available_hash(url)
        insert_sql = 'INSERT INTO urls VALUES("' + url_hash + '","' + url + '",' + str(new_id) + ')'
        if verbose:
            print('INSERTING ' + insert_sql)
        cursor.execute(insert_sql) #Insert, commit, return our new id.
        con.commit()
        return new_id
    
#Create table if not defined
def init_table():
    if verbose:
        print('Initing our table')
    sql = 'CREATE TABLE IF NOT EXISTS urls (hash_key TEXT PRIMARY KEY, url TEXT, hash_for_use INTEGER)'
    cursor.execute(sql)
    #Make sure we commit this
    con.commit()

#Even though we have an easy hash for our url let's do the easier thing
#and get the first available number in a range, we can modify this later, but
#for our tables purposes this will make things pretty, this would be where we add limits
#to our range. For now this is just gonna go until it hits the max int size in sqlite.
#Our range starts at 0 and goes up from there. We can set a max using the SQL query here, but it is not set as of now.
#In cases where we decided on a range and have a risk of running out we should just shard our service and recycle the id range, or split it out.
#Because this app so minified spliting it out should be very cheap and done either at a host level (run this in a lambda and redirect URLs)
def get_available_hash(url):
    if verbose:
        print('Checking for next available id for ' + url)
    sql = 'SELECT MIN(hash_for_use) + 1 FROM urls t1 WHERE NOT EXISTS (SELECT NULL FROM urls t2 WHERE t2.hash_for_use = t1.hash_for_use + 1)'
    cursor.execute(sql)
    next_id = cursor.fetchone()
    if (next_id[0] is None):
        return 0
    else:
        return next_id[0]


parser = argparse.ArgumentParser()
parser.add_argument('-id', type=int)
parser.add_argument('-url', type=str)
parser.add_argument('-v', action='store_true')
args = parser.parse_args()
verbose = bool(False)

init_table()

if args.v:
    verbose = bool(True)

if args.url is not None:
    url = args.url
    db_id = hash_url(url)
    print(str(db_id))
elif args.id is not None:
    id = args.id
    db_url = get_url(id)
    print(db_url)

cursor.close()
con.close()