#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def get_poezd(poezd, name, no, time):
    """
    Добавить данные о работнике.
    """
    poezd.append({"name": name, "no": no, "time": time})
    return poezd


def list(poezd):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if poezd:
         # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+".format(
            "-" * 10,
            "-" * 20,
            "-" * 8,
        )
        print(line)
        print("| {:^10} | {:^20} | {:^8} |".format(" No ", "Название", "Время"))
        print(line)

        for idx, po in enumerate(poezd, 1):
            print(
                "| {:>10} | {:<20} | {"
                "} |".format(po.get("no", ""), po.get("name", ""), po.get("time", ""))
            )
        print(line)

    else:
        print("Список поездов пуст.")


def select_poezd(poezd, nom):
     """
    Выбрать поезда с заданным номером.
    """
    rezult = []
    for idx, po in enumerate(poezd, 1):
        if po["no"] == str(nom):
            rezult.append(po)

    return rezult


def save_poezd(file_name, poezd):
    """
    Сохранить все поезда в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(poezd, fout, ensure_ascii=False, indent=4)


def load_poezd(file_name):
    """
    Считать все поезда из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def help():
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("display - вывести список поездов;")
    print("select - запросить поезд по номеру")
    print("save - сохранить список поездов;")
    print("load - загрузить список поездов;")
    print("exit - завершить работу с программой.")


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d", "--data", action="store", required=False, help="Имя файла данных"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("poezd")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser("add", parents=[file_parser], help="Добавить поезд")
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="Название пункта назначения?",
    )
    add.add_argument("--no", action="store", type=int, help="Номер поезда?")
    add.add_argument(
        "-t", "--time", action="store", required=True, help="Время отправления?"
    )

    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Панель отображения поездов"
    )

    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select", parents=[file_parser], help="Выбор поезда по номеру"
    )
    select.add_argument(
        "-o",
        "--nom",
        action="store",
        type=int,
        required=True,
        help="Введите номер поезда",
    )
    Help = subparsers.add_parser(
        "Help", parents=[file_parser], help="Вывод списка команд"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить имя файла.
    data_file = args.data
    if not data_file:
        data_file = os.environ.get("POEZD_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        poezd = load_poezd(data_file)
    else:
        poezd = []

    if args.command == "add":
        poezd = get_poezd(poezd, args.name, args.no, args.time)
        is_dirty = True

    # Отобразить всех работников.
    elif args.command == "display":
        list(poezd)

    elif args.command == "select":
        selected = select_poezd(poezd, args.nom)
        list(selected)
    elif args.command == "Help":
        help()

    if is_dirty:
        save_poezd(data_file, poezd)


if __name__ == "__main__":
    main()
