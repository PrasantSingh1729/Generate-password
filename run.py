import os
from flask import Flask, render_template, request, redirect
import gevent.pywsgi
# from OpenSSL import SSL
import os
# context = SSL.Context(SSL.TLSv1_2_METHOD)
# context.use_certificate('mycert.crt')
# context.use_privatekey('myprivatekey.key')
app = Flask(__name__)

class _encrypter():
    """
    Encrypt the pressed character into string of length four \n
    Four character of string are one symbol, one number,\n
    one uppercase letter and one lowercase letter
    """
    def __init__(self,pin):
        self.pin = pin
        self.symbols = ['~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}',']','|','\\',':',';','"','\'','<',',','>','.','?','/',]
        self.numbers = ['1','2','3','4','5','6','7','8','9','0']
        self.lower_case_alphabets = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
        self.upper_case_alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    def _permutate_(self,encrypt,key):
        return encrypt[0]+encrypt[1]+encrypt[2]+encrypt[3]
    def _encrypt_(self,key):
        md = self.pin + ord(key)
        encrypt = [str(self.symbols[md%len(self.symbols)])]
        encrypt = encrypt + [str(self.lower_case_alphabets[md%len(self.lower_case_alphabets)])]
        encrypt = encrypt + [str(self.numbers[md%len(self.numbers)])]
        encrypt = encrypt + [str(self.upper_case_alphabets[md%len(self.upper_case_alphabets)])]
        return encrypt[0]+encrypt[1]+encrypt[2]+encrypt[3]

def encrypt(pin, password):
    encrypter = _encrypter(pin)
    encrypt = ""
    for char in password:
        encrypt = encrypt + encrypter._encrypt_(char)
    return encrypt

@app.route("/",methods=["GET","POST"])
def index():
    global error
    global text
    global success
    if request.method == "POST":
        req = request.form
        pin = req["pin"]
        password = req["password"]
        if len(pin)!=4 or not pin.isnumeric():
            text = "Pin should be four digit number"
            error=True
        else:
            pin = int(pin)
            text = encrypt(pin, password)
            print("encrypted:",text )
            success = True
            error = False
        print(pin,password)
        return redirect(request.url)
    return render_template("index.html",reply=text, error=error, success=success)






if __name__ == "__main__":
    text = "Hello"
    error = False
    success = False
    # app.run(ssl_context=context)
    host="0.0.0.0"
    port = int(os.environ.get('PORT', 5000))
    app_server = gevent.pywsgi.WSGIServer((host,port),app)
    app_server.serve_forever()
    #app.run(threaded=True, port=port)