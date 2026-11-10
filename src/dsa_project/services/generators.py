#idk kung itututloy pa to



# import random
# import string
# import qrcode
# import os
# from datetime import date, timedelta

# def pass_gen(type, length):
#     password = ""
#     match(type):
#         case 'default':
#             for i in range(length):
#                 password += random.choice(string.ascii_letters + string.digits + string.punctuation)
#             return password
#         case 'pin':
#             for i in range(length):
#                 password += random.choice(string.digits)
#         #add more idk    

# def qr_gen(text):
#     qr = qrcode.QRCode(
#     version = 21,
#     error_correction = qrcode.constants.ERROR_CORRECT_M,
#     box_size = 5,
#     border = 5)
#     qr.add_data(text)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
#     os.makedirs("static/uploads/qrcodes_generated", exist_ok=True)
#     img.save("static/uploads/qrcodes_generated/qr_code.png")
#     return "uploads/qrcodes_generated/qr_code.png"



# first_names = []
# last_names = []
# nationalities = []
# def fake_info_gen():
#     first = random.choice(first_names)
#     middle = random.choice(last_names)
#     last = random.choice(last_names)
#     start = date(1980, 1, 1)
#     end = date(2007, 12, 31)
#     birthdate = start + timedelta(days=random.randint(0, (end - start).days))
    
#     return {
#         "name": {
#             "first": first,
#             "middle": middle,
#             "last": last,
#             "full": f"{first} {middle} {last}",
#         },
#         "personal": {
#             "age": random.randint(18, 60),
#             "birthdate": birthdate.strftime("%Y-%m-%d"),
#             "gender": random.choices(population=['Male', 'Female', 'Gay', 'Female Gay', 'Both', 'None'], weights=[0.45, 0.45, 0.04, 0.04, 0.01, 0.01],
#                                      k=1)[0],
#             "nationality": random.choice(nationalities)
#         },
#         "contact": {
#             "email": f"{first}{middle}{last}@fakemail.com",
#             "phone": ''.join(str(random.randint(0, 9)) for _ in range(8)),
#             "username": ""
#         },
#         "address": {
#             "street": "",
#             "city": "",
#             "region": "",
#             "country": "",
#             "postal_code": ""
#         },
#         "additional": {
#             "occupation": "",
#             "company": "",
#             "education": "",
#             "hobbies": []
#         }
#     }