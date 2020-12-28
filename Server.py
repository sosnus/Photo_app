import web
import os 
import time
import json

os.system("pwd")
os.system("ls")
os.system("ls ./tmp")
os.system("ls -l")

urls = (
    '/', 'Index',
    '/upload', 'Upload',
    '/result', 'Result'
)

lastOutputJson = "nofile.json"

pwdToLastTimestamp = '/dev/null'


class Index:
    def GET(self):
        return "Hi!, use /upload"

class Result:
    def GET(self):
        print(pwdToLastTimestamp)
        newRespond = {}
        with open(str(pwdToLastTimestamp + 'output1.json')) as json_file:
            newRespond = json.load(json_file)
            # return json.dumps(data)
        with open(str(pwdToLastTimestamp + 'output2.json')) as json_file:
            newRespond.update(json.load(json_file))
            # return json.dumps(data)
        return json.dumps(newRespond)
        # with open('lastOutputJson', 'r') as outfile:
            # print(str(json_file))
        return "Result!"




class Upload:
    def GET(self):
        return """<html><head></head><body>
        <h1>PhotoApp</h1>
        <h2>Upload Your photo here</h2>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        print("_____ NEW POST on /upload...")
        web.debug(x['myfile'].filename) # This is the filename

        # filedir = '/home/zombie/data/minio/photo' # Azure VM
        # filedir = '/Users/stanislawpulawski/data/dockervolumes/minio/photo' # My Laptop
        filedir = '/data/minio/photo' # Container
        
        timestamp = str(int(time.time()))
        os.system("cd {} && mkdir {}".format(filedir, timestamp))
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            wholeFilepath = str(filedir +'/'+ timestamp +'/'+ 'inputfile')
            fout = open(filedir +'/'+ timestamp +'/'+ 'inputfile','wb') # creates the file where the uploaded file should be stored
            fout = open(wholeFilepath,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        global lastOutputJson
        pathInputFile = filedir + '/'+timestamp+"/inputfile"    
        lastOutputJson = filedir + '/'+timestamp+"/inputfile"    
        lastOutputJson = lastOutputJson.replace("inputfile", "outputfile.json")

        os.system("cp {} ./tmp/{}".format(pathInputFile, x['myfile'].filename))
        runContrastCommand = str("python3 ./contrast.py -f {} -o {} -n {}".format(wholeFilepath, lastOutputJson, x['myfile'].filename))
        print(runContrastCommand)
        os.system(runContrastCommand)
        runFaceRecognitionCommand = str("python3 ./Start.py -f {} -o {} -n {}".format(wholeFilepath, lastOutputJson, x['myfile'].filename))
        print(runFaceRecognitionCommand)
        os.system(runFaceRecognitionCommand)


        print(pathInputFile)
        print("AAAAAAAAAAA")
        global pwdToLastTimestamp
        print(pwdToLastTimestamp)
        pwdToLastTimestamp = str(pathInputFile.replace("/inputfile", "/"))
        print(pwdToLastTimestamp)
        print("_____ Copy all to timestamp folder...")

        os.system("cp ./tmp/output1.json {} ".format(pathInputFile.replace("inputfile", "output1.json")))
        os.system("cp ./tmp/output2.json {} ".format(pathInputFile.replace("inputfile", "output2.json")))
        os.system("cp ./tmp/{} {} ".format(x['myfile'].filename, pathInputFile.replace("inputfile", x['myfile'].filename)))
        os.system("cp ./tmp/out-face-{} {} ".format(x['myfile'].filename, pathInputFile.replace("inputfile", str('out-face-' + x['myfile'].filename))))

        print("_____ Done, return /result...")
        raise web.seeother('/result')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()