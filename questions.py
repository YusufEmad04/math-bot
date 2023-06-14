import re

questions = {}
marking_scheme = {}

def steps_extractor(answer):
    lines = [line.strip() for line in answer.split("\n") if re.search(".+[).]", line.strip())]
    numerical = True if lines[0].startswith("1") else False

    return numerical, lines

def check_starting_type(text):
    letter_only = "l"
    letter_and_i = "li"

    letter_only_check = re.search("^\([^i]\)", text)
    letter_and_i_check = re.search("^\([^i]\)\(i+\)", text)

    if letter_only_check and not letter_and_i_check:
        return text[letter_only_check.span()[0] + 1: letter_only_check.span()[1] - 1], letter_only
    elif letter_and_i_check:
        letter_span = re.search("^\([^i]\)", text).span()
        i_span = re.search("\(i+\)", text).span()

        return (
            text[letter_span[0] + 1: letter_span[1] - 1],
            text[i_span[0] + 1: i_span[1] - 1]
        ), letter_and_i


def check_if_i(text):
    l = "l"
    i = "i"
    letter_check = re.search("^\([^i]\)", text)
    i_check = re.search("^\(i+\)", text)

    if letter_check:
        return text[letter_check.span()[0] + 1: letter_check.span()[1] - 1], l
    elif i_check:
        return text[i_check.span()[0] + 1: i_check.span()[1] - 1], i


def get_questions_from_lines(lines):
    current_letter = ""
    current_i_letter = ""
    current_state = "l"

    for i in lines:
        if i:
            if check_if_i(i):
                letter, letter_type = check_if_i(i)

                if letter_type == "l":
                    current_letter = letter
                    current_state = "l"
                    questions[letter] = [i]
                elif letter_type == "i":
                    current_state = "i"
                    current_i_letter = letter
                    if len(questions[current_letter]) == 1:
                        questions[current_letter].append({letter: i})
                    else:
                        questions[current_letter][1][letter] = i
            else:
                if current_state == "l":
                    questions[current_letter][0] += "\n" + i
                elif current_state == "i":
                    questions[current_letter][1][current_i_letter] += "\n" + i


def get_marking_scheme_from_lines(lines):
    current_letter = ""
    current_i_letter = ""
    current_state = "l"

    for i in lines:
        if i:
            if check_starting_type(i):
                letters, letter_type = check_starting_type(i)
                if letter_type == "l":
                    current_letter = letters
                    current_i_letter = ""
                    current_state = letter_type
                else:
                    current_letter = letters[0]
                    current_i_letter = letters[1]
                    current_state = letter_type
            else:
                if current_state == "l":
                    if current_letter not in marking_scheme:
                        marking_scheme[current_letter] = i
                    else:
                        marking_scheme[current_letter] += "\n" + i
                elif current_state == "li":
                    if current_letter not in marking_scheme:
                        marking_scheme[current_letter] = {current_i_letter: i}
                    else:
                        if current_i_letter not in marking_scheme[current_letter]:
                            # print(i)
                            marking_scheme[current_letter][current_i_letter] = i
                        else:
                            marking_scheme[current_letter][current_i_letter] += "\n" + i


with open("./questions/1.txt", "r", encoding='utf-8') as f:
    # read line by line
    lines = f.readlines()
    # remove \n
    lines = [line.strip() for line in lines]
    questions_lines = lines[:lines.index("Marking Scheme:")]
    marking_scheme_lines = lines[lines.index("Marking Scheme:") + 1:]
    get_questions_from_lines(questions_lines)
    get_marking_scheme_from_lines(marking_scheme_lines)


def get_question_text(question_letter, question_i_letter):
    if len(questions[question_letter]) == 1 or not question_i_letter:

        question = questions[question_letter][0]
        question = "\n".join(list(map(lambda x: "\t" + x, question.split("\n"))))

        return question
    else:

        question = questions[question_letter][0]
        question = "\n".join(list(map(lambda x: "\t" + x, question.split("\n"))))

        question_i = questions[question_letter][1][question_i_letter]
        question_i = "\n".join(list(map(lambda x: "\t" + x, question_i.split("\n"))))

        return question + "\n" + question_i


def get_marking_scheme_text(question_letter, question_i_letter):

    if question_letter in marking_scheme:
        print("yes")
    else:
        print("no")

    if type(marking_scheme[question_letter]) == str or not question_i_letter:
        answer = marking_scheme[question_letter]
        answer = "\n".join(list(map(lambda x: "\t" + x, answer.split("\n"))))
        return answer
    else:
        answer = marking_scheme[question_letter][question_i_letter]
        answer = "\n".join(list(map(lambda x: "\t" + x, answer.split("\n"))))

        return answer

# print(str(questions))
