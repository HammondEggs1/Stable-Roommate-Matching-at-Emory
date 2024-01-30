class Student:

    def __init__(self, oxStudent, campusPref, schedule, gender, genderPref, extracurriculars, major, importanceWeights, name):
        # an int from -1 to 1, -1 for Oxford, 0 for alum, 1 for Atlanta non-alum
        self.oxStudent = oxStudent
        # a default dictionary of times that has 1s for available times and defaults to 0
        self.schedule = schedule
        # an int from 0 to 3, 0: female, 1: male, 2: non-binary, 3: other
        self.gender = gender
        # an int from 0 to 3 identical to gender but stating their preference
        self.genderPref = genderPref
        # a default dictionary of possible extracurriculars
        self.extracurriculars = extracurriculars
        # a major integer with the first two digits representing academic department,
        # the following two representing category, final two representing specific majors
        self.major = major
        # an array of numbers from 0 to 3 that criteria will be multiplied by when considering overall compatibilty
        # index 0: schedule 1: gender 2: Extracurriculars 3: major
        self.importanceWeights = importanceWeights
        # Field identical to OxStudent but used to indicate what campus the student wants their match to be from
        self.campusPref = campusPref
        # The student's name in String form
        self.name = name

    # Calls every other compare method to calculate an overall compatibility score between students
    # and multiplies them by the level of importance the students placed on them
    def compareStudents(self, student2):
        weightTotal = 2;
        for i, weight in enumerate(self.importanceWeights):
            weightTotal = weightTotal + weight
        total = (self.compareSchedule(student2.schedule) * self.importanceWeights[0])
        total = total + (self.compareGender(student2.gender) * self.importanceWeights[1])
        total = total + (self.compareExtracurriculars(student2.extracurriculars) * self.importanceWeights[2])
        total = total + (self.compareMajor(student2.major) * self.importanceWeights[3])
        total = total + self.compareCampus(student2.oxStudent) * 2
        return total/weightTotal

    # Uses the default dictionary schedules to check if the times this student is available
    # are also available for the other student. 
    def compareSchedule(self, schedule2):
        matches = 0
        for i, time in enumerate(self.schedule):
            if(schedule2[time]==1):
                matches = matches+1;
        return matches/pow(len(self.schedule), 0.75)

    # Checks if the other student's gender matches their preference. Reaching "No preference"
    # is considered equal to finding a match in this context
    def compareGender(self, gender2):
        for i in range(len(self.genderPref)-1):
            if(self.genderPref[i] == 3 or self.genderPref[i] == gender2):
                return (4-i)/4;
        return 0

    # Compares extracurriculars using a default dictionary in a manner
    # similar to compareSchedule
    def compareExtracurriculars(self, extracurriculars2):
        if(len(self.extracurriculars) == 0 or len(extracurriculars2) == 0):
            return 0
        matches = 0
        for i, extracurricular in enumerate(self.extracurriculars):
            if(extracurriculars2[extracurricular]==1):
                matches = matches+1;
        return matches/pow(len(self.extracurriculars), 0.75)

    # Compares majors based on their classification system, checking each
    # potential major represented by the String. It first checks the first
    # two numbers, the exact major, then the next two, department, then
    # the final two, academic area.
    def compareMajor(self, major2):
        majors = len(self.major) // 6
        total = 0
        for i in range(majors):  
            for j in range(len(major2) // 6):
                if(self.major[(i+4):(i+6)] == major2[(j+4):(j+6)]):
                    total = total + 1
                elif(self.major[(i+2):(i+4)] == major2[(j+2):(j+4)]):
                    total = total + 0.67
                elif(self.major[i:(i+2)] == major2[j:(j+2)]):
                    total = total + 0.33

        return (total)/pow(((majors+ (len(major2) // 6)) / 2), 0.75)

    # Checks if the other student is an alumni or non-alumni as preferred
    # THIS METHOD SHOULD BE ALTERED IN THE FUTURE TO REFLECT HAVING BOTH
    # ATLANTA AND OXFORD STUDENTS
    def compareCampus(self, campus2):
        if(self.campusPref == campus2):
            return 1
        return 0