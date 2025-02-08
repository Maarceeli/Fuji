from sdk.src.interfaces.prometheus.context import (
    PrometheusAuthContext,
    PrometheusWebCredentials,
)
from sdk.src.interfaces.prometheus.interface import PrometheusInterface
import os
import pickle

# NOT SAFE, DO NOT USE IN PRODUCTION
if os.path.exists('data.temp'):
    with open('data.temp', 'rb') as file:
        auth_context = pickle.load(file)
        interface = PrometheusInterface(
            auth_context=auth_context,
            student_context=None,
        )
        
        interface.login()
else:
    interface = PrometheusInterface(
        auth_context=PrometheusAuthContext(
            prometheus_web_credentials=PrometheusWebCredentials(
                username=input("Login: "), password=input("Hasło: ")
            )
        ),
        student_context=None,
    )
    
    interface.login()
    auth_context = interface.get_auth_context()
    
    with open('data.temp', 'wb') as file:
        pickle.dump(auth_context, file)

students = interface.get_students()

# Select the first student and fetch grades
if students:
    interface.select_student(students[0].context)
    grades = interface.get_grades(2)
    print(grades)
else:
    print("No students found.")