
from pl_helpers import name, points, not_repeated
from code_feedback import Feedback
from pl_unit_test import PLTestCaseWithPlot, PLTestCase

def check_string(name, expected, observed):
    if not isinstance(observed, str):
        err_str = f"'{name}' did not return a string (it returned a '{type(observed)}'.)"
        Feedback.finish(err_str)
    if (expected != observed):
        Feedback.add_feedback(f"'{name}' did not return the expected value.")
        return False
    else:
        return True


class Test(PLTestCaseWithPlot):

    student_code_file = 'zzCODE_FILEzz'

    def verify_count_evens(self, list, answer):
        observed = Feedback.call_user(self.st.count_evens, list)
        if Feedback.check_scalar(f'result of count_evens({list})', answer, observed,
                                 accuracy_critical=False, report_failure=True):
            Feedback.set_score(1)
        else:
            Feedback.set_score(0)

    @points(1)
    @name('test 1')
    def test_1(self):
        expected = 77332
        observed = Feedback.call_user(self.st.fn1, 1, 4)
        if Feedback.check_scalar('result of fn1(1, 4)', expected, observed,
                                     accuracy_critical=False,report_failure=True):
            Feedback.set_score(1)
        else:
            Feedback.set_score(0)


   