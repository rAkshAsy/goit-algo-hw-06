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
        self.value = self.value.casefold()

class Phone(Field):
    def __init__(self, value: str):
        if not (9 < len(value) < 12) or not value.isdigit():
            raise ValueError('Invalid phone number.')
        super().__init__(value)
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str) -> None:
        obj_phone = Phone(phone)
        if obj_phone:
            self.phones.append(obj_phone)
    
    def remove_phone(self, phone: str) -> None:
        removed_phone = self.find_phone(phone)
        if removed_phone:
            self.phones.remove(removed_phone)

    def find_phone(self, phone: str) -> Phone:
        try:
            finded_phone = [p_obj for p_obj in self.phones if p_obj.value == phone]
            return finded_phone[0]
        except ValueError:
            return None
        except IndexError:
            return None
        
    def edit_phone(self, old_phone, new_phone) -> None:
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError('Incorect arguments for self.edit_phone() method.')

    def __str__(self):
        name = self.name.value.capitalize()
        if self.phones:
            return f"Contact name: {name}, phones: {', '.join([p.value for p in self.phones])}"
        return f'Contact name: {self.name.value}, phones: There`s no phones'
        
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        if key not in self.data:
            self.data[key] = record
    
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
           
    def find(self, name: str):
        search_name = name.casefold()
        return self.data[search_name] if search_name in self.data else None
    
    def __str__(self):
        underline = f'\n{'-'*50}\n'
        result = 'Your AddressBook:' + underline
        if self.data:
            for _, record in self.data.items():
                if not record.phones:
                    result += f'Contact name: {record.name.value}, phones: There`s no phones' + underline
                else:
                    p_list = [p.value for p in record.phones]
                    result += f'Contact name: {record.name.value}, phones: {', '.join(p_list)}' + underline
        else:
            result += 'Your address book is empty!' + underline
        return result


if __name__ == "__main__":

    book = AddressBook()

# Create first Record object

    rob_rec = Record('roBert')
    # rob_rec.add_phone('955546000')
    rob_rec.add_phone('0955546000')

# Create second Record object

    name_rec = Record('NaMe 1')
    name_rec.add_phone('0887009090')
    name_rec.add_phone('+380939585547')
    name_rec.add_phone('80939585547')

    name_rec.edit_phone('80939585547', '0887003030')

    name_rec.remove_phone('0887003030') # Remove phone numder
    name_rec.remove_phone('0887003000') # Return None and do nothing

    print(rob_rec, name_rec, sep='\n') # Test method Record.__str__()
    print('###'*20)

# Addind Records to the UserDic

    book.add_record(rob_rec)
    book.add_record(name_rec)
    
    print(book)

# Change phone number

    rob_rec.edit_phone('1234567890000', '0951002030') # Corectly work
    print(rob_rec)

# Exception catching

    try:
        rob_rec.edit_phone('INCORRECT PHONE', '+380959585444')
    except ValueError as e:
        print(e)

    try:
        rob_rec.edit_phone('0951002030', '00')
    except ValueError as e:
        print(e)
