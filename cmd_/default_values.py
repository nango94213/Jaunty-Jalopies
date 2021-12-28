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

    # ==============================================
    # Vehicle Types
    # ==============================================
    AVAILABLE_VEHICLE_TYPES = [
        'SUV',
        'Van',
        'Truck',
        'Convertible',
        'Car'
    ]

    # ==============================================
    # Vehicle Type Attributes
    # ==============================================
    # SUV
    # https://www.motorbiscuit.com/these-7-cars-have-more-cupholders-than-youll-ever-need/)
    NUMBER_OF_CUP_HOLDERS_OPTIONS = [number for number in range(20)] 
    DRIVETRAIN_TYPE_OPTIONS = ['FWD', 'RWD', 'AWD', 'EV', 'Other']

    # Convertible
    BACK_SEAT_COUNT_OPTIONS = [0, 2]
    ROOF_TYPE_OPTIONS = ["textile", "detachable hardtop", "retractable hardtop", "windblocker", "safety", "other"]

    # Car
    NUMBER_OF_DOORS_OPTIONS = [2, 4, 6]

    # Truck
    CARGO_COVER_TYPE_OPTIONS = ['roll-up', 'soft folding', 'hard folding', 'retractable', 
        'high impact plastic lid', 'painted fiberglass lid', 'other']
    NO_REAR_AXLES_OPTIONS = [2, 3, 4]

    # ==============================================
    # Other
    # ==============================================
    # The first car was made on 1886: https://www.daimler.com/company/tradition/company-history/1885-1886.html
    MIN_MODEL_YEAR = 1886

    # Federal limit gross vehicle weight
    # https://ops.fhwa.dot.gov/freight/policy/rpt_congress/truck_sw_laws/index.htm
    MAX_CARGO_CAPACITY = 80000