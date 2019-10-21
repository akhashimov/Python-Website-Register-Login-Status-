@web_app.route('/log-check', methods=['GET','POST'])
def check_login():
    em_adr=request.form['logcheck1']
    pswd=request.form['logcheck2']
    f = json.load(open('user-info.json', 'rt'))
    tresto = json.load(open('academic-info.json', 'wt'))
    for item in f:
        if em_adr== item['email'] and pswd==item['password']:
            usr_id=item['id']
            temporarydic=item
            for itemko in tresto:
                if itemko['email'] == em_adr:
                    acad_dict=itemko
                else:
                    return redirect('/log-error')
            portlet=uuid.uuid4()

            return redirect('/personal_account/',portlet=portlet,temporarydic=temporarydic,acad_dict=acad_dict)
    return redirect('/log-error/')

@web_app.route('/personal_account/')
def personal_account():
    return render_template('personal_account page 1.html')
@web_app.route('/personal_account/<portlet>/2')
def personal_account():
    return render_template('personal_account page 2.html')
@web_app.route('/personal_account/<portlet>/3')
def personal_account():
    return render_template('personal_account page 3.html')

def get_all_files(email,doctype):

            
