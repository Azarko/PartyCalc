"""Tests for calculator.py."""

__author__ = 'Boris Polyanskiy'

import unittest

from PartyCalc.calculator import Person, PartyCalculator


class TestPerson(unittest.TestCase):
    def test_init(self) -> None:
        person = Person('mr.White')
        self.assertEqual(person.name, 'mr.White')
        self.assertEqual(person.balance, 0.0)
        person = Person('mr.Green', 20.0)
        self.assertEqual(person.name, 'mr.Green')
        self.assertEqual(person.balance, 20.0)

    def test_calculate_payment(self) -> None:
        person = Person('mr.White', 50.0)
        self.assertEqual(person.calculate_payment(50.0), 0.0)
        self.assertEqual(person.calculate_payment(50), 0.0)
        self.assertEqual(person.calculate_payment(100.0), 50.0)
        self.assertEqual(person.calculate_payment(10.0), -40.0)
        person.balance = 50
        self.assertEqual(person.calculate_payment(50), 0.0)
        self.assertIsInstance(person.calculate_payment(50), float)


class TestPaymentCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = PartyCalculator()

    def test_init(self) -> None:
        self.assertEqual(len(self.calc.persons), 0)
        self.assertEqual(self.calc.each_pay, 0.0)

    def test_select_name(self) -> None:
        self.calc.add_person()
        self.calc.add_person()
        self.assertEqual(['person_01', 'person_02'], self.calc.get_names())
        self.calc.add_person('person_03')
        self.calc.add_person()
        self.assertIn('person_04', self.calc.get_names())
        self.calc.delete_person('person_02')
        self.assertNotIn('person_02', self.calc.get_names())
        self.calc.add_person()
        self.assertIn('person_02', self.calc.get_names())
        self.calc.change_person_name('person_02', 'person_2')
        self.calc.add_person()
        self.assertIn('person_02', self.calc.get_names())
        self.assertIn('person_2', self.calc.get_names())

    def test_add_person(self) -> None:
        self.calc.add_person('test1')
        self.calc.add_person('test2', 15.0)
        self.assertEqual(self.calc.persons[0].name, 'test1')
        self.assertEqual(self.calc.persons[0].balance, 0.0)
        self.assertEqual(self.calc.persons[1].name, 'test2')
        self.assertEqual(self.calc.persons[1].balance, 15.0)
        self.assertRaises(ValueError, self.calc.add_person, 'test1')
        self.assertRaises(ValueError, self.calc.add_person, 'test3', 'lalala')
        self.assertEqual(self.calc.persons[-1].name, 'test2')
        self.calc.add_person('test4', 50)
        self.assertIsInstance(self.calc.persons[-1].balance, float)
        self.assertEqual(len(self.calc.get_names()), 3)
        self.calc.add_person()
        self.calc.add_person()
        self.assertIn('person_01', self.calc.get_names())
        self.assertIn('person_02', self.calc.get_names())

    def test_delete_person(self) -> None:
        self.calc.add_person('test1')
        self.calc.add_person('test2')
        self.calc.add_person('test3', 10.0)
        self.assertRaises(ValueError, self.calc.delete_person, 'test4')
        self.calc.delete_person('test2')
        self.assertEqual([person.name for person in self.calc.persons], ['test1', 'test3'])

    def test_get_names(self) -> None:
        self.assertEqual(self.calc.get_names(), [])
        names = ['test1', 'test3', 'test2']
        for name in names:
            self.calc.add_person(name)
        self.assertEqual(self.calc.get_names(), names)

    def test_reset(self) -> None:
        self.calc.add_person('test1', 10)
        self.assertEqual(len(self.calc.persons), 1)
        self.calc.reset()
        self.assertEqual(len(self.calc.persons), 0)

    def test_get_person_by_name(self) -> None:
        params = (('test1', 0.0), ('test2', 10.0), ('test3', 50.0))
        for param in params:
            self.calc.add_person(*param)
        self.assertRaises(ValueError, self.calc._get_person_by_name, 'test4')
        for name, balance in params:
            person = self.calc._get_person_by_name(name)
            self.assertEqual(person.name, name)
            self.assertEqual(person.balance, balance)

    def test_set_person_balance(self) -> None:
        self.calc.add_person('test1')
        self.calc.add_person('test2', 10.0)
        self.assertRaises(ValueError, self.calc.set_person_balance, 'test3', 10)
        self.assertEqual(self.calc.persons[0].balance, 0.0)
        self.calc.set_person_balance('test1', 5.0)
        self.assertEqual(self.calc.persons[0].balance, 5.0)
        self.assertEqual(self.calc.persons[1].balance, 10.0)
        self.calc.set_person_balance('test2', 7.0)
        self.assertEqual(self.calc.persons[1].balance, 7.0)

    def test_change_person_name(self) -> None:
        self.calc.add_person('test1')
        self.calc.add_person('test2')
        self.assertEqual(self.calc.get_names(), ['test1', 'test2'])
        self.assertRaises(ValueError, self.calc.change_person_name, 'test3', 'test4')
        self.assertIsNone(self.calc.change_person_name('test2', 'test2'))
        self.calc.change_person_name('test2', 'test3')
        self.assertEqual(self.calc.get_names(), ['test1', 'test3'])
        self.assertRaises(ValueError, self.calc.change_person_name, 'test1', 'test3')

    def test_get_payments_sum(self) -> None:
        self.assertEqual(self.calc.get_payments_sum(), 0.0)
        self.calc.add_person('test1', 10.0)
        self.calc.add_person('test2', 20.0)
        self.calc.add_person('test3', 5.0)
        self.assertEqual(self.calc.get_payments_sum(), 35.0)

    def test_calculate_payments(self) -> None:
        self.calc.add_person('test1', 30.0)
        self.calc.add_person('test2', 5.0)
        self.calc.add_person('test3', 25.0)
        for person in self.calc.persons:
            self.assertEqual(person.need_to_pay, 0.0)
        self.calc.calculate_payments()
        self.assertEqual(self.calc.each_pay, 20.0)
        self.assertEqual(self.calc.persons[0].need_to_pay, -10.0)
        self.assertEqual(self.calc.persons[1].need_to_pay, 15.0)
        self.assertEqual(self.calc.persons[2].need_to_pay, -5.0)


if __name__ == "__main__":
    unittest.main()
