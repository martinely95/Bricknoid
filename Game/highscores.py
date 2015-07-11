from collections import OrderedDict


def return_highscores():
    scores = OrderedDict()
    with open('system/highscores.txt') as txt_file:
        for score in txt_file:
            line = score.split(" ", 1)
            line[1] = line[1][:-1]
            scores[line[0]] = line[1]
    return scores


def check_if_highscore(score):
    scores = return_highscores()
    for score2 in scores.keys():
        if int(score) > int(score2):
            return True
    if type(scores) is OrderedDict:
        return True
    return False


def insert_highscore(score, name):
    scores = return_highscores()
    scores[score] = name
    with open('system/highscores.txt', 'w') as txt_file:
        for key, value in scores.items():
            txt_file.writelines(key)
            txt_file.write(' ')
            txt_file.write(value)
            txt_file.write('\n')

