import sys, re


class UserNumberError(TypeError):
    pass


class UserNameError(TypeError):
    pass


# основна функція, яка працює з користувачем, приймає та виводить інформацію
def main():
    entered_str = None

    while True:
        entered_str = input("Hello!\n>>>") if entered_str is None else input(">>>")
        key = None

        for i in dict_of_keys.keys():
            if re.match(i, entered_str.lower()):
                key = i
                entered_str = entered_str.lower().removeprefix(key).removeprefix(" ").capitalize()
                break

        print(handler(key, entered_str))


# функція-дукоратор, яка перевіряє строку, введену користувачем, на винятки
def input_error(func):
    def wrappers(key, entered_str):
        try:
            return func(key, entered_str)

        except KeyError:
            return "I don't understand what you want from me!\n" \
                   "(An invalid command was entered. To see existing commands, type <help> or <info>)"

        except UserNameError:
            return "You entered the invalid name!\n" \
                   "(The name must contain only Latin letters and be separated from the command by one space)"

        except UserNumberError:
            return "You entered the invalid number!\n" \
                   "(The phone number should look like this: 380888888888 And be separated from the name by one space)"
    return wrappers


# функція, яка працює з введеною користувачем строкою
@input_error
def handler(key, entered_str):
    if key == "add" or key == "change":
        if re.match(r"[a-zA-Z]+ ?", entered_str) is None:
            raise UserNameError()
        if re.match(r"\w+ \+?\d{12} ?", entered_str) is None:
            raise UserNumberError()
        name_and_phone = re.split(" ", entered_str)
        names = name_and_phone[0]
        phones = name_and_phone[1]
        return dict_of_keys[key](names, phones)
    elif key == "phone":
        if re.match(r"[a-zA-Z]+ ?", entered_str) is None:
            raise UserNameError()
        name_and_phone = re.split(" ", entered_str)
        names = name_and_phone[0]
        return dict_of_keys[key](names)
    return dict_of_keys[key]()


# бот виводить у консоль привітання
def hello(*args, **kwargs):
    return "How can I help you?"


# бот зберігає в пам'яті новий контакт або змінює існуючий
def change(names, phones):
    is_new_contact = 'changed' if names in dict_of_contacts.keys() else 'added'
    dict_of_contacts[names] = phones
    return f"Contact with the name: '{names}', and phone number: '{phones}'"\
           f" - has been successfully {is_new_contact}!"


# бот виводить у консоль номер телефону для зазначеного контакту
def phone(names):
    names = re.match(r"\w+$", names).group()
    return f"{names} -> {dict_of_contacts.get(names)}" if names in dict_of_contacts.keys() else \
        "No contact found with this name!"


# бот виводить у консоль список всіх контактів
def show_all(*args, **kwargs):
    longest_names = 0
    for i in dict_of_contacts.keys():
        if len(i) > longest_names:
            longest_names = len(i)
    return "\n".join([f"{names:<{longest_names}} -> " + phones for names, phones in dict_of_contacts.items()])


# бот виводить у консоль список всіх команд
def info(*args, **kwargs):
    longest_keys = 0
    for i in dict_of_description.keys():
        if len(i) > longest_keys:
            longest_keys = len(i)
    return "All existing keys:\n\n" \
           "!!! WARNING: THERE SHOULD BE ONLY ONE SPACE BETWEEN ALL WORDS " \
           "AND THE NAME MUST CONTAIN ONLY LATIN LETTERS !!!\n\n" + \
           "\n".join([f"{f'<{key}>':<{longest_keys + 2}} -> " + desc for key, desc in dict_of_description.items()])


# бот віходить із програми
def close(*args, **kwargs):
    sys.exit("Good bye!")


# словник з усіма командами
dict_of_keys = {
    "hello": hello,
    "hi": hello,
    "add": change,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "info": info,
    "help": info,
    "good bye": close,
    "close": close,
    "exit": close,
    "no": close
}

# словник з усіма контактами
dict_of_contacts = {
    "Andrey": "380888888888",
    "Mary": "380777777777",
    "Sasha": "380666666666",
    "Maksim": "380555555555",
}

# словник з описом усіх команд
dict_of_description = {
    "hello": "Greetings command",
    "hi": "Greetings command",
    "add": "The command to add a new contact. After the command, write the name of the new contact, "
           "and then the phone number of the form 380888888888. There should be only one space between all words",
    "change": "The command to change the number of an existing contact. After the command, write the name "
              "of the existing contact, and then the phone number in the form 380888888888",
    "phone": "After the command, enter the name of the existing contact whose phone number you want to know",
    "show all": "Command to display all contacts",
    "info": "Help command. Shows all possible commands and their description",
    "help": "Help command. Shows all possible commands and their description",
    "good bye": "Program exit command",
    "close": "Program exit command",
    "exit": "Program exit command",
    "no": "Program exit command"
}


# запуск програми
if __name__ == "__main__":
    main()
