from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def upload_file():
   return '''
   <html>
   <body>
        <form action = "http://localhost:8000/upload" method = "POST" enctype = "multipart/form-data">
            <p> Username: </p>
            <div class="form-group">
                <input type="text" class="form-control" id="username" name="username">
            </div>

            <p> Username: </p>
            <div class="form-group">
                <input type="text" class="form-control" id="email" name="email">
            </div>

            <p> Username: </p>
            <div class="form-group">
                <input type="text" class="form-control" id="password" name="password">
            </div>
            <div class="form-group">
                <input type="file" class="form-control" id="file" name = "file" />
            </div>
            <input type = "submit"/>
        </form>   
   </body>
</html>
'''
	
@app.route('/upload', methods = ['POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8000)