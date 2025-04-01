import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from database import intidb, database1
from utils.uuid import generate_code
from Auth.register import customer_register, admin_register, professional_register
from Auth.login import customer_login, professional_login, admin_login_function
from Auth.verify import customer_block_status, professionals_block_status, recheck_email, professional_approv_check
from services.dashboard.customer_dashboard import customer_dashboard_functions, get_service_info, get_sub_service, close_my_service, service_close, customer_info
from services.dashboard.admin_dashboard import add_service, get_all_services_details, list_all_props, pdf_data_return, professional_approv, list_all_service_status
from services.recieve_information import retrive_customer_info, retrive_service_info, main_service_name, sub_service_name
from services.service_init import service_intilization, get_service_status
from services.dashboard.professional_dashboard import professional_dashboard_functions, find_service_for_me, my_service_type, prof_number, accept, my_services, rejected_service, prof_profile 
from services.query.search_service import customer_search, prof_search, admin_search

app = Flask(__name__)
app.secret_key = "Mad-1 Project"


intidb()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/templates/stack/<path:filename>')
def serve_image(filename):
    return send_from_directory('templates/stack', filename)


@app.route('/register', methods=['GET','POST'])
def register_customer():
    if request.method=='POST':
        id = generate_code()
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        mb_no = request.form.get('mb_no')
        address = request.form.get('address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')

        if id and full_name and email and password and mb_no and address and city and pincode:
            success = customer_register(id, full_name, email, password, mb_no, address, city, pincode)
            return redirect(url_for('login_customer'))
    return render_template('customer_register.html')

@app.route('/admin/register', methods=['GET','POST'])
def register_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            admin_register(email, password)
            return redirect(url_for('admin_login'))
    return render_template('admin_register.html')

@app.route('/professionals/register', methods=['GET','POST'])
def register_professionals():
    name_or_type = request.args.get('name_or_type')
    main_services = main_service_name()
    if request.method=='POST':
        id = generate_code()
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        mb_no = request.form.get('mb_no')
        address = request.form.get('address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        id_proof = request.files.get('id_proof')  
        service_type = request.form.get('service_type')
        experience = request.form.get('experience')

        main_service_type = eval(service_type)[0]
        speciality = eval(service_type)[1]
        
        prev_status = recheck_email(email)
        if prev_status:
            if id and full_name and email and password and mb_no and address and city and pincode and id_proof and main_service_type and speciality and experience:
                success = professional_register(id, full_name, email, mb_no, password, address, city, pincode, id_proof, main_service_type, speciality, experience)
                return redirect(url_for('login_professionals'))
        else:
            return 'Email is already Present, Please Login '
        
    if name_or_type is not None:
        sub_services = sub_service_name(name_or_type)
        print(sub_services)
        return render_template('professionals_register.html', sub_services=sub_services)    


    return render_template('professionals_register.html', main_services=main_services)    

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            found, admin_id = admin_login_function(email, password)
            if found:
                return redirect(url_for('admin_dashboard', admin_id=admin_id)) 
    return render_template('admin_login.html')


@app.route('/login', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            block_status = customer_block_status(email)
            if block_status:
                found, customer_id = customer_login(email, password)
                if found:
                    return redirect(url_for('customer_dashboard', customer_id=customer_id))


    return render_template('customer_login.html')


@app.route('/professionals/login', methods=['GET', 'POST'])
def login_professionals():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            block_status = customer_block_status(email)
            if block_status:
                professional_approv_status = professional_approv_check(email)
                if professional_approv_status:
                    found, professional_id = professional_login(email, password)
                    if found:
                        return redirect(url_for('professional_dashboard', professional_id=professional_id)) 
                else:
                    return 'Current You are Not Approved'
            return 'Something is Fissy' 
    return render_template('professional_login.html')

@app.route('/professional_dashboard')
def professional_dashboard():
    professional_id = request.args.get('professional_id')
    service_init_id = request.args.get('service_init_id')
    status = request.args.get('status')
    professional_name = None
    if professional_id:
        professional_name = professional_dashboard_functions(professional_id)
        
        p_no = prof_number(professional_id)
        s_t = my_service_type(professional_id)
        available_services = find_service_for_me(s_t[0], professional_id)
        aval_ser = None

        if service_init_id is not None and status is not None and status == 'Accept':

            accepted_service = accept(service_init_id, professional_name, professional_id, status, p_no[0])
        if service_init_id is not None and status is not None and status == 'Reject':
            rejected_service(service_init_id, professional_id)
        myservice = my_services(professional_id)
        return render_template("professional_dashboard.html", 
                           professional_id=professional_id, 
                           professional_name=professional_name, 
                           available_services=available_services,
                           myservice=myservice)
    else:
        return redirect(url_for('login_professionals'))


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    admin_id = request.args.get('admin_id')
    
    prof_id = request.args.get('id')
    services = get_all_services_details()
    fid = list_all_props()
    service_logs = list_all_service_status() 
    if prof_id:
        professional_approv(prof_id)
        return render_template('admin_dashboard.html', services=services, profs=fid, service_logs=service_logs) 
    return render_template('admin_dashboard.html', services=services, profs=fid, service_logs=service_logs ) 

@app.route('/profile')
def profile():
    customer_id = request.args.get('customer_id')
    professional_id = request.args.get('professional_id')

    if customer_id:
        customer_name = customer_dashboard_functions(customer_id)
        customer_details = customer_info(customer_id)
        return render_template('profile.html',
         customer_id=customer_id,
         customer_name=customer_name,
         customer_detail=customer_details)
    
    if professional_id:
        professional_name = professional_dashboard_functions(professional_id)
        prof_details = prof_profile(professional_id)
        return render_template('profile.html',
         professional_id=professional_id,
         professional_name=professional_name,
         prof_details=prof_details)
    
    return render_template('profile.html')


@app.route('/customer_dashboard')
def customer_dashboard():
    customer_id = request.args.get('customer_id')
    name_or_type = request.args.get('name_or_type')
    service_id_for_book = request.args.get('service_id_for_book')
    status = request.args.get('status')

    customer_name = None

    if customer_id:
        customer = customer_dashboard_functions(customer_id)
        if customer:
            customer_name = customer
        else:
            return render_template('customer_dashboard.html', error="Customer not found")

    main_services = get_service_info()

    unique_service_init_id = generate_code()
    customer_status = "init"
    service_intilization(unique_service_init_id, customer_status, 
                         retrive_service_info(service_id_for_book), 
                         retrive_customer_info(customer_id))

    service_info = get_service_status(customer_id)

    list_subservices = None
    if name_or_type:
        list_subservices = get_sub_service(name_or_type)

    if status is not None: 
        results = close_my_service(service_id_for_book, status)
        return redirect(url_for('customer_dashboard', customer_id=customer_id))
    
    my_prev_service  = service_close(customer_id)
    return render_template('customer_dashboard.html',
                           customer_id=customer_id,
                           customer_name=customer_name,
                           main_services=main_services,
                           list_subservices=list_subservices,
                           service_info=service_info,
                           prev_service= my_prev_service)



@app.route('/download/pdf/<id>')
def download_pdf(id):
    pid = id
    pdf_data = pdf_data_return(pid)      
    file_path = f'Data/id_proof_{id}.pdf'  
    with open(file_path, 'wb') as file:
        file.write(pdf_data[0][0])
    response = send_file(file_path, as_attachment=True, download_name=f'id_proof_{id}.pdf', mimetype='text/plain') 
    return response




@app.route('/service_add', methods=['POST'])
def service_add():
    if request.method == 'POST':
        id = generate_code()  
        name_or_type = request.form.get('name_or_type')
        sub_type = request.form.get('sub_type')
        description = request.form.get('description')
        base_price = request.form.get('base_price')

        if name_or_type and sub_type and description and base_price:
            add_service(id, name_or_type, sub_type, description, base_price)

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/search')
def adminsearch():
    admin_search_param = request.args.get('admin_search_param')
    admin_query = request.args.get('query')
    if admin_search_param is not None:
        a_input_accept = admin_search_param
        if admin_query is not None:
            admin_result, column_names = admin_search(admin_search_param, admin_query)
            Result = True
            return render_template(
                'admin_search.html', 
                a_input_accept=a_input_accept,
                Result=Result, 
                admin_result=admin_result, 
                column_names=column_names,
                col_len=len(column_names))

        return render_template('admin_search.html',  a_input_accept=a_input_accept)

    return render_template('admin_search.html')

@app.route('/search')
def search():
    customer_id = request.args.get('customer_id')
    professional_id = request.args.get('professional_id')
    customer_search_param = request.args.get('customer_search_param')
    prof_search_param = request.args.get('prof_search_param')
    customer_query = request.args.get('customer_query')
    professional_query = request.args.get('prof_query')

    if professional_id is not None:
        professional_name = professional_dashboard_functions(professional_id)
        if prof_search_param:
            p_input_accept = prof_search_param
            if professional_query is not None:
                professional_search_result = prof_search(professional_id, prof_search_param, professional_query)
                return render_template('search.html', professional_id=professional_id, professional_name=professional_name, p_input_accept=p_input_accept, professional_search_result=professional_search_result, )
            return render_template('search.html', professional_id=professional_id, professional_name=professional_name, p_input_accept=p_input_accept )

        return render_template('search.html', professional_id=professional_id, professional_name=professional_name)
    
    
    if customer_id is not None:
        customer_name = customer_dashboard_functions(customer_id)
        if customer_search_param:  
            input_accept = customer_search_param
            if customer_query is not None:
                customer_search_result = customer_search(customer_id, customer_search_param, customer_query)
                return render_template('search.html', customer_id=customer_id, customer_name=customer_name, customer_search_result=customer_search_result, )
            
            return render_template('search.html', customer_id=customer_id, customer_name=customer_name, input_accept=input_accept)

        return render_template('search.html', customer_id=customer_id, customer_name=customer_name)
    
    return render_template('search.html')



if __name__ == '__main__':
    app.run(debug=True)