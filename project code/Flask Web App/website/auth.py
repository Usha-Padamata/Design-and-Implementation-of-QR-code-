from flask import Flask,Blueprint,render_template,request,flash,redirect,url_for,send_from_directory
import math, random
import qrcode
from PIL import Image
from PIL import Image, ImageDraw
import os, sys
from random import SystemRandom
from flask_mail import Mail,Message
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

global k

app=Flask('flaskapp')

app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "maddi.kundana3@gmail.com"
app.config['MAIL_PASSWORD'] = "bsii mhgh uohq ijgw"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['UPLOAD_FOLDER'] = "static"

auth = Blueprint('auth','flaskapp')



mail=Mail(app)

class UploadFileForm(FlaskForm):
    file =FileField("File",validators=[InputRequired()])
    submit = SubmitField("Submit")



@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        rollno = request.form.get("rollno")
        


# length of password can be changed
# by changing value in range
	
        if(rollno == '19KT1A0533'):
            flash("Mail has sent to saikundana2002@gmail.com")
            digits = "0123456789"
            global OTP
            OTP=''
            for i in range(4) :
                OTP += digits[math.floor(random.random() * 10)]
            print(OTP)
            k=OTP
            print(k)
            a = qrcode.make(OTP)# Saving as an image file
            a.save('a.png')
            #-----------------------------------------------------------------
            #----------------------------------------------------------------- 
            img = Image.open("a.png")


            f,e= os.path.splitext("a.png")
            out_filename_A=f+"_A.png"
            out_filename_B=f+"_B.png"

            img=img.convert('1')#convert image to 1 bit
            
            #Prepare two empty slider images for drawing
            width=img.size[0]*2
            height=img.size[1]*2
            out_image_A = Image.new('1', (width, height))
            out_image_B = Image.new('1', (width, height))
            draw_A = ImageDraw.Draw(out_image_A)
            draw_B = ImageDraw.Draw(out_image_B)
            print("12345")
            
            #There are 6(4 choose 2) possible patterns and it is too late for me to think in binary and do these efficiently
            patterns=((1,1,0,0), (1,0,1,0), (1,0,0,1), (0,1,1,0), (0,1,0,1), (0,0,1,1))
            #Cycle through pixels

            for x in range(0, width//2):
                for y in range(0, height//2):
                    pixel=img.getpixel((x,y))
                    pat=random.choice(patterns)
                    #A will always get the pattern
                    draw_A.point((x*2, y*2), pat[0])
                    draw_A.point((x*2+1, y*2), pat[1])
                    draw_A.point((x*2, y*2+1), pat[2])
                    draw_A.point((x*2+1, y*2+1), pat[3])
                    if pixel==0:#Dark pixel so B gets the anti pattern
                        draw_B.point((x*2, y*2), 1-pat[0])
                        draw_B.point((x*2+1, y*2), 1-pat[1])
                        draw_B.point((x*2, y*2+1), 1-pat[2])
                        draw_B.point((x*2+1, y*2+1), 1-pat[3])
                    else:
                        draw_B.point((x*2, y*2), pat[0])
                        draw_B.point((x*2+1, y*2), pat[1])
                        draw_B.point((x*2, y*2+1), pat[2])
                        draw_B.point((x*2+1, y*2+1), pat[3])
            out_image_A.save("C:/Users/DELL/OneDrive/Desktop/Flask Web App/website/static/share1.jpg" , 'JPEG')
            out_image_B.save("C:/Users/DELL/OneDrive/Desktop/Flask Web App/website/static/share2.jpg", 'JPEG')
            out_image_A.show()
            out_image_B.show()

    
            message = Message(OTP,sender="maddi.kundana3@gmail.com",recipients = ['saikundana2002@gmail.com'])
            message.body = "Sending email"

            mail.send(message)

            print("Done.")
            
            return redirect(url_for('auth.merge'))
        else:
            flash("User is not registered")
        print(rollno)
        
    return render_template("login.html")



@auth.route('/logout')
def logout():
    return "<h1><center><b> LogOut </b></center></h1>"

@auth.route('/verification',methods=['GET','POST'])
def verification():
        
    img1 = Image.open("C:/Users/DELL/OneDrive/Desktop/Flask Web App/website/static/share1.jpg")
    img2 = Image.open("C:/Users/DELL/OneDrive/Desktop/Flask Web App/website/static/share2.jpg")
    img1.paste(img2, (0,0), mask = img2)
    img1.show()
    img1.save('C:/Users/DELL/OneDrive/Desktop/Flask Web App/website/static/final.png','PNG')

    print("completed")
    if request.method == "POST":
        otp = request.form.get("otp")
        if otp == OTP:
            flash("Successfully logged In")
        else:
            flash("OTP is incorrect")
    return render_template("verification.html")

@auth.route('/merge',methods=['GET','POST'])
def merge():
    form  = UploadFileForm()
    if form.validate_on_submit():
        file= form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return redirect(url_for('auth.verification'))
    
    return render_template('merge.html',form=form)

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4:
            flash("Email must be greater than 4 characters.",category="error")
        elif len(firstName) < 2:
            flash("First Name should be greater than 2  characters",category="error")
        elif len(password1) < 7:
            flash("password must be atleast 7 characters .",category ="error")
        elif password1 != password2 :
            flash("Passwords does not match",category = "error")
        else:
            flash("Account Created",category = "success")

    return render_template("sign_up.html")