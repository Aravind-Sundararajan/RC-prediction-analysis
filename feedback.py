from itertools import cycle

class Ratios:
    def __init__(self, input,dur):
        duration = dur
        ratios = [input.count(c)/duration for c in range(5)]

        self.unimanual = ratios[0] + ratios[1]
        self.unimanual_DNDR = ratios[0] / (ratios[1]  + 0.0001)

        self.biAsymmetric = ratios[2] + ratios[3]
        self.biAsymmetric_DNDR = ratios[2] / (ratios[3] + 0.0001)

        self.bisymmetric = ratios[4]

        self.bimanual = self.biAsymmetric + self.bisymmetric

        self.all_control = sum(ratios[0:4])   

class Feedback:
    """a class that holds and returns feedback"""
    def __init__(self):
        message_file = open("positive_messages.txt","r")
        positive_messages = message_file.readlines()
        self.positive_messages_cycle = cycle(positive_messages)
        self.positive_message = next(self.positive_messages_cycle )
        message_file.close()

        feedback_file = open("feedback.txt","r")
        self.feedback_messages = feedback_file.readlines()
        feedback_file.close()
        self.impaired = "left" #idk why this is like this but whatever
        self.normal = "right"
        self.time_window = 2.0 #2 seconds
    
    def __repr__(self):
        return "instance of Feedback"

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

    """circular indexing, get a new positive message"""
    def get_positive_message(self):
        self.positive_message = next(self.positive_messages_cycle)
        return self.positive_message
    
    """ function that processes the input list. this is wrapped by get_feedback(). This should be implemented."""
    def get_feedback_message(self,t1,t2):
        return self.feedback_messages[0]

    """ function that compares 2 input lists of RC data"""
    def _process(self,t1,t2):
        l = len(t1)
        t1_1 = [t for t in t1 if t < 5] #control
        t1_2 = [t for t in t1 if t > 5] #post-stroke
        t2_1 = [t for t in t2 if t < 5] #control
        t2_2 = [t for t in t2 if t > 5] #post-stroke
        rt1_1 = Ratios(t1_1,l)
        rt1_2 = Ratios(t1_2,l)
        rt2_1 = Ratios(t2_1,l)
        rt2_2 = Ratios(t2_2,l)

        if rt1_1.all_control > rt1_2.all_control:
            posrat = rt1_2.all_control/rt1_1.all_control
        else:
            posrat = rt1_1.all_control/rt1_2.all_control

        return self.feedback_messages[0]

    """ returns a feedback message based on the input list of prediction classifications from the RC NN"""
    def get_feedback(self, t1,t2):
        output = self.get_positive_message() + self._process(t1,t2)
        output = output.replace("IMPAIRED", self.impaired)
        output = output.replace("NORMAL", self.normal)
        return output

    """performs the analysis on the input list of prediction classes"""
    def run(self,input = None, path = None ):
        output = []

        if path is not None:
            with open(path) as f:
                rcdata = f.read().splitlines()
        elif input is not None:
            rcdata = input
        else:
            return output

        l = len(rcdata)

        possible_feedback_durations = [
            900,#15 minutes
            3600,#1 hour
            21600,#6 hours
            86400,#1 day
            518400,#6 days
        ]

        possible_feedback_durations = [elem for elem in possible_feedback_durations if 2*elem < l] # if we can fit 2 durations in the input file
        
        for elem in possible_feedback_durations:
            t1 = input[0:int(elem/self.time_window)]
            t2 = input[int(elem/self.time_window):2*int(elem/self.time_window)]
            duration_string = self.get_time_duration(t1)
            feedback_string = self.get_feedback(t1,t2)
            feedback_string = feedback_string.replace('CURRENTTIME',duration_string)
            output.append(feedback_string)
        return output