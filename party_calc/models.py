import dataclasses


@dataclasses.dataclass
class Person:
    """Dataclass which describes each person's parameters"""

    name: str
    balance: float = 0.0
    need_to_pay = 0.0

    def __repr__(self) -> str:
        return f'Person "{self.name}" with balance {self.balance}.'

    def calculate_payment(self, payment: float) -> float:
        """Calculate how much this person must to pay.

        :param payment: how much EACH person must to pay
        :return: how much THIS person must to pay
        """
        self.need_to_pay = float(payment - self.balance)
        return self.need_to_pay
