class Feedback:

    @staticmethod
    def call_user(func, *args):
        """Call the user function with the provided arguments."""
        return func(*args)
    
    @staticmethod
    def set_score(score):
        """Set the score for the feedback."""
        Feedback.score = score
    
    @staticmethod
    def add_feedback(str):
        Feedback.message = str