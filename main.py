import table_out
import report_out

""""Предоставляет возможность выбора вывода табличных данных вакансий либо формирования
    графиков и отчетов в виде ввода команд: Вакансии или Статистика
"""

type_out = input("Введите вид формирования данных: ")
if type_out == 'Вакансии':
    table_out.InputParam()
elif type_out == 'Статистика':
    report_out.get_table()
else:
    print('Неверный ввод!')


#Main нужен для того, чтобы объединить работу двух файлов