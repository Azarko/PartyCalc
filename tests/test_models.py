from party_calc.models import Person


def test_init():
    name = 'mr.White'
    person = Person(name)
    assert person.name == name
    assert person.balance == 0.0
    name, balance = 'mr.Green', 20.0
    person = Person(name, balance)
    assert person.name == name
    assert person.balance == balance
    assert name in repr(person)


def test_calculate_payment():
    person = Person('mr.White', 50.0)
    assert person.calculate_payment(50.0) == 0.0
    assert person.calculate_payment(50) == 0.0
    assert person.calculate_payment(100.0) == 50.0
    assert person.calculate_payment(10.0) == -40.0
    person.balance = 50
    assert person.calculate_payment(50) == 0.0
    assert isinstance(person.calculate_payment(50), float)
