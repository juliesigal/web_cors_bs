from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from customers import Customers
from db_repo import DbRepo
from db_config import local_session


app = Flask(__name__)
CORS(app)
repo = DbRepo(local_session)

def convert_to_json(_list: list):
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list

@app.route("/")
def home():
    return render_template('index2.html')


# url/<resource> <--- GET POST
@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    if request.method == 'GET':
        return jsonify(convert_to_json(repo.get_all_customers()))
    if request.method == 'POST':
        customer_data = request.get_json()
        new_customer = Customers(id=None, name=customer_data["name"], address=customer_data["address"])
        repo.add(new_customer)
        return_ls = []
        customers = repo.get_all_customers()
        for customer in customers:
            return_ls.append({"id": customer.id, "name": customer.name, "address": customer.address})
        return jsonify(return_ls)

@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_customer_by_id(id):
    global customers
    if request.method == 'GET':
        for c in customers:
            if c["id"] == id:
                return jsonify(c)
        return '{}'

    if request.method == 'PUT':
        updated_new_customer = request.get_json()
        for c in customers:
            if c["id"] == id:
                c["id"] = updated_new_customer["id"] if "id" in updated_new_customer.keys() else None
                c["name"] = updated_new_customer["name"] if "name" in updated_new_customer.keys() else None
                c["address"] = updated_new_customer["address"] if "address" in updated_new_customer.keys() else None
                return jsonify(updated_new_customer)
        customers.append(updated_new_customer)
        return jsonify(updated_new_customer)

    if request.method == 'DELETE':
        repo.delete_customer_by_id(id)
        return_ls = []
        customers = repo.get_all_customers()
        for customer in customers:
           return_ls.append({"id": customer.id, "name": customer.name, "address": customer.address})
        return jsonify(return_ls)


app.run()