"""
Api for working with freak calculator.
"""

__author__ = 'Boris Polyanskiy'

from copy import copy
from dataclasses import dataclass
from typing import List


@dataclass
class Person:
    name: str
    balance: float = 0.0
    need_to_pay = 0.0

    def __repr__(self) -> str:
        return f'Person "{self.name}" with balance {self.balance}.'

    def calculate_payment(self, payment: float) -> float:
        """Calculate how much this person must to pay.

        :param payment: how much each person must to pay
        :return: how much this person must to pay
        """
        self.need_to_pay = float(payment - self.balance)
        return self.need_to_pay


class PartyCalculator:
    def __init__(self) -> None:
        self._persons = []      # type: List[Person]
        self.each_pay = 0.0

    def __repr__(self) -> str:
        return f'Payment calculator with {len(self._persons)} persons and total payments {self.get_payments_sum()}'

    def __getitem__(self, item):
        return copy(self._persons[item])

    @property
    def persons(self) -> List[Person]:
        return [person for person in self]

    def add_person(self, name: str, balance: float = 0.0) -> None:
        """Create and add new person.

        :param name: name of new person
        :param balance: initial balance of person
        :return: None
        """
        if name in self.get_names():
            raise ValueError(f'Person with name "{name}" already exists!')
        self._persons.append(Person(name, float(balance)))

    def delete_person(self, name: str) -> None:
        """Delete person with name `name`.

        :param name: name of person
        :return: None
        """
        if name not in self.get_names():
            raise ValueError(f"Person with name '{name}' doesn't exist!")
        self._persons.remove(self._get_person_by_name(name))

    def get_names(self) -> List[str]:
        """Return list with persons names."""
        return [person.name for person in self._persons]

    def reset(self) -> None:
        """Reset all instance data"""
        self._persons = []
        self.each_pay = 0.0

    def _get_person_by_name(self, name: str) -> Person:
        """Return person object with selected name

        :param name: name of person
        :return: Person object
        """
        if name not in self.get_names():
            raise ValueError(f"Person with name '{name}' doesn't exist!")
        for person in self._persons:
            if person.name == name:
                return person

    def set_person_balance(self, name: str, balance: float) -> None:
        """Change balance of person with name `name` to `balance`

        :param name: name of existing person
        :param balance: new balance
        :return: None
        """
        person = self._get_person_by_name(name)
        person.balance = balance

    def change_person_name(self, name: str, new_name: str) -> None:
        """Change name of person with name `name` to `new_name`.

        :param name: name of existing person
        :param new_name: new name of person
        :return: None
        """
        person = self._get_person_by_name(name)
        if new_name == name:
            raise ValueError('Selected names are same!')
        if new_name in self.get_names():
            raise ValueError(f'New name already exists: {new_name}!')
        person.name = new_name

    def get_payments_sum(self) -> float:
        """Return total paid sum."""
        return sum(person.balance for person in self._persons) if len(self._persons) else 0

    def calculate_payments(self) -> None:
        """Calculate how much each person must pay (or must receive)."""
        total_paid = self.get_payments_sum()
        each_pay = total_paid / len(self._persons)
        for person in self._persons:
            person.calculate_payment(each_pay)
        self.each_pay = each_pay
