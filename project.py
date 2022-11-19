from flask import *    #import all class from flask module
import sqlite3

app=Flask(__name__)  #creating object in Flask class

@app.route("/")   #decorater
def index():
	return render_template("index.html") #render_template() is a class from flask

@app.route("/addcontact")
def addcontact():
	return render_template("addcontact.html")

@app.route("/savedetails",methods=["POST","GET"])
def savedetails():
	msg="msg"
	if request.method=="POST":
		try:
			name=request.form["name"]
			email=request.form["email"]
			number=request.form["number"]
			
			with sqlite3.connect("/home/sanjay/AddressBook/contactsbook.db") as connection:
				cursor=connection.cursor()
				cursor.execute(""" INSERT INTO contacts("Name","Email","Number")VALUES(?,?,?)""",(name,email,number))
				connection.commit()
				msg="contact added successfully"
		except:
			connection.rollback()
			msg="we can not add contact to the list"
		finally:
			return render_template("success.html",msg=msg)
		

@app.route("/display")
def display():
	connection=sqlite3.connect("/home/sanjay/AddressBook/contactsbook.db")
	connection.row_factory=sqlite3.Row
	cursor=connection.cursor()
	cursor.execute("SELECT * FROM contacts")
	rows=cursor.fetchall()
	return render_template("display.html",rows=rows)

@app.route("/delete")
def delete():
	return render_template("delete.html")

@app.route("/deleterecord",methods=["POST"])
def deleterecord():	
	Sno=request.form["Sno"]
	connection=sqlite3.connect("/home/sanjay/AddressBook/contactsbook.db")
	try:
		cursor=connection.cursor()
		cursor.execute("DELETE FROM contacts WHERE Sno = ?",Sno)
		connection.commit()
		connection.close()
		msg="contact successfully deleted"
	except:
		msg="can't be deleted"
	finally:
		return render_template("delete_record.html",msg=msg)

if __name__=="__main__":
	app.run(debug=True)