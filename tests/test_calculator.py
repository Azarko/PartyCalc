import pytest


PERSON_NAME_1 = 'test1'
PERSON_NAME_2 = 'test2'
PERSON_NAME_3 = 'test3'
PERSON_NAME_4 = 'test4'


def test_init(calc):
    assert len(calc.persons) == 0
    assert calc.each_pay == 0
    assert 'with 0 persons' in repr(calc)


def test_select_name(calc):
    calc.add_person()
    calc.add_person()
    assert calc.get_names() == ['person_01', 'person_02']
    calc.add_person('person_03')
    calc.add_person()
    assert 'person_04' in calc.get_names()
    calc.delete_person('person_02')
    assert 'person_02' not in calc.get_names()
    calc.add_person()
    assert 'person_02' in calc.get_names()
    calc.change_person_name('person_02', 'person_2')
    calc.add_person()
    assert 'person_02' in calc.get_names()
    assert 'person_2' in calc.get_names()


def test_is_person_exists(calc):
    assert not calc.is_person_exists(PERSON_NAME_2)
    calc.add_person(PERSON_NAME_1)
    assert calc.is_person_exists(PERSON_NAME_1)
    assert not calc.is_person_exists(PERSON_NAME_2)


def test_add_person(calc):
    calc.add_person(PERSON_NAME_1)
    calc.add_person(PERSON_NAME_2, 15.0)
    assert calc.persons[0].name == PERSON_NAME_1
    assert calc.persons[0].balance == 0.0
    assert calc.persons[1].name == PERSON_NAME_2
    assert calc.persons[1].balance == 15.0
    with pytest.raises(ValueError):
        calc.add_person(PERSON_NAME_1)
    assert calc.persons[-1].name == PERSON_NAME_2
    calc.add_person(PERSON_NAME_4, 50)
    assert isinstance(calc.persons[-1].balance, float)
    assert len(calc.get_names()) == 3
    calc.add_person()
    calc.add_person()
    names = set(calc.get_names())
    assert 'person_01' in names
    assert 'person_02' in names
    with pytest.raises(ValueError):
        calc.add_person(balance='str')
    with pytest.raises(ValueError):
        calc.add_person(name='')


def test_delete_person(calc):
    calc.add_person(PERSON_NAME_1)
    calc.add_person(PERSON_NAME_2)
    calc.add_person(PERSON_NAME_3, 10.0)
    with pytest.raises(ValueError):
        calc.delete_person(PERSON_NAME_4)
    calc.delete_person(PERSON_NAME_2)
    assert PERSON_NAME_2 not in calc.get_names()


def test_get_names(calc):
    assert not calc.get_names()
    names = [PERSON_NAME_1, PERSON_NAME_3, PERSON_NAME_2]
    for name in names:
        calc.add_person(name)
    assert calc.get_names() == names


def test_reset(calc):
    calc.add_person(PERSON_NAME_1, 10)
    assert len(calc.persons) == 1
    calc.reset()
    assert len(calc.persons) == 0


def test_get_person_by_name(calc):
    params = (
        (PERSON_NAME_1, 0.0),
        (PERSON_NAME_2, 10.0),
        (PERSON_NAME_3, 50.0),
    )
    for param in params:
        calc.add_person(*param)
    with pytest.raises(ValueError):
        calc.get_person_by_name(PERSON_NAME_4)
    for name, balance in params:
        person = calc.get_person_by_name(name)
        assert person.name == name
        assert person.balance == balance


def test_set_person_balance(calc):
    calc.add_person(PERSON_NAME_1)
    calc.add_person(PERSON_NAME_2, 10.0)
    with pytest.raises(ValueError):
        calc.set_person_balance(PERSON_NAME_3, 10)
    assert calc.persons[0].balance == 0.0
    calc.set_person_balance(PERSON_NAME_1, 5.0)
    assert calc.persons[0].balance == 5.0
    assert calc.persons[1].balance == 10.0
    calc.set_person_balance(PERSON_NAME_2, 7.0)
    assert calc.persons[1].balance == 7.0


def test_change_person_name(calc):
    calc.add_person(PERSON_NAME_1)
    calc.add_person(PERSON_NAME_2)
    assert calc.get_names() == [PERSON_NAME_1, PERSON_NAME_2]
    with pytest.raises(ValueError):
        calc.change_person_name(PERSON_NAME_3, PERSON_NAME_4)
    assert calc.change_person_name(PERSON_NAME_2, PERSON_NAME_2) is None
    calc.change_person_name(PERSON_NAME_2, PERSON_NAME_3)
    assert calc.get_names() == [PERSON_NAME_1, PERSON_NAME_3]
    with pytest.raises(ValueError):
        calc.change_person_name(PERSON_NAME_1, PERSON_NAME_3)
    with pytest.raises(ValueError):
        calc.change_person_name(PERSON_NAME_1, '')


def test_get_payments_sum(calc):
    assert calc.get_payments_sum() == 0.0
    calc.add_person(PERSON_NAME_1, 10.0)
    calc.add_person(PERSON_NAME_2, 20.0)
    calc.add_person(PERSON_NAME_3, 5.0)
    assert calc.get_payments_sum() == 35.0


def test_calculate_payments(calc):
    calc.add_person(PERSON_NAME_1, 30.0)
    calc.add_person(PERSON_NAME_2, 5.0)
    calc.add_person(PERSON_NAME_3, 25.0)
    for person in calc.persons:
        assert person.need_to_pay == 0.0
    calc.calculate_payments()
    assert calc.each_pay == 20.0
    assert calc.persons[0].need_to_pay == -10.0
    assert calc.persons[1].need_to_pay == 15.0
    assert calc.persons[2].need_to_pay == -5.0


def test_to_list(calc):
    assert not calc.to_list()
    reference = [('test_2', 15.0), ('test_1', 10.0), ('test_3', 12.0)]
    for data in reference:
        calc.add_person(*data)
    assert reference == calc.to_list()
