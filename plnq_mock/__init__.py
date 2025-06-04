###############################################################################
#
# plnq_mock --- Mock the PLNQData object so that config files can be 
# executed in a Jupyter environment.
#
# The plnq script injects an object named plnq into the code blocks when it 
# executes them. That object does not exist in the Jupyter environment that 
# instructors use when editing exercise config files. This code creates that
# plnq object if necessary so that the code blocks don't crash when executed
# outside of the plnq script.
#
# (c) 2025  Zachary Kurmas
#
###############################################################################
from plnq.plnq import PLNQData


def setup():
    # Actually, at the moment there is no reason to mock anything. We just need 
    # to return a PLNQData object without putting the name 'plnq' into the 
    # notebook's namespace
    return PLNQData()