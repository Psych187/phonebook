#Создать телефонный справочник с возможностью импорта и экспорта данных в формате .txt. Фамилия, имя, отчество,
# номер телефона - данные, которые должны находиться в файле.
#1. Программа должна выводить данные
#2. Программа должна сохранять данные в текстовом файле
#3. Пользователь может ввести одну из характеристик для поиска определенной записи(Например имя или фамилию
#человека)
#4. Использование функций. Ваша программа не должна быть линейной



def choose_action(phonebook):
    while True:
        print('Menue:')
        user_choice = input('1 - Open another book\n2 - View all contacts\n3 - Find contact\n4 - Add contact\n\
5 - Change contact\n6 - Remove contact\n7 - Export/import contacts\n0 - Exit\n')
        print()
        if user_choice == '1':
            file_to_add = input('Enter imported file name: ')
            import_data(file_to_add, phonebook)
        elif user_choice == '2':
            show_phonebook(phonebook)
        elif user_choice == '3':
            contact_list = read_file_to_dict(phonebook)
            find_number(contact_list)
        elif user_choice == '4':
            add_phone_number(phonebook)
        elif user_choice == '5':
            change_phone_number(phonebook)
        elif user_choice == '6':
            delete_contact(phonebook)
        elif user_choice == '7':
            source_file = input('Enter file name to export from: ')
            destination_file = input('Enter file name to export to: ')
            search_parameter = input('0 - Search by name\n1 - Search by surname\n2 - Search by number\n3 - Search by comment:\n')
            search_value = input('Enter value: ')
            export_contact(source_file, destination_file, search_parameter, search_value)
        elif user_choice == '0':
            print('See you!')
            break
        else:
            print('Wrong command!')
            print()
            continue


def import_data(file_to_add, phonebook):
    try:
        with open(file_to_add, 'r', encoding='utf-8') as new_contacts, open(phonebook, 'a', encoding='utf-8') as file:
            contacts_to_add = new_contacts.readlines()
            file.writelines(contacts_to_add)
    except FileNotFoundError:
        print(f'{file_to_add} not found')


def read_file_to_dict(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    headers = ['Name', 'Surname', 'Phone number', 'Comment']
    contact_list = []
    for line in lines:
        line = line.strip().split()
        contact_list.append(dict(zip(headers, line)))
    return contact_list


def read_file_to_list(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        contact_list = []
        for line in file.readlines():
            contact_list.append(line.split())
    return contact_list


def search_parameters():
    print('Which field to search?')
    search_field = input('1 - name\n2 - surname\n3 - phone number\n4 - comment\n')
    print()
    search_value = None
    if search_field == '1':
        search_value = input('Enter name to search: ')
        print()
    elif search_field == '2':
        search_value = input('Enter surname to search: ')
        print()
    elif search_field == '3':
        search_value = input('Enter phone num to search: ')
        print()
    if search_field == '4':
        search_value = input('Enter comment to search: ')
        print()
    return search_field, search_value


def find_number(contact_list):
    search_field, search_value = search_parameters()
    search_value_dict = {'1': 'Name', '2': 'Surname', '3': 'Phone number', '4': 'Comment' }
    found_contacts = []
    for contact in contact_list:
        if contact[search_value_dict[search_field]] == search_value:
            found_contacts.append(contact)
    if len(found_contacts) == 0:
        print('Not found')
    else:
        print_contacts(found_contacts)
    print()


def get_new_number():
    first_name = input('Enter name: ')
    last_name = input('Enter surname: ')
    phone_number = input('Enter phone number: ')
    comment = input('Enter comment: ')
    return first_name,last_name, phone_number, comment


def add_phone_number(file_name):
    info = ' '.join(get_new_number())
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f'{info}\n')


def show_phonebook(file_name):
    list_of_contacts = sorted(read_file_to_dict(file_name), key=lambda x: x['Name' ])
    print_contacts(list_of_contacts)
    print()
    return list_of_contacts


def search_to_modify(contact_list: list):
    search_field, search_value = search_parameters()
    search_result = []
    for contact in contact_list:
        if contact[int(search_field) - 1] == search_value:
            search_result.append(contact)
    if len(search_result) == 1:
        return search_result[0]
    elif len(search_result) > 1:
        print('Several matches found')
        for i in range(len(search_result)):
            print(f'{i + 1} - {search_result[i]}')
        num_count = int(input('Choose contact to change/remove: '))
        return search_result[num_count - 1]
    else:
        print('Not found')
    print()


def change_phone_number(file_name):
    contact_list = read_file_to_list(file_name)
    number_to_change = search_to_modify(contact_list)
    contact_list.remove(number_to_change)
    print('Enter field to change ')
    field = input('1 - Name\n2 - Surname\n3 - Phone number\n4 - Comment\n')
    if field == '1':
        number_to_change[0] = input('Enter name: ')
    elif field == '2':
        number_to_change[1] = input('Enter surname: ')
    elif field == '3':
        number_to_change[2] = input('Enter phone number: ')
    elif field == '4':
        number_to_change[3] = input('Enter comment: ')
    contact_list.append(number_to_change)
    with open(file_name, 'w', encoding='utf-8') as file:
        for contact in contact_list:
            line = ' '.join(contact) + '\n'
            file.write(line)


def delete_contact(file_name):
    contact_list = read_file_to_list(file_name)
    number_to_change = search_to_modify(contact_list)
    contact_list.remove(number_to_change)
    with open(file_name, 'w', encoding='utf-8') as file:
        for contact in contact_list:
            line = ' '.join(contact) + '\n'
            file.write(line)


def print_contacts(contact_list: list):
    for contact in contact_list:
        for key, value in contact.items():
            print(f'{key}: {value:12}', end='')
        print()


def export_contact(source_file, destination_file, search_parameter, search_value):
    contact_list = read_file_to_list(source_file)
    search_result = []
    for contact in contact_list:
        if contact[1] == search_value:  # Поиск по фамилии (если параметр - "фамилия")
            search_result.append(contact)
        elif contact[0] == search_value:  # Поиск по имени (если параметр - "имя")
            search_result.append(contact)
        elif contact[2] == search_value:  # Поиск по телефону (если параметр - "телефон")
            search_result.append(contact)
        elif contact[3] == search_value:  # Поиск по комментарию (если параметр - "комментарий")
            search_result.append(contact)

    if len(search_result) == 1:
        with open(destination_file, 'r', encoding='utf-8') as file:
            existing_contacts = file.readlines()
            existing_contacts = [contact.strip() for contact in existing_contacts]
            new_contact = ' '.join(search_result[0])
            if new_contact in existing_contacts:
                print("Contact already exists.")
            else:
                with open(destination_file, 'a', encoding='utf-8') as file:
                    line = new_contact + '\n'
                    file.write(line)
                print("Contact exported")
    elif len(search_result) > 1:
        print('Several matches found:')
        for i in range(len(search_result)):
            print(f'{i + 1} - {search_result[i]}')
        num_count = int(input('Choose contact to export: '))
        with open(destination_file, 'r', encoding='utf-8') as file:
            existing_contacts = file.readlines()
            existing_contacts = [contact.strip() for contact in existing_contacts]
            new_contact = ' '.join(search_result[num_count - 1])
            if new_contact in existing_contacts:
                print("Already exists")
            else:
                with open(destination_file, 'a', encoding='utf-8') as file:
                    line = new_contact + '\n'
                    file.write(line)
                print("Contact exported")
    else:
        print('Not found')



if __name__ == '__main__':
    file = input('Enter book to open in format name.txt: ')
    choose_action(file)