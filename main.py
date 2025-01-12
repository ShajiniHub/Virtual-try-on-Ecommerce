from flask import Flask, render_template, request, jsonify, redirect, url_for, Response,session
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from skimage.filters import gaussian
from test import evaluate
import os
import datetime
import mysql.connector
from flask import send_file
from nltk.stem import PorterStemmer
import re
import json
from wordcloud import STOPWORDS

import webcolors
from flask import request as flask_request


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'abcdef'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    database="lips"
)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/',methods=['POST','GET'])
def index():

    
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():

    msg=""
    if flask_request.method == 'POST':
        username = flask_request.form['username']
        password = flask_request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"  
        else:
            msg="fail"

    return render_template('login.html', msg=msg)




@app.route('/register',methods=['POST','GET'])
def register():
    
    msg=""
    st=""
    username=""
    password=""
    name=""
    email=""
    mess=""
    if flask_request.method=='POST':
        name=flask_request.form['name']
        mobile=flask_request.form['mobile']
        email=flask_request.form['email']
        username=flask_request.form['username']
        password=flask_request.form['password']
        now = datetime.datetime.now()
        reg_date=now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM user where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO user(id, name, mobile, email, username, password, reg_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, mobile, email, username, password, reg_date)
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            st="1"
            mess = f"Reminder: Hi {name}, your username is {username} and password is {password}!"
            mycursor.close()
        else:
            msg="fail"
  
    return render_template('register.html', msg=msg, email=email, mess=mess, st=st, username=username, password=password, name=name)


################################################################################################

def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)

def hair(image, parsing, part=17, color=[230, 50, 20]):
    if len(color) != 3:
        raise ValueError("Color must be a list of three values: [blue, green, red]")

    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part == 12 or part == 13:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    changed[parsing != part] = image[parsing != part]
    return changed

def apply_lip_color(image_path, lipstick_color):
    cp = 'cp/79999_iter.pth'
    image = cv2.imread(image_path)
    parsing = evaluate(image_path, cp)
    parsing = cv2.resize(parsing, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    table = {
        'upper_lip': 12,
        'lower_lip': 13
    }

    parts = [table['upper_lip'], table['lower_lip']]

    colors = [lipstick_color, lipstick_color]  # Use the selected lipstick color for both upper and lower lips

    for part, color in zip(parts, colors):
        image = hair(image, parsing, part, color)

    return image



def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    bgr_color = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))
    return list(bgr_color)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if flask_request.method == 'POST':
        if 'file' in flask_request.files:
            file = flask_request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                lipstick_color_hex = flask_request.form['favcolor']  # Get the selected lipstick color from the form as a hex string
                lipstick_color = hex_to_bgr(lipstick_color_hex)  # Convert hex color to BGR
                result_image = apply_lip_color(file_path, lipstick_color)
                cv2.imwrite(file_path, result_image)
                return redirect(url_for('download_result', filename=filename))

    return render_template('upload.html')

@app.route('/download/<filename>')
def download_result(filename):
    # Construct the full path to the result image
    result_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Return the result image as a file attachment
    return send_file(result_file_path, as_attachment=True)




###########################################################################


def stream():
    global cap
    cap=cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            print("Frame shape:", frame.shape)  # Print frame shape for debugging
            imgencode=cv2.imencode('.jpg',frame)[1]
            strinData = imgencode.tostring()
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+strinData+b'\r\n')
        else:
            print("Failed to capture frame from webcam")
def stop():
    global cap
    if cap.isOpened():
        cap.release()

   


@app.route('/webcam')
def webcam():
    # Video streaming route. Put this in the src attribute of an img tag
    
    
    return Response(stream(),mimetype='multipart/x-mixed-replace;boundary=frame')



@app.route('/video', methods=['POST', 'GET'])
def video():
    result_filename=""
    if flask_request.method == 'POST':
        if 'capture' in flask_request.form:
            lipstick_color_hex = flask_request.form['favcolor']
            lipstick_color = hex_to_bgr(lipstick_color_hex)

            # Capture image from webcam
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            # Save the captured image
            filename = 'captured_image.jpg'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            cv2.imwrite(file_path, frame)

            # Apply lipstick color to the captured image
            result_image = apply_lip_color(file_path, lipstick_color)

            # Save the result image
            result_filename = 'result_image.jpg'
            result_file_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
            cv2.imwrite(result_file_path, result_image)

            # Redirect to the uploaded file page
            return redirect(url_for('download_result', filename=result_filename))

    return render_template('video.html', filename=result_filename)



####################################################################################################################

def hex_to_name(hex_code):
    try:
        return webcolors.hex_to_name(hex_code)
    except ValueError:
        return "Unknown Color"





@app.route('/add_product',methods=['POST','GET'])
def add_product():

    if 'username' not in session or session.get('user_type') != 'admin':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('admin'))

    username = session.get('username')
    
    msg=""
    if flask_request.method=='POST':
        favcolor=flask_request.form['favcolor'] 

        # Convert the hexadecimal color code to color name
       

        price=flask_request.form['price']
        pname=flask_request.form['pname']
        if 'file' in flask_request.files:
            file = flask_request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = 'E:/lipstick_ecommerce/static/uploads/' + filename
                file.save(image_path)
                now = datetime.datetime.now()
                reg_date=now.strftime("%Y-%m-%d")
        
                mycursor = mydb.cursor()
        
                mycursor.execute("SELECT max(id)+1 FROM products")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO products(id, file, favcolor, price, username, reg_date, pname) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (maxid, filename, favcolor, price, username, reg_date, pname)
                mycursor.execute(sql, val)
                mydb.commit()

                msg="success"
                
            else:
                msg="fail"
  
    return render_template('add_product.html', msg=msg)



@app.route('/add_query',methods=['POST','GET'])
def add_query():

    if 'username' not in session or session.get('user_type') != 'admin':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('admin'))

    username = session.get('username')
    
    msg=""
    if flask_request.method=='POST':
        inputt=flask_request.form['input']
        output=flask_request.form['output']
        
        now = datetime.datetime.now()
        reg_date=now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        
        mycursor.execute("SELECT max(id)+1 FROM cc_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO cc_data(id, input, output) VALUES (%s, %s, %s)"
        val = (maxid, inputt, output)
        mycursor.execute(sql, val)
        mydb.commit()

        msg="success"
                
    else:
        msg="fail"
  
    return render_template('add_query.html', msg=msg)


@app.route('/view', methods=['GET', 'POST'])
def view():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login'))

    
    username=session.get('username')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM products")
    data3 = cursor.fetchall()
    cursor.close()

    if flask_request.method == 'POST':
    
        color = flask_request.form.get('color')
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM products WHERE favcolor LIKE %s", ('%' + color + '%',))
        data3 = cursor.fetchall()
        cursor.close()

    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    data = cursor.fetchone()
    cursor.close()
    name=data[1]
    mobile=data[2]
    email=data[3]
    act=flask_request.args.get("act")
    if act=="ok":
        
        pid=flask_request.args.get("pid")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (pid,))
        data8 = cursor.fetchone()
        cursor.close()
        pro_username=data8[5]
        color=data8[2]
        price=data8[3]
        now = datetime.datetime.now()
        req_date=now.strftime("%B %d, %Y")
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM book")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO book(id, name, mobile, email, pro_username, color, price, req_date, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, name, mobile, email, pro_username, color, price, req_date, username)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        session['maxid'] = maxid

        
        return redirect(url_for('quantity', maxid=maxid))

    else:

        msg="fail"

    

    return render_template('view.html', products=data3)

@app.route('/quantity', methods=['GET', 'POST'])
def quantity():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login'))

    
    maxid=session.get('maxid')
    if flask_request.method=='POST':
        quantity=flask_request.form['quantity']
        

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM book where id = %s",(maxid,))
        data1 = cursor.fetchone()
        cursor.close()
        price=data1[6]

        quantity = int(quantity)
        price = float(price)

        total=quantity*price
        
        cursor = mydb.cursor()
        cursor.execute("update book set quantity=%s, total=%s where id=%s",(quantity, total, maxid))
        mydb.commit()
        return redirect(url_for('payment', maxid=maxid))

    return render_template('quantity.html', maxid=maxid)




@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login'))

    msg=""
    total=""
    st=""
    mess=""
    mobile=""
    name=""
    maxid=session.get('maxid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM book where id = %s",(maxid,))
    data1 = cursor.fetchone()
    cursor.close()
    total=data1[10]

    

    if flask_request.method=='POST':
        payment=flask_request.form['payment']
        
        cursor = mydb.cursor()
        cursor.execute("update book set payment=%s where id=%s",(payment, maxid))
        mydb.commit()
        msg="success"

    return render_template('payment.html', maxid=maxid, msg=msg, total=total)


@app.route('/view_booking', methods=['GET', 'POST'])
def view_booking():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login'))

    
    username=session.get('username')
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM book WHERE username = %s", (username,))
    data = cursor.fetchall()
    cursor.close()

    return render_template('view_booking.html', book=data)




@app.route('/view_order', methods=['GET', 'POST'])
def view_order():
    if 'username' not in session or session.get('user_type') != 'admin':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('admin '))

    
    username=session.get('username')
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM book")
    data2 = cursor.fetchall()
    cursor.close()

    return render_template('view_order.html', book=data2)

@app.route('/admin',methods=['POST','GET'])
def admin():

    msg=""
    if flask_request.method == 'POST':
        username = flask_request.form['username']
        password = flask_request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'admin'
            msg="success"  
        else:
            msg="fail"

    
    return render_template('admin.html', msg=msg)


##############################################################EXTRA#######################################################


@app.route('/request', methods=['GET', 'POST'])
def request():
    if 'username' not in session or session.get('user_type') != 'user':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login'))

    msg=""
    total=""
    st=""
    mess=""
    mobile=""
    name=""
    username=session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM user where username = %s",(username,))
    data = cursor.fetchone()
    cursor.close()
    mobile=data[2]
    email=data[3]

    if flask_request.method=='POST':
        request=flask_request.form['request']
        now = datetime.datetime.now()
        date=now.strftime("%B %d, %Y")
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO request(id, request, mobile, email, username, date) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid, request, mobile, email, username, date)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"

    return render_template('request.html', msg=msg)


@app.route('/view_request', methods=['GET', 'POST'])
def view_request():
    msg=""
    mess=""
    st=""
    mobile=""
    username=""
    act=flask_request.args.get('act')
    cursor = mydb.cursor()

    cursor.execute('SELECT * FROM request')
    data = cursor.fetchall()
            

    if act=="ok":
        sid=flask_request.args.get("sid")
        cursor.execute('SELECT * FROM request where id=%s',(sid,))
        d1 = cursor.fetchone()
        mobile=d1[2]
        cursor.execute("update request set status=1 where id=%s",(sid,))
        mydb.commit()
        st="1"
        mess=f"Alert: Please Check, Your Request Has Been Accepted Sucessfully."

    
    if act=="del":
        did=flask_request.args.get("did")
        cursor.execute("delete from request where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_request'))     

    return render_template('view_request.html',msg=msg,data=data, mess=mess, mobile=mobile, st=st, username=username)

@app.route('/bot', methods=['GET', 'POST'])
def bot():
    msg=""
    output=""
    uname=""
    mm=""
    s=""
    xn=0
    if 'username' in session:
        uname = session['username']
    
    cnt=0
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM user where username=%s",(uname, ))
    value = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM cc_data")
    data=mycursor.fetchall()
            
    if flask_request.method=='POST':
        msg_input=flask_request.form['msg_input']
        
        text=msg_input
        ##
        
        #nlp=STOPWORDS
        #def remove_stopwords(text):
        #    clean_text=' '.join([word for word in text.split() if word not in nlp])
        #    return clean_text
        ##
        #txt=remove_stopwords(msg_input)
        ##
        stemmer = PorterStemmer()
    
        from wordcloud import STOPWORDS
        STOPWORDS.update(['rt', 'mkr', 'didn', 'bc', 'n', 'm', 
                          'im', 'll', 'y', 've', 'u', 'ur', 'don', 
                          'p', 't', 's', 'aren', 'kp', 'o', 'kat', 
                          'de', 're', 'amp', 'will'])

        def lower(text):
            return text.lower()

        def remove_specChar(text):
            return re.sub("#[A-Za-z0-9_]+", ' ', text)

        def remove_link(text):
            return re.sub('@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+', ' ', text)

        def remove_stopwords(text):
            return " ".join([word for word in 
                             str(text).split() if word not in STOPWORDS])

        def stemming(text):
            return " ".join([stemmer.stem(word) for word in text.split()])

        #def lemmatizer_words(text):
        #    return " ".join([lematizer.lemmatize(word) for word in text.split()])

        def cleanTxt(text):
            text = lower(text)
            text = remove_specChar(text)
            text = remove_link(text)
            text = remove_stopwords(text)
            text = stemming(text)
            
            return text

        

        #show the clean text
        #dat=df.head()
        #data=[]
        #for ss in dat.values:
        #    data.append(ss)
        #msg_input=data
        #####################
        mm='%'+msg_input+'%'
        
        mycursor.execute("SELECT count(*) FROM cc_data where input like %s || output like %s",(mm,mm))
        cnt=mycursor.fetchone()[0]
        if cnt>0:
            
            mycursor.execute("SELECT * FROM cc_data where input like %s || output like %s",(mm,mm))
            dd=mycursor.fetchone()
            print(dd[2])
            
            output=dd[2]

        else:
            if msg_input=="":
                
                output="How can i help you?"
            else:
                
                output="Sorry, No Results Found!"


        
        return json.dumps(output)


    return render_template('bot.html', msg=msg,output=output,uname=uname,cc_data=data,value=value)   




@app.route('/logout')
def logout():
    
    session.clear()
    print("Logged out successfully", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    



