"""
Testing model and object processors.
"""
from __future__ import unicode_literals
import pytest  # noqa
import sys
from textx import metamodel_from_str

if sys.version < '3':
    text = unicode  # noqa
else:
    text = str

grammar = """
First:
    'first' seconds+=Second
    ('A' a+=INT)?
    ('B' b?=BOOL)?
    ('C' c=STRING)?
;

Second:
    sec = INT
;

"""

model_processor_called = False


def test_model_processor():
    """
    Test that model processors are called after model parsing.
    """
    global model_processor_called

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'

    metamodel = metamodel_from_str(grammar)
    metamodel.register_model_processor(model_processor)

    metamodel.model_from_str(model_str)

    assert model_processor_called


def model_processor(model, metamodel):
    """
    Model processor is called when the model is successfully parsed.
    """
    global model_processor_called
    model_processor_called = True

    assert model.__class__.__name__ == "First"
    assert model.seconds[0].sec == 34


def test_object_processors():
    """
    Test that object processors are called.
    They should be called after each model object construction.
    """

    call_order = []

    def first_obj_processor(first):
        first._first_called = True
        call_order.append(1)

    def second_obj_processor(second):
        second._second_called = True
        call_order.append(2)

        # test that parent is fully initialised.
        # b should be True
        assert second.parent.b

    obj_processors = {
        'First': first_obj_processor,
        'Second': second_obj_processor,
    }

    metamodel = metamodel_from_str(grammar)
    metamodel.register_obj_processors(obj_processors)

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'
    first = metamodel.model_from_str(model_str)

    assert hasattr(first, '_first_called')
    for s in first.seconds:
        assert hasattr(s, '_second_called')
    assert call_order == [2, 2, 2, 1]


def test_object_processors_user_classes():
    """
    Test that object processors are called.
    They should be called after each model object construction.
    """

    def first_obj_processor(first):
        first._first_called = True
        first._a_copy = first.a

    def second_obj_processor(second):
        second._second_called = True
        second._sec_copy = second.sec

        # test that parent is fully initialised.
        # b should be True
        assert second.parent.b is not None

    obj_processors = {
        'First': first_obj_processor,
        'Second': second_obj_processor,
    }

    class First(object):
        def __init__(self, seconds, a, b, c):
            self.seconds = seconds
            self.a = a
            self.b = b
            self.c = c

    class Second(object):
        def __init__(self, sec, parent):
            self.sec = sec
            self.parent = parent

    metamodel = metamodel_from_str(grammar, classes=[First, Second])
    metamodel.register_obj_processors(obj_processors)

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'
    first = metamodel.model_from_str(model_str)

    assert hasattr(first, '_first_called')
    assert first._a_copy == first.a
    for s in first.seconds:
        assert hasattr(s, '_second_called')
        assert s._sec_copy == s.sec


def test_object_processor_falsy():
    """
    Test that object processors are called for falsy objects.
    """

    def second_obj_processor(second):
        second._second_called = True

    obj_processors = {
        'Second': second_obj_processor,
    }

    class Second(object):
        def __init__(self, parent, sec):
            self.parent = parent
            self.sec = sec
            self._second_called = False

        def __len__(self):
            return 0

    metamodel = metamodel_from_str(grammar, classes=[Second])
    metamodel.register_obj_processors(obj_processors)

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'
    first = metamodel.model_from_str(model_str)

    for s in first.seconds:
        assert s._second_called is True


def test_object_processor_replace_object():
    """
    Test that what is returned from object processor is value used in the
    output model.
    """
    def second_obj_processor(second):
        return second.sec / 2

    def string_obj_processor(mystr):
        return "[{}]".format(mystr)

    obj_processors = {
        'Second': second_obj_processor,
        'STRING': string_obj_processor,
    }

    metamodel = metamodel_from_str(grammar)
    metamodel.register_obj_processors(obj_processors)

    model_str = 'first 34 45 7 A 45 65 B true C "dfdf"'
    first = metamodel.model_from_str(model_str)

    assert len(first.seconds) == 3
    assert first.seconds[0] == 17

    assert first.c == '["dfdf"]'


def test_obj_processor_simple_match_rule():
    grammar = r"""
    First:
        a=MyFloat 'end'
    ;
    MyFloat:
        /\d+\.(\d+)?/
    ;
    """
    model = '3. end'

    mm = metamodel_from_str(grammar)
    m = mm.model_from_str(model)
    assert type(m.a) is text

    processors = {
        'MyFloat': lambda x: float(x)
    }
    print('filters')
    mm = metamodel_from_str(grammar)
    mm.register_obj_processors(processors)
    m = mm.model_from_str(model)

    assert type(m.a) is float


def test_obj_processor_sequence_match_rule():

    grammar = """
    First:
        i=MyFixedInt 'end'
    ;
    MyFixedInt:
    '0' '0' '04'
    ;
    """

    model = '0004 end'

    mm = metamodel_from_str(grammar)
    m = mm.model_from_str(model)
    assert type(m.i) is text

    processors = {
        'MyFixedInt': lambda x: int(x)
    }
    mm = metamodel_from_str(grammar)
    mm.register_obj_processors(processors)
    m = mm.model_from_str(model)

    assert type(m.i) is int


def test_base_type_obj_processor_override():
    grammar = """
    First:
        'begin' i=INT 'end'
    ;
    """

    def to_float_with_str_check(x):
        assert type(x) is text
        return float(x)

    processors = {
        'INT': to_float_with_str_check
    }
    mm = metamodel_from_str(grammar)
    mm.register_obj_processors(processors)
    m = mm.model_from_str('begin 34 end')

    assert type(m.i) is float


def test_custom_base_type_with_builtin_alternatives():
    grammar = r"""
    Model: i*=MyNumber;
    MyNumber: MyFloat | INT;
    MyFloat:  /[+-]?(((\d+\.(\d*)?|\.\d+)([eE][+-]?\d+)?)|((\d+)([eE][+-]?\d+)))(?<=[\w\.])(?![\w\.])/;
    """  # noqa

    mm = metamodel_from_str(grammar)
    model = mm.model_from_str('3.4 6')
    assert type(model.i[0]) is text
    assert type(model.i[1]) is int

    mm.register_obj_processors({'MyFloat': lambda x: float(x)})
    model = mm.model_from_str('3.4 6')
    assert type(model.i[0]) is float
    assert type(model.i[1]) is int


def test_nested_match_rules():
    """
    Test calling processors for nested match rules.
    """
    grammar = r"""
    Model: objects*=MyObject;
    MyObject: HowMany | MyNumber;
    HowMany: '+'+;  // We will register processor that returns a count of '+'
    MyNumber: MyFloat | INT;
    MyFloat:  /[+-]?(((\d+\.(\d*)?|\.\d+)([eE][+-]?\d+)?)|((\d+)([eE][+-]?\d+)))(?<=[\w\.])(?![\w\.])/;
    """  # noqa

    def howmany_processor(x):
        return len(x)

    mm = metamodel_from_str(grammar)
    mm.register_obj_processors({'HowMany': howmany_processor,
                                'MyFloat': lambda x: float(x)})
    model = mm.model_from_str('3.4 ++ + ++ 6')
    assert model.objects[0] == 3.4
    assert model.objects[1] == 5
    assert model.objects[2] == 6
    assert type(model.objects[2]) is int

    # Now we will add another processor for `MyObject` to test if we can change
    # the result returned from match processors lower in hierarchy.
    def myobject_processor(x):
        assert type(x) in [int, float]
        return '#{}'.format(text(x))
    mm.register_obj_processors({'HowMany': howmany_processor,
                                'MyFloat': lambda x: float(x),
                                'MyObject': myobject_processor})
    model = mm.model_from_str('3.4 ++ + ++ 6')
    assert model.objects[0] == '#3.4'
    assert model.objects[1] == '#5'


def test_multipart_nested_match_rules():
    """
    Test calling processors for multipart nested match rules.
    """
    grammar = r"""
    Model: objects*=MyNumber;
    MyNumber: '#' MyFloat | '--' INT '--';
    MyFloat:  /[+-]?(((\d+\.(\d*)?|\.\d+)([eE][+-]?\d+)?)|((\d+)([eE][+-]?\d+)))(?<=[\w\.])(?![\w\.])/;
    """  # noqa

    called = [False]

    def myfloat_processor(x):
        called[0] = True
        return float(x)

    mm = metamodel_from_str(grammar)
    mm.register_obj_processors({'MyFloat': myfloat_processor})
    model = mm.model_from_str(' # 3.4 -- 6 -- ')
    assert called[0]
    assert model.objects[0] == '#3.4'
    assert model.objects[1] == '--6--'
