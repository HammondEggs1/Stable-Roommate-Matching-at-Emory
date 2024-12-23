# Stable-Roommate-Matching-at-Emory
An undergraduate research project completed in spring semester of 2023. Some work original, see README

This project utilizes both original and libraries. All parts of the project relating to the integer programming optimal roommate matching algorithm are a library written as part of a seperate research project not by Zachary Hammond. Files "api_connector.py," "main.py," and "student.py" are all original work by Zachary Hammond. 

This project work by accessing responses to a google form that requests specific information from Emory students about their major, gender, extracurriculars, and campus of origin. The form can be viewed here: https://docs.google.com/document/d/192n7EkimniMxfUHOT6-IagOVeEAoS_S5t9lkKrwyWlQ/edit?usp=sharing

The file api_connector.py pulls the data from the google form using forms API. The data is then processed into a series of student objects, which contain methods to compare each aspect of a student to another and generate an overall compatibiltiy score for each pair of students. Then, all students are compared to all others using these methods, before having each score pairwise sorted to rank student choices. These rankings are then fed into the (unoriginal) integer programming optimization algorithm to produce optimal matches.
