
import re
def validate_signup_data(data):
    error = {}
    required_keys = {'first_name','email','phone_number','organization','last_name','password','is_waitlisted','is_premium'}
    keys_passed = set(data.keys())
    missing_keys = required_keys - keys_passed
    incorrect_keys = keys_passed - required_keys
    first_name = data.get('first_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    

    if missing_keys or incorrect_keys: #if either case existings then loop in
        return {'missing_keys': missing_keys, 'extra_keys': incorrect_keys}
    for key in required_keys: # for each value ie, first_name, phone_number, email etc in req keys, loop one by one. this confirms that all values are provided by the user
        if not str(data[key]): # str is to convert false in a string otherwise its not taken. if no value is passed, then return error
            error[key] = '{} is missing'.format(key)
    
    if first_name:
        regex = '/^[!@#$%^&*()_+\-=\[\]{;}:"\\|,.<>\/?]*$/'
        if len(first_name) < 3:
            error['first_name'] = 'First name should have atleast 3 characters'
        if not re.search(regex,first_name):
            error['first_name'] = 'First name cannot have special characters'

    if email:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex,email)):
            error['email'] = 'Email entered is invalid'

    if phone_number:
        if not len(phone_number) == 10:
            error['phone_number'] = 'The phone number must contain 10 digits'
        if not phone_number.isdigit():
            error['phone_number'] = 'Phone number contains only digits'

    if password:
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$"
        if not (re.search(regex,password)):
            error['password'] = 'Please enter a valid password. Password should be of atleast 8 characters. Password should have one uppercase,one number,one special character,one lowercase'

    return error


def validate_campaign(data):
    error = {}
    required_keys = {'title','description','start_date','end_date','end_message'}
    keys_passed = set(data.keys())
    missing_keys = required_keys - keys_passed
    extra_keys = keys_passed - required_keys

    if missing_keys or extra_keys:
        return {'missing_keys': missing_keys, 'extra_keys': extra_keys}
    for key in required_keys:
        if not str(data[key]):
            error[key] = '{} is missing'.format(key)
    return error


def validate_bots(data):
    error = {}
    required_keys = {'title','description','intro_text','help_text','end_message','questions','campaign_id_id'}
    keys_passed = set(data.keys())
    missing_keys = required_keys - keys_passed
    extra_keys = keys_passed - required_keys

    if missing_keys or extra_keys:
        return {'missing_keys': missing_keys, 'extra_keys': extra_keys}
    for key in required_keys:
        if not str(data[key]):
            error[key] = '{} is missing'.format(key)
    return error