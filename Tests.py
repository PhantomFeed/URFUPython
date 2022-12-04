from unittest import TestCase
import report_out
import table_out


class PrepareTests_for_report_Out(TestCase):
    def test_Tags(self):
        self.assertEqual(report_out.Tools.prepare('<div>Файл</div>'), 'Файл')

    def test_Usual(self):
        self.assertEqual(report_out.Tools.prepare('qwerty'), 'qwerty')

    def test_Spaces(self):
        self.assertEqual(report_out.Tools.prepare('AA          AAA'), 'AA AAA')

    def test_StrWithN(self):
        self.assertEqual(report_out.Tools.prepare('you\\nme'), 'you; me')

    def test_Empty(self):
        self.assertEqual(report_out.Tools.prepare(''), '')


class SalaryTests_for_report_out(TestCase):
    def test_salary_from(self):
        self.assertEqual(type(report_out.Salary(10.0, 20.4, 'RUR')).__name__, 'Salary')

    def test_salary_to(self):
        self.assertEqual(report_out.Salary(10.0, 20.4, 'RUR').salary_from, 10)

    def test_salary_currency(self):
        self.assertEqual(report_out.Salary(10.0, 20.4, 'RUR').salary_to, 20)

    def test_salary_to_rub(self):
        self.assertEqual(report_out.Salary('10.0', 20.4, 'RUR').salary_currency, 'RUR')


class currencyTests_for_report_out(TestCase):
    def test_two_strings(self):
        self.assertEqual(report_out.Salary.currency_to_rub(10, 20, 'RUR'), 15.0)

    def test_string_and_float(self):
        self.assertEqual(report_out.Salary.currency_to_rub(10.0, 20, 'RUR'), 15.0)

    def test_equal_string_and_float(self):
        self.assertEqual(report_out.Salary.currency_to_rub(10, 30.0, 'RUR'), 20.0)

    def test_equal_string_and_float_RUR(self):
        self.assertEqual(report_out.Salary.currency_to_rub(10, 30.0, 'EUR'), 1198.0)


class as_textTests(TestCase):
    def test_None(self):
        self.assertEqual(report_out.Report.as_text(None), '')

    def test_Empty(self):
        self.assertEqual(report_out.Report.as_text(''), '')

    def test_ListToStr(self):
        self.assertEqual(type(report_out.Report.as_text(['Да', 'Нет'])).__name__, 'str')

    def test_DictToStr(self):
        self.assertEqual(type(report_out.Report.as_text({'Да', 'Нет'})).__name__, 'str')

    def test_TupleToStr(self):
        self.assertEqual(type(report_out.Report.as_text(('Да', ['Нет']))).__name__, 'str')

    def test_String(self):
        self.assertEqual(report_out.Report.as_text('string'), 'string')


class SalaryTests_for_table_out(TestCase):
    def test_salary_from(self):
        self.assertEqual(type(table_out.Salary(10.0, 20.4, 'Нет', 'RUR')).__name__, 'Salary')

    def test_salary_to(self):
        self.assertEqual(table_out.Salary(10.0, 20.4, 'Да', 'RUR').salary_from, 10)

    def test_salary_currency(self):
        self.assertEqual(table_out.Salary(10.0, 20.4, 'Нет', 'RUR').salary_to, 20)

    def test_salary_to_rub(self):
        self.assertEqual(table_out.Salary('10.0', 20.4, 'Нет', 'RUR').salary_currency, 'RUR')