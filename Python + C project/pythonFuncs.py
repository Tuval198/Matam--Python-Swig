#constants :
NUM_OF_SCORES = 5

ID_LOCATION = 0
EATING_HABITS_LOCATION = 1
AGE_LOCATION = 2
GENDER_LOCATION = 3
FIRST_SCORE_LOCATION = 4

ID_LEN = 8
MAX_AGE = 100
MIN_AGE = 10
MIN_VOTE = 1
MAX_VOTE = 10

VEGAN_VALUE = 0
VEGETARIAN_VALUE = 1
OMNIVORE_VALUE = 2

HISTOGRAM_SIZE = 10

MAN = False
WOMAN = True
#end of constants

def LegalVote(line):
    #gets one vote from votes file and returns true if it is legal
    words_list = line.split()
    if len(words_list[ID_LOCATION]) != ID_LEN: #ilegal id
        return False
    if int(words_list[AGE_LOCATION])<MIN_AGE or \
            int(words_list[AGE_LOCATION])>MAX_AGE: #ilegal age
        return False
    for i in range(FIRST_SCORE_LOCATION, FIRST_SCORE_LOCATION + 5):
        if int(words_list[i]) < MIN_VOTE or int(words_list[i]) > MAX_VOTE:
            #ilegal votes
            return False
    return True #everything is ok

def InsertVote(fixed_list, new_vote):
    #this function gets sorted votes list and a new legal vote
    #and inserts the vote in the correct place in the sorted list
    #if the person already voted we just change his vote
    for i, vote in enumerate(fixed_list):
        id_vote = vote.split()[ID_LOCATION]
        id_new_vote = new_vote.split()[ID_LOCATION]
        if id_vote == id_new_vote:     #if person already voted
            fixed_list[i] = new_vote
            return #vote inserted we are done
        if id_vote > id_new_vote:
            fixed_list.insert(i, new_vote)
            return #done
    #if we are here list is empty or we got to the last vote
    fixed_list.append(new_vote)

#Filters a survey and prints to screen the corrected answers:
#old_survey_path: The path to the unfiltered survey
def correct_myfile(old_survey_path):
    votes = open(old_survey_path, 'r')
    fixed_list = []
    for line in votes:
        if LegalVote(line):
            InsertVote(fixed_list, line)

    for vote in fixed_list:
        print(vote, end = "")
    votes.close()

import Survey #using it from here

def CastEatingHabit(habit):
    if habit == 'Omnivore':
        return OMNIVORE_VALUE
    if habit == 'Vegetarian':
        return VEGETARIAN_VALUE
    if habit == 'Vegan':
        return VEGAN_VALUE
    #shouldnt get here :
    return

def CastGender(gender):
    if gender == 'Man':
        return MAN
    if gender == 'Woman':
        return WOMAN
    #shouldnt get here :
    return

def CreateScoresArray(details):
    #this function gets detail list and return array with grades
    scores = Survey.SurveyCreateIntAr(NUM_OF_SCORES)
    for i in range(5):
        Survey.SurveySetIntArIdxVal(scores, i,
                                    int(details[FIRST_SCORE_LOCATION + i]))
    return scores

#Returns a new Survey item with the data of a new survey file:
#survey_path: The path to the survey
def scan_survey(survey_path):
    new_survey = Survey.SurveyCreateSurvey()
    votes = open(survey_path, 'r')
    for line in votes:
        details = line.split()
        scores_array = CreateScoresArray(details)
        Survey.SurveyAddPerson(new_survey, int(details[ID_LOCATION]),
                               int(details[AGE_LOCATION]),
                               CastGender(details[GENDER_LOCATION]),
                               CastEatingHabit(details[EATING_HABITS_LOCATION]),
                               scores_array)
        Survey.SurveyDestoryIntAr(scores_array)
    votes.close()
    return new_survey

#Prints a python list containing the number of votes for each rating of a group according to the arguments
#s: the data of the Survey object
#choc_type: the number of the chocolate (between 0 and 4)
#gender: the gender of the group (string of "Man" or "Woman"
#min_age: the minimum age of the group (a number)
#max_age: the maximum age of the group (a number)
#eating_habits: the eating habits of the group (string of "Omnivore", "Vegan" or "Vegetarian")

def print_info(s, choc_type, gender, min_age, max_age, eating_habits):
    histogram_array = Survey.SurveyQuerySurvey(s, choc_type,
                                               CastGender(gender),
                                               min_age, max_age,
                                               CastEatingHabit(eating_habits))
    histogram_list = []
    for i in range(HISTOGRAM_SIZE):
        histogram_list.append(Survey.SurveyGetIntArIdxVal(histogram_array, i))

    print(histogram_list)
    Survey.SurveyQueryDestroy(histogram_array)

#Clears a Survey object data
#s: the data of the Survey object
def clear_survey(s):
    Survey.SurveyDestroySurvey(s)
    return
