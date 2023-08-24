from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
import re
import pickle

class Field:
    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __str__(self):
        return self.value

class Phone(Field):
    def __repr__(self):
        return self.value
    
    @Field.value.setter
    def value(self, new_value):
        # Перевірка на коректність номера телефону за допомогою регулярного виразу
        if not re.match(r'^\d{10}$', new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value

class Email(Field):
    def __repr__(self):
        return self.value

class Birthday(Field):

    @Field.value.setter
    def value(self, new_value):
        if new_value > datetime.now():
            raise ValueError("Invalid birthday: cannot be in the future")
        self._value = new_value

class Record:
    def __init__(self, name, phone: Phone=None, email: Email=None, birthday: Birthday=None):  
        self.name = name
        self.phones = [] 
        self.emails = []
        self.birthday = birthday 
        if phone:
            self.phones.append(phone)
        if email:
            self.emails.append(email)


    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def add_email(self, email):
        self.emails.append(email)

    def remove_email(self, email):
        self.emails.remove(email)

    def edit_email(self, old_email, new_email):
        if old_email in self.emails:
            index = self.emails.index(old_email)
            self.emails[index] = new_email

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()

            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()

            days_left = (next_birthday - today).days
            return days_left

class AddressBook(UserDict):

    def __init__(self, file_path):
        super().__init__()
        self.file_path = Path(file_path)
        self.load()

    def dump(self):
        with self.file_path.open('wb') as file:
            pickle.dump((self.data, self.last_record_id), file)

    def load(self):
        if self.file_path.exists():
            with self.file_path.open('rb') as file:
                self.data, self.last_record_id = pickle.load(file)
        else:
            self.data = {}
            self.last_record_id = 0

    def search(self, search_str):
        result = []
        search_str = search_str.lower()

        for record_id, record in self.data.items():
            if (
                search_str in record.name.value.lower() or
                any(search_str in phone.value for phone in record.phones) or
                any(search_str in email.value.lower() for email in record.emails)
            ):
                result.append(record_id)

        return result

    def __iter__(self, batch_size=1):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i + batch_size]

    def add_record(self, record):
        self.data[record.name.value] = record

if __name__ == "__main__":

# Створення декількох полів
    name1 = Name("John Doe")
    phone1 = Phone("0991234567")
    email1 = Email("john@gmail.com")
    birthday1 = Birthday(datetime(1990, 5, 15))

    name2 = Name("Jane Smith")
    phone2 = Phone("0501234567")
    email2 = Email("jane@gmail.com")
    birthday2 = Birthday(datetime(1985, 10, 20))

# Створення записів
    record1 = Record(name1, phone1, email1, birthday1)
    record2 = Record(name2, phone2, email2, birthday2)

# Додавання та редагування контактів
    record1.add_phone(Phone("0505555555"))
    record2.edit_email(Email("jane@gmail.com"), Email("updated@gmail.com"))

# Створення адресної книги та додавання записів
    address_book = AddressBook("address_book.pkl")
    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.dump()
    address_book.load()

    search_str = "0501234567"
    search_result = address_book.search(search_str)
    if search_result:
        print(f"Search results for '{search_str}':")
        for result in search_result:
            print(result)
    else:
        print(f"No results found for '{search_str}'")



    # batch_size = 2 
    # for batch in address_book:
    #     for record in batch:
    #         print("Name:", record.name)
    #         print("Phones:", record.phones)
    #         print("Emails:", record.emails)
        
    #         if record.birthday:
    #             days_left = record.days_to_birthday()
    #             print("Days to next birthday:", days_left)
        
    #         print("-" * 20)