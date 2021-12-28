from faker import Faker

fake = Faker()

class DefaultValues:
    # ==============================================
    # Users
    # ==============================================
    PRIVILEGED_USERS = [{
            'firstname': 'Ding',
            'lastname': fake.last_name(),
            'username': 'ding',
            'password': 'staycurious',
            'role': 'service_writer'
        }, 
        {
            'firstname': 'Om',
            'lastname': fake.last_name(),
            'username': 'om',
            'password': 'beproductive',
            'role': 'manager'
        }, 
        {
            'firstname': 'Yinan',
            'lastname': fake.last_name(),
            'username': 'yinan',
            'password': 'simplyawesome',
            'role': 'sales_person'
        }, 
        {
            'firstname': 'Leo',
            'lastname': fake.last_name(),
            'username': 'leo',
            'password': 'markthisday',
            'role': 'sales_person'
        }, 
        {
            'firstname': 'Rolan',
            'lastname': fake.last_name(),
            'username': 'rolan',
            'password': 'imtheceo',
            'role': 'owner'
        }, 
        {
            'firstname': 'Luis',
            'lastname': fake.last_name(),
            'username': 'luis',
            'password': 'wh4t3v3r',
            'role': 'inventory_clerk'
        }
    ]

    # ==============================================
    # Colors
    # ==============================================
    AVAILABLE_COLORS = [
        'Aluminum',
        'Beige',
        'Black',
        'Blue',
        'Brown',
        'Bronze',
        'Claret',
        'Copper',
        'Cream',
        'Gold',
        'Gray',
        'Green',
        'Maroon',
        'Metallic',
        'Navy',
        'Orange',
        'Pink',
        'Purple',
        'Red',
        'Rose',
        'Rust',
        'Silver',
        'Tan',
        'Turquoise',
        'White',
        'Yellow'
    ]