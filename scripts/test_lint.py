"""Тесты линтера: python3 -m unittest scripts/test_lint.py (из корня навыка)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint  # noqa: E402


def rules(text, prefix):
    return [f for f in lint.lint(text) if f[2].startswith(prefix)]


class SelfTest(unittest.TestCase):
    def test_builtin_self_test(self):
        lint.self_test()


class PossessiveEcho(unittest.TestCase):
    def test_list_of_vash(self):
        self.assertTrue(rules("Он знает вашу методологию, ваш стиль и ваши правила.", "С1"))

    def test_svoy_twice(self):
        self.assertTrue(rules("Соберите свои посты и список своих правок.", "С1"))

    def test_mixed_pronouns_ok(self):
        # «свои тексты» и «ваши» - разные местоимения, это не эхо
        self.assertFalse(rules("Вы отдаёте свои тексты, а ваши правки становятся правилами.", "С1"))

    def test_word_inside_other_word_ok(self):
        self.assertFalse(rules("Свойство своевременно проверено.", "С1"))


class NotInFrame(unittest.TestCase):
    def test_series(self):
        t = "Причина не в вас. Корень не в том, что сервис слабый. Нужна система."
        self.assertTrue(rules(t, "С6"))

    def test_single_ok(self):
        self.assertFalse(rules("Ваша карта тут ни при чём. Дело не в банке, а в стране выпуска.", "С6"))

    def test_plain_negation_ok(self):
        self.assertFalse(rules("Он не в офисе. Я не в курсе, что там.", "С6"))


class Particles(unittest.TestCase):
    def test_threshold_counts_only_long_texts(self):
        short = " ".join(["Помощник пишет черновик по правилам автора."] * 20)  # ~120 слов
        self.assertFalse(rules(short, "С7"))

    def test_hyphen_to(self):
        t = " ".join(["Писать-то вы умеете, только начинаете с нуля каждый раз."] * 40)
        self.assertFalse(rules(t, "С7"))


if __name__ == "__main__":
    unittest.main()
