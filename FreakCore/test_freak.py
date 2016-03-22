from unittest import TestCase, main
from core import Freak, FreakCore


class TestFreak(TestCase):
    def test_freaks_creation(self):
        freak = Freak()
        self.assertEqual(freak.name, Freak.def_freak_name)
        self.assertEqual(freak.balance, 0.0)
        freak = Freak("Mr.White", 13)
        self.assertEqual(freak.name, "Mr.White")
        self.assertEqual(freak.balance, 13)
        self.assertEqual(type(freak.balance), type(13.0))

    def test_freaks_rename(self):
        freak = Freak("Mr.White", 13)
        freak.change_name("Mr.Yellow")
        self.assertEqual(freak.name, "Mr.Yellow")
        self.assertEqual(freak.balance, 13)

    def test_set_balance(self):
        freak = Freak("Mr.white", 13)
        freak.set_balance(50)
        self.assertEqual(freak.balance, 50)


class TestCore(TestCase):
    def test_init(self):
        calc1 = FreakCore()
        self.assertEqual([], calc1.get_freak_names())
        self.assertEqual(0, calc1._calculate_total_sum())

        calc2 = FreakCore()
        self.assertEqual([], calc2.get_freak_names())
        self.assertEqual(0, calc2._calculate_total_sum())

        self.assertNotEqual(calc1, calc2)

    def test_add_delete(self):
        calc = FreakCore()
        # self.assertTrue(calc.add_freak("Mr.White", 13))
        # del calc2
    #     calc.add_freak("Mr.Yellow", 15)
    #     calc.add_freak("Mr.Brown", 17)
    #     calc.add_freak("Mr.Pinky", 19)
    #     del calc


# if __name__ == "__main__":
#     main()
