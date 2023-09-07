
from pl_helpers import name, points, not_repeated
from code_feedback import Feedback
from pl_unit_test import PLTestCaseWithPlot, PLTestCase
import json

class Test(PLTestCaseWithPlot):
    
    def verify(self, function_name, expected, params_json):
        params = json.loads(params_json)
        observed = Feedback.call_user(self.st[function_name], *params)
        if (expected == observed):
            Feedback.set_score(1)
        else:
            Feedback.set_score(0)
