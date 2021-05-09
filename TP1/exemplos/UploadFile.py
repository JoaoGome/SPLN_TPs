from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return '''
   <html>
   <body>
      <form action = "http://localhost:8000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
   </body>
</html>
'''
	
@app.route('/uploader', methods = ['POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8000)