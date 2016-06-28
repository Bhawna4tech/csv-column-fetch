#!/usr/bin/python
import os
import sys
import csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename



app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['csv','xls'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def csv_writer(data,data1):
	#print "WRITING"
	
	with open(os.path.join('uploads/',"new.csv"), "ab") as csv_file: 
		writer = csv.writer(csv_file,delimiter= ',')
		for line in zip(data,data1):
			writer.writerow(line)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
	else :
		return ''' 
			<html>
			<body> <h1>Please Upload (.csv) file</h1>
			</body> 
			</html>
			'''
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	#file.save(os.path.join('/uploads',filename))
        	
	print "hello I am above reading"
    	with open(os.path.join('uploads/',filename), 'rb') as csvfile:
		#print "READING"
   		for line in csvfile.readlines():
   		     array = line.split(',')
	   	     first_item = array[0]

   		num_columns = len(array)
	   	csvfile.seek(0)

    		reader = csv.reader(csvfile, delimiter=',')
		#htmlfile = open("templates/hello2.html","w")
		#htmlfile.write('<h1>' + 'Fetched Data' + '</h1>')
 		#os.remove(os.path.join('uploads/','new.csv')) #OTHERWISE, THE WRITE FILE WILL BECOME BULKY AND WILL HAVE REPEATED DATA
		i=0
		rownum=0
		flag=0
		for row in reader:
			if rownum==0:
				for column in row:
					if "Pump Name" in column:
						col1=i
						i=i+1
						flag=1
					elif "PRICE" in column:
						col2=i
						i=i+1
					else:
						i=i+1
				if (flag==0):
					return ''' 
					<html>
					<body> <h1>The file doesn't contain <b>Pump Name</b></h1>
					</body> 
					</html>
					'''
			rownum=rownum+1
			content = list(row[col1:(col1+1)])		
			content2 = list(row[col2:(col2+1)])
		
			csv_writer(content,content2)

	return redirect(url_for('uploaded_file',filename='new.csv'))
	

@app.route("/uploads/getCSVfile")
def getPlotCSV():
	return send_from_directory(app.config['UPLOAD_FOLDER'],'new.csv')

@app.route('/uploads/<filename>')
def uploaded_file(filename):

	reader = csv.reader(open(os.path.join('uploads/',filename)))
	htmlfile = open("templates/csvpage.html","w")
	#htmlfile=os.fdopen(os.open("templates/hello2.html", os.O_WRONLY | os.O_CREAT, 0600), '-rwx') 
	rownum = 0
	htmlfile.write('<a href="/uploads/getCSVfile">Click to Download</a>')
	htmlfile.write('<table>')
	for row in reader: 
		if rownum == 0:
			htmlfile.write('<tr>')
		  	for column in row:
  				htmlfile.write('<th>' + column + '</th>')
		  		htmlfile.write('</tr>')
	  	else:
	  		htmlfile.write('<tr>')	
  			for column in row:
  				htmlfile.write('<td>' + column + '</td>')
	 		htmlfile.write('</tr>')
		rownum += 1
	htmlfile.write('</table>')
	print "Created " + str(rownum) + " row table."
	htmlfile.close()
	return render_template('csvpage.html')
	#return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )












 



