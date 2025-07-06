import os

import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

conn = psycopg2.connect(user='nalepo_user',password='5bHGAJmRCsHOYSFjppOr7sIL2xQrPpsX',host='dpg-d1l4tqndiees73f7b3h0-a',port='5432',database='nalepo')

cur = conn.cursor()


# fetching data
def fetch_users():
    cur.execute('select * from users;')
    users = cur.fetchall()
    return users

def fetch_campaigns():
    cur = conn.cursor()
    cur.execute("""
            SELECT campaign_id, title,description,goal_amount,start_date,end_date,
            TO_CHAR(created_at, 'Month DD, YYYY')
            FROM campaigns ORDER BY created_at DESC
            """)
    campaigns = cur.fetchall()
    return campaigns

def fetch_donation():
    cur.execute('select * from donations;')
    donations = cur.fetchall()
    return donations

def fetch_payments():
    cur.execute('select * from payments;')
    payments = cur.fetchall()
    return payments

def fetch_volunteers():
    cur.execute('select * from volunteers;')
    volunteers = cur.fetchall()
    return volunteers

def fetch_events():
    cur = conn.cursor()
    cur.execute("""
                SELECT event_id,title,description,event_date,location,
                TO_CHAR(created_at, 'Month DD, YYYY')
                FROM events ORDER BY created_at DESC
            """)
    events = cur.fetchall()
    return events

def fetch_eventreg():
    cur.execute('select * from eventreg;')
    eventreg = cur.fetchall()
    return eventreg

def fetch_blogs():
    cur = conn.cursor()
    cur.execute("""
        SELECT blog_id, user_id, title, content, 
        TO_CHAR(published_at, 'Month DD, YYYY') 
        FROM blogs ORDER BY published_at DESC
    """)
    blogs = cur.fetchall()
    cur.close()
    return blogs



def fetch_contact():
    cur.execute('select * from contact;')
    contact = cur.fetchall()
    return contact

# inserting data
def insert_users(values):
    insert = "insert into users(name,email,password,role,status)values(%s,%s,%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_campaigns(values):
    insert = "insert into campaigns(title,description,goal_amount,start_date,end_date)values(%s,%s,%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_donations(values):
    insert = "insert into donations(user_id,campaign_id,amount)values(%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_payments(values):
    insert = "insert into payments(donation_id,provider,amount)values(%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_volunteers(values):
    insert = "insert into volunteers(user_id,skills,availability)values(%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_events(values):
    insert = "insert into events(title,description,event_date,location)values(%s,%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_event_registration(values):
    insert = "insert into event_registration(event_id,user_id)values(%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_blogs(values):
    insert = "insert into blogs(user_id,title,content)values(%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def insert_contact(values):
    insert = "insert into contact(name,email,message)values(%s,%s,%s)"
    cur.execute(insert,values)
    conn.commit()

def check_user(email):
    query="select * from users where email = %s"
    cur.execute(query,(email,))
    user=cur.fetchone()
    return user

