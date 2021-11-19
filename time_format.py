def time_format(seconds):
    if (seconds >= (4361170769 * pow(10, 8))):
        return "more than the universe is old"
    elif (seconds >= (1.42 * pow(10, 17)) and seconds < (4361170769 * pow(10, 8))):
        return "more than the Earth is old"
    elif (seconds >= 31556926 and seconds < (1.42 * pow(10, 17))):
        return str(round(seconds / 31556926, )) + " years " + str(round((seconds % 31556927) / 86400, )) + " days"
    elif (seconds >= 86400 and seconds < 31556926):
        return str(round((seconds / 86400) % 366, )) + " days " + str(round((seconds % 86400) / 3600, )) + " hours"
    elif (seconds > 3600 and seconds < 86400):
        return  str(round((seconds / 3600) % 25, )) + " hours " + str(round(seconds % 3600, )) + " seconds"
    else:
        return str(round(seconds, 2)) + " seconds"