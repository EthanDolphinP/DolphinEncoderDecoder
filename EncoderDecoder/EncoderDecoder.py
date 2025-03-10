import string
import random
import json
import os
import sys
import re  # Added for regex functionality
from fnmatch import fnmatch

class EncoderDecoder:
    def __init__(self, old_key, new_key):
        self.old_key = old_key
        self.new_key = new_key

    def Initial_CLI(self):
        print("-" * 16, "Encoder/Decoder", "-" * 16)
        print("Option One: Encode")
        print("Option Two: Decode")
        print("Option Three: Search for File")
        print("Option Zero: Close Program")
        while True:
            try:
                user_choice = int(input("Pick Your Choice: "))
                if user_choice in [1, 2, 3, 0]:
                    return user_choice
                else:
                    print("Please enter a valid number")
            except ValueError:
                print("Please enter a valid number")

    def Msg_Encode(self):
        print("-" * 16, "Encoder", "-" * 16)
        entered_message = input("Input the text to be Encoded: \n")
        encoded_message = ''.join(self.new_key[self.old_key.index(char)] if char in self.old_key else char for char in entered_message)
        print(f"Output: {encoded_message}")
        self.Choice_CLI()

    def Msg_Decode(self):
        print("-" * 16, "Decoder", "-" * 16)
        entered_message = input("Input the text to be Decoded: \n")
        decoded_message = ''.join(self.old_key[self.new_key.index(char)] if char in self.new_key else char for char in entered_message)
        print(f"Output: {decoded_message}")
        self.Choice_CLI()

    def File_Encode_Decode(self, file_path, mode):
        if not os.path.isfile(file_path):
            print("Entered File does not exist.")
            return

        with open(file_path, "r") as txtfile:
            all_text = txtfile.read()

        dir_name, base_file_name = os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0]
        extension = os.path.splitext(file_path)[1]
        new_file_path = os.path.join(dir_name, f"{base_file_name}_{'encoded' if mode == 'e' else 'decoded'}{extension}")

        if mode == 'e':
            message = ''.join(self.new_key[self.old_key.index(char)] if char in self.old_key else char for char in all_text)
        else:
            message = ''.join(self.old_key[self.new_key.index(char)] if char in self.new_key else char for char in all_text)

        with open(new_file_path, "w") as txtfile:
            txtfile.write(message)

        print(f"{'Encoded' if mode == 'e' else 'Decoded'} file created at: {new_file_path}")

    def Fourth_Choice_CLI(self):
        print("-" * 16, "Search for File", "-" * 16)
        search_root = input("Enter the root directory to start the search (e.g., C:\\): ").strip()
        search_pattern = input("Enter the file name or pattern to search for: ").lower()

        def find_files(root, pattern):
            print("Searching...")
            matches = []
            try:
                regex_pattern = re.compile(f".*{re.escape(pattern)}.*", re.IGNORECASE)
                for path, _, files in os.walk(root):
                    for name in files:
                        if regex_pattern.search(name.lower()):
                            matches.append(os.path.join(path, name))
            except PermissionError:
                print("Permission denied while accessing some directories.")
            except Exception as e:
                print(f"An error occurred while searching: {e}")
            return matches

        found_files = find_files(search_root, search_pattern)
        if not found_files:
            print("No files found.")
            return

        print("Found files:")
        for idx, file in enumerate(found_files, 1):
            print(f"{idx}: {file}")

        while True:
            try:
                choice = int(input("Enter the number of the file you want to select: "))
                if 1 <= choice <= len(found_files):
                    file_path = found_files[choice - 1]
                    break
                else:
                    print("Please enter a valid number corresponding to a file.")
            except ValueError:
                print("Please enter a valid number.")

        encode_decode = input("Would you like to Encode or Decode the file? (e/d): ").lower()
        if encode_decode in ['e', 'd']:
            self.File_Encode_Decode(file_path, encode_decode)
        else:
            print("Invalid option. Returning to menu.")
        self.Choice_CLI()


    def Choice_CLI(self):
        user_choice = self.Initial_CLI()
        if user_choice == 1:
            self.Msg_Encode()
        elif user_choice == 2:
            self.Msg_Decode()
        elif user_choice == 3:
            self.Fourth_Choice_CLI()
        elif user_choice == 0:
            print("Thanks for using!")

# Key Handling
def save_keys(old_key, new_key, filename="keys.json"):
    file_path = os.path.join(os.getcwd(), filename)  # Save the file in the current working directory
    keys = {'old_key': old_key, 'new_key': new_key}
    with open(file_path, 'w') as file:
        json.dump(keys, file)
    print(f"Keys saved to: {file_path}")  # Debugging line

def load_keys(filename="keys.json"):
    file_path = os.path.join(os.getcwd(), filename)  # Load the file from the current working directory
    print(f"Looking for keys at: {file_path}")  # Debugging line

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            keys = json.load(file)
            return keys['old_key'], keys['new_key']
    else:
        print(f"Keys file not found at {file_path}.")  # Debugging line
        return None, None

if __name__ == "__main__":
    try:
        old_key_list, new_key = load_keys()
        if old_key_list is None or new_key is None:
            raise KeyError("Encryption keys not found.")
    except KeyError as e:
        print(e)
        user_option = input("Would you like to create new keys (y/n): ").lower()
        if user_option == 'y':
            # Generate new keys
            print("Creating new keys...")
            old_key_list = list(string.ascii_lowercase)
            new_key = random.sample(old_key_list, len(old_key_list))

            # Save new keys
            save_keys(old_key_list, new_key)
            print("New keys have been generated and saved.")
        else:
            print("Exiting program.")
            sys.exit(0)

    EncoderDecoder(old_key_list, new_key).Choice_CLI()
