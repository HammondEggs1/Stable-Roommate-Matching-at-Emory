from __future__ import print_function
import os
import google.auth
import pickle

from apiclient import discovery
from httplib2 import Http
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from collections import defaultdict
import json
from student import Student

# Parses JSON data for the campus the student attends and processes it
# into the format used by the Student object
def getOxstudentStatus(result):
    status = result['0eea6a37']['textAnswers']['answers'][0]['value']
    if(status=='Oxford College current student'):
        return -1
    elif(status=='Oxford College alumni, current Atlanta student'):
        return 0
    else:
        return 1

# Parses schedule selections from JSON and transforms them into a 
# default dictionary defaulting to 0 with 1s at available times
def getSchedule(result):
    availibility = defaultdict(lambda: 0)
    times = result['43583fc7']['textAnswers']['answers']
    for i, time in enumerate(times):
        availibility[time['value']] = 1;
    return availibility

# Parses the student's gender and converts it to integer form
def getGender(result):
    # If the question is not answered it is read as "prefer not to say"
    if '4d1a52c9' not in result:
        return 3
    gender = result['4d1a52c9']['textAnswers']['answers'][0]['value']
    if(gender=="Female"):
        gender=0
    elif(gender == "Male"):
        gender = 1
    elif(gender == "Non-binary"):
        gender = 2
    elif(gender == "Prefer not to say"):
        gender = 3
    return gender

# parses gender preferences in order into an array where location [i]
# represents the student's i+1st choice for a gender match
def getGenderPref(result):
    genderPrefs = [0] * 4
    if '51ee5b31' in result:
        genderPrefs[0] = result['51ee5b31']['textAnswers']['answers'][0]['value']
    else:
        genderPrefs[0] =  "No preference"
    if '13612449' in result:
        genderPrefs[1] = result['13612449']['textAnswers']['answers'][0]['value']
    else:
        genderPrefs[1] =  "No preference"
    if '5bd0e939' in result:
        genderPrefs[2] = result['5bd0e939']['textAnswers']['answers'][0]['value']
    else:
        genderPrefs[2] =  "No preference"
    if '791fdc66' in result:
        genderPrefs[3] = result['791fdc66']['textAnswers']['answers'][0]['value']
    else:
        genderPrefs[3] =  "No preference"

    
    
    for i in range(4):
        if(genderPrefs[i]=="Female"):
            genderPrefs[i]=0
        elif(genderPrefs[i] == "Male"):
            genderPrefs[i] = 1
        elif(genderPrefs[i] == "Non-binary"):
            genderPrefs[i] = 2
        elif(genderPrefs[i] == "No preference"):
            genderPrefs[i] = 3
    return genderPrefs

# Parses extracurriculars into a default dictionary in the same manner
# as the schedule
def getExtracurriculars(result):
    # First multiple choice extracurriculars are read
    extracurriculars = defaultdict(lambda: 0)
    if '60a62c20' in result:
        standards = result['60a62c20']['textAnswers']['answers']
        for i, extra in enumerate(standards):
            extracurriculars[extra['value']] = 1
    # Next, write-in answers are parsed and put into lower case for
    # ease of comparison
    if '069c8d36' in result:
        additionals = result['069c8d36']['textAnswers']['answers']
        for i, extra in enumerate(additionals):
            extracurriculars[extra['value'].lower()] = 1
    return extracurriculars

# Parses the importance question into an array of numbers that comparison
# scores will be multiplied by based on how important the student thinks that
# factor is. 
def getImportanceWeights(result):
    importanceWeights = [0] * 4
    importanceWeights[0] = result['7a3eaf26']['textAnswers']['answers'][0]['value']
    importanceWeights[1] = result['41edd11c']['textAnswers']['answers'][0]['value']
    importanceWeights[2] = result['2ce5700e']['textAnswers']['answers'][0]['value']
    importanceWeights[3] = result['4f1806a4']['textAnswers']['answers'][0]['value']
    
    
    for i in range(4):
        if(importanceWeights[i]=="Very important"):
            importanceWeights[i] = 4
        elif(importanceWeights[i] == "Somewhat important"):
            importanceWeights[i] = 2
        elif(importanceWeights[i] == "Somewhat unimportant"):
            importanceWeights[i] = 1
        elif(importanceWeights[i] == "Completely unimportant"):
            importanceWeights[i] = 0
    return importanceWeights

# Parses majors as Strings than transforms them into integers for comparison
def getMajor(result):
    major = ''
    majorData = result['3c41bb3c']['textAnswers']['answers']
    for i, data in enumerate(majorData):
        major = major + majorToInt(data['value'])
    return major

# Integers have been assigned to every major, with the first 2 digits
# representing field (STEM, Business, Humanities), the following two
# representing department, and the final two representing specific majors.
# Joint majors are occasionally considered equivalent to a double major in
# the two joint topics, but are not in other cases. 
def majorToInt(major):
    if(major=="Undecided"):
        return "000000"
    elif(major=="Accounting"):
        return "042101"
    elif(major=="African American Studies"):
        return "030101"
    elif(major=="African Studies"):
        return "030102"
    elif(major=="American Studies"):
        return "030222"
    elif(major=="Analytic Consulting"):
        return "042102"
    elif(major=="Ancient Mediterranean Studies"):
        return '030201'
    elif(major=="Anthropology"):
        return '020303'
    elif(major=="Applied Mathematics and Statistics"):
        return '010706'
    elif(major=="Arabic"):
        return '032004'
    elif(major=="Architectural Studies"):
        return '060805'
    elif(major=="Art History"):
        return '030202'
    elif(major=="Arts Management"):
        return '042103'
    elif(major=="Biology"):
        return '010401'
    elif(major=="Biophysics"):
        return '010407'
    elif(major=="Business Administration"):
        return '042104'
    elif(major=="Business Administration and Quantitative Sciences"):
        return '042105'
    elif(major=="Chemistry"):
        return '010402'
    elif(major=="Chinese Studies"):
        return  '030225'
    elif(major=="Classical Civilization"):
        return '030210'
    elif(major=="Classics"):
        return '030203'
    elif(major=="Classics and English"):
        return '030203030304'
    elif(major=="Classics and Philosophy"):
        return '030203031202'
    elif(major=="Comparative Literature"):
        return "030301"
    elif(major=="Computer Science"):
        return "010701"
    elif(major=="Dance and Movement Studies"):
        return "060801"
    elif(major=="East Asian Studies"):
        return "030211"
    elif(major=="Economics"):
        return "020902"
    elif(major=="Economics and Mathematics"):
        return "020902010703"
    elif(major=="Economics and Human Health"):
        return "020902010404"
    elif(major=="Engineering"):
        return "010406"
    elif(major=="Engineering Sciences"):
        return "010406"
    elif(major=="English"):
        return "030304"
    elif(major=="English and Creative Writing"):
        return "030302"
    elif(major=="English and History"):
        return "030217030304"
    elif(major=="Environment and Sustainability Management"):
        return "042106"
    elif(major=="Environmental Sciences"):
        return "010403"
    elif(major=="Film and Media Management"):
        return "042107"
    elif(major=="Film and Media"):
        return "021001"
    elif(major=="Finance"):
        return "042108"
    elif(major=="French Studies"):
        return "030213"
    elif(major=="German Studies"):
        return "030214"
    elif(major=="Greek"):
        return "030204032001"
    elif(major=="Health Innovation"):
        return "042109"
    elif(major=="History"):
        return "030217"
    elif(major=="History and Art History"):
        return "030217"
    elif(major=="Human Health"):
        return "010404"
    elif(major=="Information and Systems of Operations Management"):
        return "042110"
    elif(major=="Interdisciplinary Studies in Society and Culture"):
        return "031701"
    elif(major=="International Studies"):
        return "021301"
    elif(major=="Italian Studies"):
        return "030212"
    elif(major=="Japanese"):
        return "032006"
    elif(major=="Jewish Studies"):
        return "030220"
    elif(major=="Latin"):
        return "030209032002"
    elif(major=="Latin American and Caribbean Studies"):
        return "030221"
    elif(major=="Linguistics"):
        return "021201"
    elif(major=="Marketing"):
        return "042111"
    elif(major=="Mathematics"):
        return "010703"
    elif(major=="Mathematics and Computer Science"):
        return "010701010703"
    elif(major=="Mathematics and Political Science"):
        return "010703021302"
    elif(major=="Middle Eastern and South Asian Studies"):
        return "030223"
    elif(major=="Music"):
        return "060802"
    elif(major=="Neuroscience and Behavioral Biology"):
        return "010404"
    elif(major=="Nursing"):
        return "052201"
    elif(major=="Philosophy"):
        return "031202"
    elif(major=="Philosophy and Religion"):
        return "031901031202"
    elif(major=="Philosophy, Politics, Law"):
        return "031201"
    elif(major=="Physics"):
        return "010405"
    elif(major=="Physics and Astronomy"):
        return "010405"
    elif(major=="Political Science"):
        return "021302"
    elif(major=="Pre-Law"):
        return "031203"
    elif(major=="Pre-Med"):
        return "010410"
    elif(major=="Psychology"):
        return "021401"
    elif(major=="Public Policy and Analysis"):
        return "021303"
    elif(major=="Quantitative Sciences"):
        return "021801"
    elif(major=="Religion"):
        return "031901"
    elif(major=="Religion and Anthropology"):
        return "020303031901"
    elif(major=="Religion and Sociology"):
        return "031901020304"
    elif(major=="Russian and East European Studies"):
        return "030227"
    elif(major=="Sociology"):
        return "020304"
    elif(major=="Spanish"):
        return "032003"
    elif(major=="Spanish and Linguistics"):
        return "021201032003"
    elif(major=="Spanish and Portuguese"):
        return "032007"
    elif(major=="Strategy and Management Consulting"):
        return "042112"
    elif(major=="Theater Studies"):
        return "060803"
    elif(major=="Integrated Visual Arts"):
        return "060201"
    elif(major=="Women's Gender and Sexuality Studies"):
        return "021501"
    return "ERROR"

# Parses JSON for the student's name
def getName(result):
    return result['5f141760']['textAnswers']['answers'][0]['value']

# Parses JSON for the student's preferred campus origin for their match
def getCampusPref(result):
    # If the question is unanswered, the student is from Atlanta and needs an Oxford match
    if '567a783c' not in result:
        return -1
    pref = result['567a783c']['textAnswers']['answers'][0]['value']
    if(pref == 'Non-alumni'):
        return 0
    else:
        return 1
    
# Contacts the google server and pulls form data as JSON, then calls other methods
# to format the data to make student objects, then produces an array of student objects
# from the data.
def getStudentData():
    SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # we check if the file to store the credentials exists
    if not os.path.exists('credentials.dat'):

        flow = InstalledAppFlow.from_client_secrets_file('Documents\\SRI_IP-main\\src\\credentials.json', SCOPES)
        credentials = flow.run_local_server()

        with open('credentials.dat', 'wb') as credentials_dat:
            pickle.dump(credentials, credentials_dat)
    else:
        with open('credentials.dat', 'rb') as credentials_dat:
            credentials = pickle.load(credentials_dat)

    if credentials.expired:
        credentials.refresh(Request())

    # Picks out our specific form and gets data
    service = build('forms', 'v1', credentials=credentials)
    form_id = '1fSNDsALFTor40VbJp134dZCLN03E59SwJ4Tqq1iwZRk'
    results = service.forms().responses().list(formId=form_id).execute()['responses']

    students = []

    for i in range(30):
        result = results[i]['answers']
        oxStudent = getOxstudentStatus(result)
        schedule = getSchedule(result)
        gender = getGender(result)
        genderPref = getGenderPref(result)
        extracurriculars = getExtracurriculars(result)
        major = getMajor(result)
        importanceWeights = getImportanceWeights(result)
        name = getName(result)
        campusPref = getCampusPref(result)
        students.append(Student(oxStudent, campusPref, schedule, gender, genderPref, extracurriculars, major, importanceWeights, name))

    return students
