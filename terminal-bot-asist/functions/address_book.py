import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.value.capitalize()

class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)

        match value:
            case _ if re.match(r'^\+380\d{9}', value): 
                self.value = value

            case _ if re.match(r'^380\d{9}', value): 
                self.value = f'+{value}'

            case _ if re.match(r'^80\d{9}', value): 
                self.value = f'+3{value}'

            case _ if re.match(r'^0\d{9}', value): 
                self.value = f'+38{value}'

            case _ if re.match(r'^\d{9}', value): 
                self.value = f'+380{value}'

            case _:
                self.value = 'Invalid input'
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str) -> None:
        obj_phone = Phone(phone)
        self.phones.append(obj_phone)
    
    def remove_phone(self, phone: str) -> None:
        removed_phone = self.find_phone(phone)
        if removed_phone:
            self.phones.remove(removed_phone)

    def find_phone(self, phone: str) -> Phone:
        try:
            searched_phone = Phone(phone)
            finded_phone = [p_obj for p_obj in self.phones if p_obj.value == searched_phone.value]
            return finded_phone[0]
        except ValueError:
            return None
        except IndexError:
            return None
        
    def edit_phone(self, old_phone, new_phone) -> None:
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        if key not in self.data:
            self.data[key] = record
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
           
    def find(self, name: str):
        return self.data[name] if name in self.data else None
    
    def __str__(self):
        result = 'Your AddressBook:'
        for _, record in self.data.items():
            result += f'\nContact name: {record.name.value}, phones: {'; '.join(p.value for p in record.phones)}\n{'-'*40}'
        return result








if __name__ == "__main__":# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
     
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
