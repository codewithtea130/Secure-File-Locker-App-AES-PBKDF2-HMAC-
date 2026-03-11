🔐 Secure Image Vault

Secure Image Vault is a lightweight desktop application built with Python that allows users to encrypt and decrypt files securely using a simple drag-and-drop interface.

The application implements AES-256 encryption, PBKDF2 key derivation, and HMAC-SHA256 authentication to ensure that files remain private and protected from tampering.

Overview

Secure Image Vault is designed for users who want a simple way to protect sensitive files locally without relying on cloud services.
Files can be locked (encrypted) and unlocked (decrypted) using a password.

The application also includes master password authentication and brute-force protection to enhance security.

Key Features

AES-256 file encryption

Password-based key derivation (PBKDF2)

File integrity verification using HMAC-SHA256

Drag-and-drop file interface

Master password protection

Brute-force attack protection

Automatic detection of locked files

Minimal and lightweight desktop UI

Encryption Details
Component	Implementation
Encryption Algorithm	AES-256
Mode	CBC (Cipher Block Chaining)
Key Derivation	PBKDF2
Iterations	100,000
Authentication	HMAC-SHA256
Salt Size	16 bytes
Block Size	AES default
Key Length	32 bytes
Security Mechanisms
Feature	Description
Master Password	Required to access the application
File Password	Each file can be encrypted with its own password
HMAC Verification	Prevents file tampering
Attempt Limiting	Maximum 5 failed attempts
Lockout System	30-second lockout after repeated failures
Encrypted File Structure

Encrypted files are stored in the following format:

LOCKED | SALT | IV | HMAC | CIPHERTEXT
Field	Purpose
LOCKED	Identifier marking the file as encrypted
SALT	Used for secure key derivation
IV	Initialization vector for AES
HMAC	Ensures file integrity
CIPHERTEXT	The encrypted file content
Installation
1. Clone the repository
git clone https://github.com/yourusername/secure-image-vault.git
cd secure-image-vault
2. Install dependencies
pip install tkinterdnd2 pycryptodome
Running the Application
python main.py
First Launch

When the application runs for the first time, you will be prompted to create a master password.

Usage

Launch the application.

Drag a file into the Drag & Drop area.

Choose one of the following actions:

Lock – Encrypt the file with a password.

Unlock – Decrypt the file using the correct password.

The file will be updated automatically.

Project Structure
secure-image-vault/
│
├── main.py
├── master.lock
└── README.md
File	Description
main.py	Main application script
master.lock	Stores the hashed master password
README.md	Project documentation
Requirements
Requirement	Version
Python	3.8+
tkinter	Built-in
tkinterdnd2	Latest
pycryptodome	Latest
Important Notes

Losing the file password means the encrypted file cannot be recovered.

Losing the master password will prevent access to the application.

The program modifies files directly, so keeping backups is recommended for important files.

Future Improvements

Batch file encryption

File preview before encryption

Standalone executable build

Theme customization

Multi-file drag and drop processing

License

This project is released under the MIT License.
