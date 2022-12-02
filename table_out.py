import csv
import math
import re
import prettytable
from datetime import datetime
from prettytable import PrettyTable


class Tools:
    """Класс хранит в себе необходимые два словаря для перевода текста
    """
    rus_names = {'Название': 'name',
                 'Описание': 'description',
                 'Навыки': 'key_skills',
                 'Опыт работы': 'experience_id',
                 'Премиум-вакансия': 'premium',
                 'Компания': 'employer_name',
                 'Оклад': 'salary_from',
                 'Верхняя граница вилки оклада': 'salary_to',
                 'Оклад указан до вычета налогов': 'salary_gross',
                 'Идентификатор валюты оклада': 'salary_currency',
                 'Название региона': 'area_name',
                 'Дата публикации вакансии': 'published_at'}

    rus_true_false = {'True': 'Да', 'False': 'Нет'}

    @staticmethod
    def exit_with_print(line):
        print(line)
        exit()

    @staticmethod
    def prepare(line):
        """Очищает входную строку и возвращает очищенную для дальнейшего использования

            Args:
                line (str): Строка, которую нужно очистить

            Returns:
                str: Очищенная строка
        """
        string = re.sub(r"<[^>]+>", '', line)
        if '\n' not in string:
            string = ' '.join(string.split())
        if string == 'True' or string == 'False':
            string = Tools.rus_true_false[string]
        return string


class Vacancy:
    """Класс устанавливает все основные поля вакансии, а также хранит словарь dic_experience для перевода опыта работы
    """
    dic_experience = {"noExperience": "Нет опыта",
                      "between1And3": "От 1 года до 3 лет",
                      "between3And6": "От 3 до 6 лет",
                      "moreThan6": "Более 6 лет"}

    def __init__(self, dictionary):
        """Инициализирует объект Vacancy

            Args:
                name (str): Название вакансии
                description (str): Описание вакансии
                key_skills (list): Навыки
                experience_id (str): Опыт работы
                premium (str): Информация о том премиум вакансия или нет
                employer_name (str): Компания
                salary (Salary): Комбинированная информация о зарплате
                area_name (str): Название региона
                published_at (str): Дата публикации вакансии
        """
        self.name = dictionary['name']
        self.description = dictionary['description']
        self.key_skills = dictionary['key_skills']
        self.experience_id = Vacancy.dic_experience[dictionary['experience_id']]
        self.premium = dictionary['premium']
        self.employer_name = dictionary['employer_name']
        self.salary = Salary(dictionary['salary_from'], dictionary['salary_to'], dictionary['salary_gross'],
                             dictionary['salary_currency'])
        self.area_name = dictionary['area_name']
        self.published_at = dictionary['published_at']


class Salary:
    """Класс устанавливает все поля для представления зарплаты, хранит словарь для перевода курсов
    """
    currency_to_rub = {"AZN": 35.68,
                       "BYR": 23.91,
                       "EUR": 59.90,
                       "GEL": 21.74,
                       "KGS": 0.76,
                       "KZT": 0.13,
                       "RUR": 1,
                       "UAH": 1.64,
                       "USD": 60.66,
                       "UZS": 0.0055}

    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """Инициализирует объект Salary

            Args:
                salary_from (int): Нижняя граница вилки оклада
                salary_to (int): Верхняя граница вилки оклада
                salary_gross (str): Информация о том с вычитом ли налогов зп или нет
                salary_currency (str): Валюта оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    @staticmethod
    def get_salary_ru(salary_from, salary_to, salary_currency):
        """Используется для перевода нижней и верхней границы вилки оклада для дальнейшего получения средней зарплаты

            Args:
                salary_from (int): Нижняя граница вилки оклада
                salary_to (int): Верхняя граница вилки оклада
                salary_currency (str): Валюта оклада

            Returns:
                Tuple (int, int): Переведённые нижняя и верхяя граница вилки оклада
        """
        salary_from = int(float(salary_from)) * Salary.currency_to_rub[InputParam.curr_invert[salary_currency]]
        salary_to = int(float(salary_to)) * Salary.currency_to_rub[InputParam.curr_invert[salary_currency]]
        return salary_from, salary_to


class DataSet:
    """Класс отвечает за чтение и подготовку данных из CSV-файла

        Attributes:
            file_name (str): Название файла
            vacancies_objects (list): Список вакансий
    """

    def __init__(self, file_name):
        """Инициализирует объект DataSet.

            Args:
                file_name (str): Название файла
                vacancies_objects (list): Список вакансий
        """
        self.file_name = file_name
        data_tuple = DataSet.csv_reader(file_name)
        dic = DataSet.csv_filter(data_tuple[0], data_tuple[1])
        vacancies_objects = []
        for dictionary in dic:
            vacancies_objects.append(Vacancy(dictionary))
        self.vacancies_objects = vacancies_objects

    @staticmethod
    def csv_reader(file_name):
        """Считывает csv файл

            Args:
                file_name (str): Название файла

            Returns:
                tuple: Кортеж, состоящий из названий колонок и всех вакансий
        """
        csv_read = csv.reader(open(file_name, encoding="utf_8_sig"))
        list_data = [x for x in csv_read]
        if len(list_data) == 1:
            print("Нет данных")
            exit()
        if len(list_data) == 0:
            print("Пустой файл")
            exit()
        columns = list_data[0]
        vacancies = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
        return vacancies, columns

    @staticmethod
    def csv_filter(reader, list_naming):
        """Очищает и переводит входной файл

            Args:
                reader (list): csv файл
                list_naming (list): Словарь для перевода csv файла

            Returns:
                list: Очищенный лист
        """
        resumes = []
        sentences = {}
        for resume in reader:
            for i in range(len(resume)):
                resume[i] = Tools.prepare(resume[i])
                sentences[list_naming[i]] = resume[i]
            resumes.append(sentences.copy())
        return resumes


class InputParam:
    """Класс  отвечает за обработку параметров вводимых пользователем: фильтры, сортировка, диапазон вывода, требуемые столбцы, а также за печать таблицы на экран

        Attributes:
            file_name (str): Название файла
            filter_param (list): Параметр фильтрации(список из столбца и параметра фильрации)
            sort_param (str): Параметр сортировки
            invert_param (str): Обратный ли порядок сортировки
            range_param (list): Диапазон вывода(список из двух чисел)
            columns_param (str): Требуемые столбцы
    """

    def __init__(self):
        """Инициализирует объект InputConect, запускает проверку правильности введенных данных

            Args:
                data_set (list): Список словарей с вакансиями
                param (list): Список параметров
        """
        params = InputParam.get_params()
        data_set = DataSet(params[0])
        InputParam.print_vacancies(data_set, params[1], params[2], params[3], params[4], params[5])

    @staticmethod
    def get_params():
        """Запускает проверку правильности введенных параметров

            Returns:
                Tuple(str, str, str, str, list, list): Название файла, параметр фильтрации, параметр сортировки,
                    порядок сортировки, диапазон вывода, требуемые столбцы
        """
        file_name = input("Введите название файла: ")
        filter_param = input("Введите параметр фильтрации: ")
        sort_param = input("Введите параметр сортировки: ")
        invert_param = input("Обратный порядок сортировки (Да / Нет): ")
        range_param = input("Введите диапазон вывода: ").split()
        columns_param = input("Введите требуемые столбцы: ").split(', ')

        if filter_param != "" and ': ' not in filter_param:
            Tools.exit_with_print('Формат ввода некорректен')
        if filter_param != '' and filter_param.split(': ')[0] not in Tools.rus_names:
            Tools.exit_with_print('Параметр поиска некорректен')
        if sort_param != '' and sort_param not in Tools.rus_names:
            Tools.exit_with_print('Параметр сортировки некорректен')
        if invert_param != '' and invert_param not in Tools.rus_true_false.values():
            Tools.exit_with_print('Порядок сортировки задан некорректно')

        return file_name, filter_param, sort_param, invert_param, range_param, columns_param

    dic_currency = {"AZN": "Манаты",
                    "BYR": "Белорусские рубли",
                    "EUR": "Евро",
                    "GEL": "Грузинский лари",
                    "KGS": "Киргизский сом",
                    "KZT": "Тенге",
                    "RUR": "Рубли",
                    "UAH": "Гривны",
                    "USD": "Доллары",
                    "UZS": "Узбекский сум"}

    curr_invert = {value: key for key, value in dic_currency.items()}

    @staticmethod
    def curr_formatter(salary_from, salary_to, salary_gross, salary_currency):
        """Проверяет параметры и переводит данные

            Args:
                salary_from (int): Нижняя граница вилки оклада
                salary_to (int): Верхняя граница вилки оклада
                salary_gross (str): Информация о том с вычитом ли налогов зп или нет
                salary_currency (str): Валюта оклада

            Returns:
                str: Нижняя, верхняя граница вилки оклада, валюту и вычет налогов
        """
        currency = InputParam.dic_currency[salary_currency]
        if salary_gross == 'Нет':
            gross = 'С вычетом налогов'
        else:
            gross = 'Без вычета налогов'
        salary_from = math.trunc(float(salary_from))
        salary_to = math.trunc(float(salary_to))
        return f'{salary_from} - {salary_to} ({currency}) ({gross})'

    @staticmethod
    def formatter(row):
        """Фильтрует вакансию

            Args:
                row (dict): Словарь с одной вакансией

            Returns:
                dict: Возвращает вакансию, если она подходит под параметр фильтрации
        """
        dic = {}
        dic_names = list(Tools.rus_names.values())
        dic_names = dic_names[:7] + dic_names[10:]
        for key in dic_names:
            if key == 'salary_from':
                dic[key] = InputParam.curr_formatter(row.salary.salary_from, row.salary.salary_to,
                                                     row.salary.salary_gross, row.salary.salary_currency)
                continue
            else:
                dic[key] = getattr(row, key)
        return dic

    @staticmethod
    def do_filter(data, filter_list):
        """Фильтрует данные

            Args:
                data (list): Входные данные
                filter_list (str): Введенный параметр

            Returns:
                list: Отфильтрованные данные
        """

        def for_filter(row):
            """Фильтрует данные

                Args:
                    row (list): Входные данные

                Returns:
                    row (list): Отфильтрованные данные по парметрам
            """
            if filter_list == '':
                return True
            parameter = filter_list.split(': ')
            if parameter[0] == 'Оклад':
                salary = row['salary_from'].split()
                salary_from = salary[0]
                salary_to = salary[2]
                return int(salary_from) <= int(parameter[1]) <= int(salary_to)
            if parameter[0] == 'Идентификатор валюты оклада':
                return row['salary_from'].split()[3].replace('(', '').replace(')', '') == parameter[1]
            if parameter[0] == 'Навыки':
                parameters = parameter[1].split(', ')
                list_skill = row['key_skills'].split('\n')
                k = 0
                for x in parameters:
                    if x in list_skill:
                        k = k + 1
                return k == len(parameters)
            if parameter[0] == 'Дата публикации вакансии':
                return datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%f%z').strftime('%d.%m.%Y') == parameter[
                    1]
            return row[Tools.rus_names[parameter[0]]] == parameter[1]

        filtered_list = list(filter(for_filter, data))
        if not filtered_list:
            Tools.exit_with_print('Ничего не найдено')
        return filtered_list

    @staticmethod
    def do_sort(data, sort, reverse):
        """Сортирует данные по параметрам

            Args:
                data (list): Список словарей с вакансиями
                sort (list): Параметр фильтрации (список из столбца и параметра фильрации)
                reverse (str): Обратный ли порядок сортировки

            Returns:
                list: Отсортированный список словарей с вакансиями
        """

        is_reverse = False
        if reverse == 'Да':
            is_reverse = True

        exp_sort = {'Нет опыта': 0, 'От 1 года до 3 лет': 1, 'От 3 до 6 лет': 2, 'Более 6 лет': 3}

        def for_sort(row):
            if sort == 'Оклад':
                salary = row['salary_from'].split()
                currency = re.search(r'\((.*?)\)', row['salary_from']).group(1)
                salary_from, salary_to = Salary.get_salary_ru(salary[0], salary[2], currency)
                return (salary_from + salary_to) / 2
            if sort == 'Навыки':
                skills = row['key_skills'].split('\n')
                return len(skills)
            if sort == 'Дата публикации вакансии':
                return datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%f%z')
            if sort == 'Опыт работы':
                return exp_sort[row['experience_id']]
            return row[Tools.rus_names[sort]]

        if sort != '':
            return sorted(data, key=for_sort, reverse=is_reverse)
        else:
            return data

    @staticmethod
    def create_data(data, filter_list, sort, reverse):
        """Сортирует талицу

             Args:
                 data (list): Список словарей с вакансиями
                 sort (list): Параметр фильтрации (список из столбца и параметра фильрации)
                 reverse (str): Обратный ли порядок сортировки
                 filter_list (str): Параметры фильтрации

             Returns:
                 list: Отсортированный список словарей с вакансиями
        """
        result = []
        for i in range(len(data.vacancies_objects)):
            dic = InputParam.formatter(data.vacancies_objects[i])
            result.append(dic)

        filtered_list = InputParam.do_filter(result, filter_list)
        sorted_list = InputParam.do_sort(filtered_list, sort, reverse)

        for i in range(len(sorted_list)):
            salary = sorted_list[i]['salary_from'].split()
            salary_from = '{0:,}'.format(int(salary[0])).replace(',', ' ')
            salary_to = '{0:,}'.format(int(salary[2])).replace(',', ' ')
            salary[0] = str(salary_from)
            salary[2] = str(salary_to)
            sorted_list[i]['salary_from'] = ' '.join(salary)
            sorted_list[i]['published_at'] = datetime.strptime(sorted_list[i]['published_at'],
                                                               '%Y-%m-%dT%H:%M:%f%z').strftime('%d.%m.%Y')

            new_list = list(sorted_list[i].values())
            for j in range(len(new_list)):
                if len(new_list[j]) > 100:
                    new_list[j] = new_list[j][:100] + '...'
            sorted_list[i] = new_list
            sorted_list[i].insert(0, str(i + 1))
        return sorted_list

    @staticmethod
    def print_vacancies(data_set, filter_list, sort, reverse, indexes, fields_list):
        """Сортирует талицу

            Args:
                data_set (list): Список словарей с вакансиями
                filter_list (str): Параметры фильтрации
                sort (list): Параметр фильтрации(список из столбца и параметра фильрации)
                reverse (str): Обратный ли порядок сортировки
                indexes (Sized): Индекс столбца по которому происходит сортировка
                fields_list (list): Заполняющий лист
        """
        table = PrettyTable()
        rus_list = list(Tools.rus_names.keys())
        table.field_names = ['№'] + rus_list[:7] + rus_list[10:]
        table.align = 'l'
        table.hrules = prettytable.ALL
        table.max_width = 20

        data = InputParam.create_data(data_set, filter_list, sort, reverse)
        table.add_rows(data)

        try:
            indexes[0] = int(indexes[0]) - 1
            indexes[1] = int(indexes[1]) - 1
        except IndexError:
            if len(indexes) == 0:
                indexes.append(0)
                indexes.append(len(data_set.vacancies_objects))
            if len(indexes) == 1:
                indexes.append(len(data_set.vacancies_objects))

        if fields_list == ['']:
            print(table.get_string(start=indexes[0], end=indexes[1]))
        elif len(fields_list) == 1:
            fields_list.insert(0, '№')
            print(table.get_string(start=indexes[0], end=indexes[1], fields=fields_list))
        else:
            fields_list.insert(0, '№')
            print(table.get_string(start=indexes[0], end=indexes[1], fields=fields_list))
