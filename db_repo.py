from customers import Customers


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def get_customer_by_id(self, id_to_get):
        return self.local_session.query(Customers).get(id_to_get).all()

    def get_all_customers(self):
        return self.local_session.query(Customers).all()

    def add(self, customer):
        self.local_session.add(customer)
        self.local_session.commit()

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()

    # def get_user_by_username(self, value):
    #     return self.local_session.query(Customers).filter(Customers.username == value).all()

    # def get_user_by_email(self, value):
    #     return self.local_session.query(Users).filter(Users.email == value).all()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def delete_customer(self, customer):
        self.local_session.query(Customers).filter(Customers.id == customer.id).delete(synchronize_session=False)
        self.local_session.commit()

    def delete_customer_by_id(self, id_to_remove):
        self.local_session.query(Customers).filter(Customers.id == id_to_remove).delete(synchronize_session=False)
        self.local_session.commit()

    def put_by_id(self, id_to_update, data):
        exist_object = self.local_session.query(Customers).filter(Customers.id == id_to_update)
        if not exist_object:
            self.local_session.add(exist_object)
        exist_object.update(data)
        self.local_session.commit()

    def patch_by_id(self, id_column_name, id_to_update, data):
        exist_object = self.local_session.query(Customers).filter(id_column_name == id_to_update)
        if not exist_object:
            return
        exist_object.update(data)
        self.local_session.commit()

    def drop_all_tables(self):
        self.local_session.execute('drop TABLE customers CASCADE')
        self.local_session.commit()

    def reset_db(self):
        self.add_all([Customers(name='Dave', address='New York'),
                      Customers(name='Natalie', address='New Jersey'),
                      Customers(name='Julie', address='California'),
                      Customers(name='Angel', address='Colorado'),
                      Customers(name='Piter', address='Los Angeles')])


