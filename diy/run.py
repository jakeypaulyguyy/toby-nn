import web
import numpy as np
import simplejson as json
import mysql.connector
from cleardb import user
from cleardb import password
from cleardb import host
from cleardb import database

#mycursor.execute("SELECT w0, w1 FROM weights")
#myresult = mycursor.fetchall()
#
#w0 = myresult[0]
#w1 = myresult[1]
#print(w0)

render = web.template.render('html/')

def nonlin(x,deriv=False):
	if(deriv==True):
		return x*(1-x)

	return 1/(1+np.exp(-x))
    
class run:
    def POST(self):
        user_data = web.input()
        message = user_data.message
        message_array = message.split(',')
        message_int = [int(x) for x in message_array]
        index = user_data.Model
        mydb = mysql.connector.connect(user=user, password=password, host=host, database=database)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT w0, w1, name1, name2 FROM weights where `index` = " + str(index))
        weights = mycursor.fetchall()
        mycursor.close()
        w0 = None
        w1 = None
        for row in weights :
            w0 = np.array(json.loads(row[0]))
            w1 = np.array(json.loads(row[1]))
            name1 = row[2]
            name2 = row[3]
        print(w0)
        print(w1)
        x = np.array([message_int])
        print(x)
        # input layer
        l0 = x
        # hidden layer
        l1 = nonlin(np.dot(l0, w0))
        # output layer
        l2 = nonlin(np.dot(l1, w1))
        l2 = l2.ravel()
        answer = str
        if np.array_equal(np.around(l2), [1,0]):
            answer = name1
            
        elif np.array_equal(np.around(l2), [0,1]):
            answer = name2
            
        else:
            answer = "I don't know"
            
        return render.diy(answer,l2[0]*100,l2[1]*100,name1,name2)
