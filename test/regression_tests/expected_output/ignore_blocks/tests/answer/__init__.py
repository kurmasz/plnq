from .answer import Answer
from .float_answer import FloatAnswer
from .inline_answer import InlineAnswer
from .re_answer import ReAnswer

answer_types = {
    'FloatAnswer': FloatAnswer,
    'inline_answer': InlineAnswer,
    're_answer': ReAnswer,
}