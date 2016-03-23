from FreakCore import core


if __name__ == "__main__":
    calculator = core.FreakCore()
    calculator.add_freak("Mr.White", 10)

    calc = core.FreakCore()
    print calc.get_freak_names()
