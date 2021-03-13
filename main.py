import os
from typing import TextIO
import time
from flask import Flask, request, render_template,redirect,send_from_directory
import random
from werkzeug.utils import secure_filename
import json
import shutil

web_app = Flask(__name__)
web_app.config['UPLOAD_FOLDER'] = 'user-data'

@web_app.route('/')
def main_page():
    return render_template('index.html')
@web_app.route('/why-ALU/')
def about():
    return render_template('why-gu.html')
@web_app.route('/admission/')
def admissions():
    return render_template('admission.html')
@web_app.route('/tuition-scholarships/')
def academics():
    return render_template('costs-aid.html')
@web_app.route('/programs')
def programs():
    return render_template('programs.html')
@web_app.route('/register-user',methods=['GET','POST'])
def reg_user():
    return render_template('reg_usr_page1.html')
@web_app.route('/register-user/academic',methods=['GET','POST'])
def reg_user2():
    return render_template('reg_usr_page2.html')



@web_app.route('/reg_check/',methods=['GET','POST'])
def reg_stage1():
    with open('user-info.json','rt') as json_file:
        recent_dict=json.load(json_file)
        print('json file read')
    if request.method == 'POST':
        em_adr = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        print('forms read')
        for item_of_dict in recent_dict:
            print('email check')
            if em_adr == item_of_dict['email']:
                del recent_dict
                return redirect('/reg-error/')
            print('email check successful')
            if fname == item_of_dict['firstname'] and lname == item_of_dict['lastname'] and dob == item_of_dict['dateofbirth']:
                print('name check')
                del recent_dict
                return redirect('/reg-error')
                print('name check successful')
        possible1 = random.randint(1000, 10000)
        possible2 = 0
        print('created possible')
        pswd = request.form['password']
        pswd_config = request.form['password2']
        if str(pswd)==str(pswd_config):
            print('passwords checked')
            if recent_dict != []:
                print('recent dics are not none')
                temp_list=[]
                print('running while')
                for k in recent_dict:
                    print('running through first object in recent dics')
                    temp_list.append(k['half_id'])
                while possible1 != possible2:
                    if str(possible1) in temp_list:
                       possible2=possible1
                       possible1=random.randint(1000,10000)
                    else:
                        possible2 = possible1


            half_id = str(possible1)
            print('half id set')
            user_info = {
                "firstname": request.form['fname'],
                "lastname": request.form['lname'],
                "dateofbirth": request.form['dob'],
                "email": request.form['email'],
                "address": request.form['stradr'],
                "city": request.form['city'],
                "phone1": request.form['phone1'],
                "phone2":request.form['phone2'],
                "password": request.form["password"],
                "start_year": request.form['stryear'],
                "half_id": half_id,
                "id": request.form['stryear'] + str(half_id)
            }
            print('user info set')
            recent_dict.append(user_info)
            print('user info added to recent dic')
            print(recent_dict)
            with open('user-info.json','wt') as json_file:
                print('json read')
                json.dump(recent_dict,json_file)
                print('json dumped')
            del recent_dict
            print('deleted dict')
            tresto = json.load(open('academic-info.json', 'rt'))
            gpa = None
            ielts_overall = None
            toefl_overall = None
            sat_read = None
            sat_math = None
            sat_overall = None
            academ = {
                "email": em_adr,
                'gpa': gpa,
                'ielts_overall': ielts_overall,
                'toefl_overall': toefl_overall,
                'sat_ebrw': sat_read,
                'sat_math': sat_math,
                'sat_overall': sat_overall
            }
            for itemko in tresto:
                if itemko["email"] == em_adr:
                    del itemko
            tresto.append(academ)
            json.dump(tresto, open('academic-info.json', 'wt'))

            with open('user-info.json', 'rt') as json_file:
                recent_dict = json.load(json_file)
            em_adr = request.form['email']
            if em_adr != '':
                with open('user-info.json', 'rt') as json_file:
                    recent_dict = json.load(json_file)
                for item_of_dict in recent_dict:
                    if em_adr == item_of_dict['email']:
                        idforfp = item_of_dict['id']
                try:
                    idforfp
                except:
                    idforfp = None

                if idforfp == None:
                    return redirect('/reg-error-notfound')
            file_exists = False
            newpath = str(
                os.path.join(os.path.dirname(__file__).replace('\\', '/')) + '/user-data/' + str(idforfp) + '/')
            if os.path.exists(newpath):
                file_exists = True
            diploma_path = str(
                os.path.join(os.path.dirname(__file__).replace('\\', '/')) + '/user-data/' + str(idforfp) + '/diploma')
            transcript_path = str(os.path.join(os.path.dirname(__file__).replace('\\', '/')) + '/user-data/' + str(
                idforfp) + '/transcript')
            ielts_path = str(
                os.path.join(os.path.dirname(__file__).replace('\\', '/')) + '/user-data/' + str(idforfp) + '/ielts')
            toefl_path = str(
                os.path.join(os.path.dirname(__file__).replace('\\', '/')) + '/user-data/' + str(idforfp) + '/toefl')
            sat_path = str(
                os.path.join(os.path.dirname(__file__).replace('\\', '/')) + '/user-data/' + str(idforfp) + '/sat')
            if file_exists == False:
                os.makedirs(newpath)
                os.makedirs(diploma_path)
                os.makedirs(transcript_path)
                os.makedirs(ielts_path)
                os.makedirs(toefl_path)
                os.makedirs(sat_path)

    return redirect('/register-user/academic')




@web_app.route('/reg_check2',methods=['GET','POST'])
def reg_check2():
    if request.method == 'POST':
        em_adr=request.form['email']
        if em_adr != '':
            with open('user-info.json','rt') as json_file:
                recent_dict= json.load(json_file)
            for item_of_dict in recent_dict :
                if em_adr == item_of_dict['email']:
                    idforfp=item_of_dict['id']
            try :
                idforfp
            except:
                idforfp = ''

            if idforfp == '':
                return redirect('/reg-error-notfound')
            file_exists=False
            newpath = str(os.path.join(os.path.dirname(__file__).replace('\\','/'))+'/user-data/'+ str(idforfp) + '/')
            if os.path.exists(newpath):
                file_exists=True
            try:
                transcript_file = request.files['transcript']
                transcript_form = str(request.files['transcript'].filename)
                print(transcript_form)
            except:
                print('no transcript provided')
                transcript_file = None
            try:
                ielts_file = request.files['ielts']
                ielts_form = str(request.files['ielts'].filename)
                print(ielts_form)
            except:
                ielts_file = None
                print('no ielts provided')
            try:
                toefl_file = request.files['toefl']
                toefl_form = str(request.files['toefl'].filename)
                print(toefl_form)
            except:
                toefl_file = None
                print('no toefl provided')
            try:
                sat_file = request.files['sat']
                sat_form = str(request.files['sat'].filename)
                print(sat_form)
            except:
                sat_file = None
                print('no sat provided')
            try:
                diploma_file = request.files['diploma']
                print(diploma_file)
                diploma_form = str(request.files['diploma'].filename)
                print(diploma_form)
            except:
                diploma_file = None
                print('no diploma provided')
            if transcript_form != '':
                transcript_file.save(
                    os.path.join(web_app.config['UPLOAD_FOLDER'], str(idforfp), "transcript", transcript_form))
            if ielts_form != '':
                ielts_file.save(os.path.join(web_app.config['UPLOAD_FOLDER'], str(idforfp), "ielts", ielts_form))
            if toefl_form != '':
                toefl_file.save(os.path.join(web_app.config['UPLOAD_FOLDER'], str(idforfp), "toefl", toefl_form))
            if sat_form != '':
                sat_file.save(os.path.join(web_app.config['UPLOAD_FOLDER'], str(idforfp), "sat", sat_form))
            if diploma_form != '':
                diploma_file.save(os.path.join(web_app.config['UPLOAD_FOLDER'], str(idforfp), "diploma", diploma_form))
        try:
            gpa = request.form['gpa']
        except:
            gpa = ''
        try:
            ielts_overall = request.form['iescore']
        except:
            ielts_overall = ''
        try:
            toefl_overall = request.form['toescore']
        except:
            toefl_overall = ''
        try:
            sat_read = request.form['satscore1']
            sat_math = request.form['satscore2']
            sat_overall = request.form['satscore3']
        except:
            sat_read = ''
            sat_math = ''
            sat_overall = ''
        tresto = json.load(open('academic-info.json', 'rt'))
        academ={
            "email":em_adr,
            'gpa':gpa,
            'ielts_overall':ielts_overall,
            'toefl_overall':toefl_overall,
            'sat_ebrw':sat_read,
            'sat_math':sat_math,
            'sat_overall':sat_overall
        }
        for itemko in tresto:
            if itemko["email"] == em_adr:
                del itemko
        tresto.append(academ)
        json.dump(tresto,open('academic-info.json','wt'))



        return redirect('/reg_success/')
    else:
        return redirect('/reg_check2')
@web_app.route('/reg_success/')
def reg_success():
    return render_template('reg_success.html')

@web_app.route('/reg-error-notfound')
def reg_error_nf():
    return render_template('reg-error-notfound.html')

@web_app.route('/reg-error/')
def reg_error():
    return render_template('reg-error-existing-account.html')
#Login part

@web_app.route('/login/', methods=['GET', 'POST'])
def login_pg():
    return render_template('login-page.html')
@web_app.route('/log-error/')
def log_error():
    return render_template('login-notfound.html')

def get_files_by_doctype(doctype,usr_id):
    files_list=[]
    for filename in os.listdir(str(os.path.join(os.path.dirname(__file__).replace('\\','/')+'/user-data/'+str(usr_id)+"/"+str(doctype)))):
        files_list.append(filename)
    return files_list

@web_app.route('/personal_account/', methods=['GET','POST'])
def check_login():
    em_adr=request.form['logcheck1']
    pswd=request.form['logcheck2']
    f = json.load(open('user-info.json', 'rt'))
    tresto = json.load(open('academic-info.json', 'rt'))
    for item in f:
        if em_adr== item['email'] and pswd==item['password']:
            usr_id=item['id']
            print(usr_id)
            temporarydic=item
            for itemko in tresto:
                if itemko["email"] == em_adr:
                    acad_dict=itemko
                    if acad_dict == None:
                        acad_dict = {
                            'gpa':'0',
                            'ielts_overall':'0',
                            'toefl_overall':'0',
                            'sat_ebrw':'0',
                            'sat_math':'0',
                            'sat_overall':'0'
                        }
            try:
                acad_dict
            except NameError:
                return redirect('/log-error')
            return personal_account(usr_id,temporarydic,acad_dict)
    return redirect('/log-error/')

#personal account part
@web_app.route('/personal_account1/<username>')
def personal_account(username,temporarydict,acad_dictionary):
    return render_template('personal_account page 1.html',temporarydict=temporarydict,acad_dict=acad_dictionary,usr_id=username,files_list1=get_files_by_doctype("diploma",username),files_list2=get_files_by_doctype("transcript",username),files_list3=get_files_by_doctype("ielts",username),files_list4=get_files_by_doctype("toefl",username),files_list5=get_files_by_doctype("sat",username))
@web_app.route('/personal_account2/')
def personal_account2():
    return render_template('personal_account page 2.html')
@web_app.route('/personal_account3/')
def personal_account3():
    return render_template('personal_account page 3.html')

@web_app.route('/file/<usr_id>/<doctype>/<whatsyourname>', methods=['GET', 'POST'])
def show_file(whatsyourname,doctype,usr_id):
    return send_from_directory(str(os.path.join(os.path.dirname(__file__).replace('\\','/'))+'/user-data/'+str(usr_id)+"/"+str(doctype)+"/"),str(whatsyourname))

@web_app.route('/<usr_id>/<doctype>/<whatsyourname>', methods=['GET', 'POST'])
def delete_file():
    if request.method==["POST"]:
        shutil.move()
        return redirect()
#@web_app.route()
#def
if __name__ == "__main__":
    web_app.run(debug=True)
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
#This is a comment
