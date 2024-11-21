# SecurePasswordManager | Cybersecurity Project

## Overview
This project is a secure and robust password manager application developed using Python and advanced cryptographic techniques. The goal is to provide a secure solution for storing, retrieving, and managing user credentials, while ensuring the highest levels of data protection and confidentiality.

## Key Features

- **Secure Master Password Management**: Utilizes **Argon2** hashing for secure storage of the master password, offering protection against brute-force and rainbow table attacks.
- **Encryption & Decryption**: Implements **AES-256** encryption to protect stored passwords in the database. Passwords are securely encrypted using keys derived from the master password and a salt.
- **Password Key Derivation**: Uses **scrypt** for generating AES-256 encryption keys from the master password and salt to ensure secure password storage and retrieval.
- **Password Generator**: Provides a tool for generating strong, random passwords of configurable lengths, improving password strength and security.
- **Password Strength Checker**: Evaluates and encourages strong password practices by assessing password length, character diversity, and estimated cracking time for improved user security.
- **Database Management**: Configured a **MySQL** database to store encrypted password entries with seamless management of password data. Includes options to create, remove, and reconfigure the database schema.

## Technologies Used
- **Python**: Primary programming language for developing the application.
- **Argon2**: Used for secure password hashing.
- **scrypt**: Key derivation function for generating encryption keys.
- **AES-256**: Applied for strong encryption of user passwords.
- **MySQL**: Database management system used to securely store encrypted password data.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Pawar-Tushar/SecurePasswordManager.git
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
1. Configure the database connection in the dbconfig.py and Run this cmd :
   ```bash
   python db.py
2. Run the application:
   ```bash
   python main.py

## Usage

- **Add Password:** Add a new password entry to the database by entering a title, username, and password. The password will be encrypted before being stored.
- **Retrieve Password:** Search and retrieve encrypted password entries based on the title or username.
- **Generate Password:** Use the password generator to create a random, strong password and copy it to your clipboard.
- **Check Password Strength:** Use the built-in password strength checker to evaluate the security of any password based on various criteria.

## Contributing

- Fork the repository.
- Create a new branch for your feature or fix.
- Make your changes and commit them.
- Push your changes to your forked repository.
- Open a pull request to contribute your changes.

## Acknowledgements

- Thanks to the open-source community for providing the cryptographic libraries that made this project possible.
- The `pycryptodome` and `mysql-connector` libraries were crucial in implementing encryption and database management for this project.

## Contact

For any queries or issues, feel free to reach out via GitHub Issues or email me at [tusharpawar@749963.com].

 
