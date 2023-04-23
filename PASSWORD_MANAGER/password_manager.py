import sqlite3  # sqlite3 kur !!!
from cryptography.fernet import Fernet # cryptography kur !!!

# Veritabanı bağlantısı
conn = sqlite3.connect('passwords.db')

# Veritabanı tablosu oluşturma
conn.execute('''CREATE TABLE IF NOT EXISTS passwords
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             USERNAME TEXT NOT NULL,
             PASSWORD TEXT NOT NULL,
             WEBSITE TEXT);''')

# Şifreleme anahtarını oluşturma
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Yeni bir kullanıcı girişi oluşturma
def new_entry(username, password, website=''):
    encrypted_password = cipher_suite.encrypt(password.encode())
    conn.execute(f"INSERT INTO passwords (USERNAME, PASSWORD, WEBSITE) VALUES ('{username}', '{encrypted_password.decode()}', '{website}');")
    conn.commit()

# Kayıtlı girişleri listeleme
def list_entries():
    entries = conn.execute('SELECT * FROM passwords;').fetchall()
    for entry in entries:
        password = cipher_suite.decrypt(entry[2].encode()).decode()
        print(f"ID: {entry[0]} - Username: {entry[1]} - Password: {password} - Website: {entry[3]}")

# Kullanıcı arayüzü
while True:
    print("1. New Entry")
    print("2. List Entries")
    print("3. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        website = input("Enter website: ")
        new_entry(username, password, website)
        print("Entry added!")

    elif choice == '2':
        list_entries()

    elif choice == '3':
        break

conn.close()
