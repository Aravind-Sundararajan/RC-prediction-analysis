from itertools import cycle

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
    
    def __repr__(self):
        return "instance of Feedback"

    """circular indexing, get a new positive message"""
    def get_positive_message(self):
        self.positive_message = next(self.positive_messages_cycle)
        return self.positive_message
    
    """ function that processes the input list. this is wrapped by get_feedback(). This should be implemented."""
    def _process(self,input):
        return self.feedback_messages[0]
    
    """ returns a feedback message based on the input list of prediction classifications from the RC NN"""
    def get_feedback(self, input):
        output = self.get_positive_message() + self._process(input)
        output.replace("IMPAIRED", self.impaired)
        output.replace("NORMAL", self.normal)
        return output