from feedback import Feedback

class Analyzer:
    def __init__(self):
        self.f = Feedback()
        self.time_window = 2.0 #2 seconds

    def __repr__(self):
        return "instance of analyzer"

    """determines the current time string. there is probably a smarter way to do this."""
    def get_time_duration(self,input):
        l = len(input)
        seconds = self.time_window*l
        if (seconds < 60):
            return str(seconds) + " seconds"
        minutes = int(seconds/60)
        if (minutes < 60):
            return str(minutes) + " minutes"
        hours = int(minutes/60)
        if (hours <= 24):
            return str(hours) + " hours"
        days = int(hours/24)
        return str(days) + " days"
    

    """performs the analysis on the input list of prediction classes"""
    def run(self,input):
        l = len(input)
        possible_feedback_durations = [
            900,#15 minutes
            3600,#1 hour
            21600,#6 hours
            86400,#1 day
            518400,#6 days
        ]
        possible_feedback_durations = [elem for elem in possible_feedback_durations if elem < l]
        output = []
        for elem in possible_feedback_durations:
            this_input = input[0:int(elem/self.time_window)]
            duration_string = self.get_time_duration(this_input)
            feedback_string = self.f.get_feedback(this_input)
            feedback_string = feedback_string.replace('CURRENTTIME',duration_string)
            output.append(feedback_string)
        return output