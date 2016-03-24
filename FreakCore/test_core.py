import unittest
from core import Freak, FreakCore


class TestFreak(unittest.TestCase):
    def setUp(self):
        self.freak = Freak()

    def tearDown(self):
        del self.freak

    def test_init(self):
        self.assertEqual(self.freak.name, self.freak.def_freak_name)
        self.assertEqual(self.freak.balance, 0)

    def test_change(self):
        self.freak.change_name("Mr.White")
        self.freak.set_balance(213)
        self.assertEqual(self.freak.name, "Mr.White")
        self.assertEqual(self.freak.balance, 213)
        self.assertEqual(type(self.freak.balance), type(213.0))


class TestCore(unittest.TestCase):
    def test_init(self):
        calc = FreakCore(False)
        self.assertEqual(calc.get_freak_names(), [])
        self.assertEqual(calc._calculate_total_sum(), 0)
        self.assertFalse(calc.get_freak_by_name("Mr.White"))
        self.assertFalse(calc.get_freak_index("Mr.White"))
        self.assertFalse(calc.set_freak_balance("Mr.White", 13))
        self.assertFalse(calc.delete_freak("Mr.White"))

    def test_add_delete(self):
        calc = FreakCore(False)
        names = ["Mr.White", "Mr.Yellow", "Mr.Brown", "Mr.Red"]
        self.assertTrue(calc.add_freak())
        self.assertTrue(calc.add_freak("Mr.Black"))
        self.assertTrue(calc.add_freak(balance=5))
        self.assertEqual(calc.get_freak_names(), ["Mr.Black", "freak_1", "freak_2"])
        self.assertEqual(calc.get_freak_balance("Mr.Black"), 0)
        self.assertEqual(calc.get_freak_balance("freak_2"), 5)
        self.assertTrue(calc.delete_all_freaks())
        self.assertEqual(calc.get_freak_names(), [])
        b = 15
        for name in names:
            self.assertTrue(calc.add_freak(name, b))
            b += 2
        self.assertEqual(calc.get_freak_names(), sorted(names))
        self.assertTrue(calc.delete_freak(names.pop(1)))
        self.assertEqual(calc.get_freak_names(), sorted(names))
        self.assertFalse(calc.add_freak(names[0]))
        self.assertEqual(calc.get_freak_names(), sorted(names))
        self.assertTrue(calc.delete_freak_by_index(0))
        self.assertEqual(calc.get_freak_names(), sorted(names[1:]))

    def test_calculate_balance(self):
        calc = FreakCore(False)
        names = ["Mr.White", "Mr.Yellow", "Mr.Brown", "Mr.Red"]
        b = 15
        for name in names:
            self.assertTrue(calc.add_freak(name, b))
            b += 2
        self.assertEqual(calc._calculate_total_sum(), 72)
        calc.calculate_payments()
        self.assertEqual(calc.each_pay, 18)
        pay_sum = 0
        for freak in calc.freaks:
            pay_sum += freak.need_to_pay
        self.assertEqual(pay_sum, 0)
        calc.print_freaks()
        calc.print_freaks_payments()


if __name__ == "__main__":
    unittest.main()
