# Advanced Image Vault

A secure desktop application for encrypting and decrypting files using strong cryptographic standards.
Advanced Image Vault allows users to protect sensitive files with password-based encryption through a simple drag-and-drop interface.

The application is designed with security, simplicity, and usability in mind. Users can lock files with a password, unlock them when needed, and protect access with a master password system.

---

## Overview

Advanced Image Vault is a Python-based GUI application built with Tkinter that provides a secure way to encrypt and decrypt files locally. The application uses modern cryptographic techniques including AES encryption, PBKDF2 key derivation, and HMAC verification to ensure data integrity and confidentiality.

Files can be locked or unlocked simply by dragging them into the application window and choosing the desired action.

---

## Features

• AES-256 encryption for strong file protection
• Password-based encryption using PBKDF2 key derivation
• HMAC verification to detect tampering or corruption
• Master password authentication for application access
• Drag-and-drop file interface
• Protection against brute force attempts with lockout system
• Automatic detection of locked files
• Clean and minimal graphical user interface
• Local encryption with no internet dependency

---

## Security Design

### AES Encryption

Files are encrypted using AES in CBC mode with a 256-bit key.

### Key Derivation

Passwords are converted into encryption keys using PBKDF2 with 100,000 iterations and a random salt.

### HMAC Integrity Check

An HMAC-SHA256 authentication tag ensures that encrypted data has not been modified.

### Lockout Protection

After multiple failed password attempts, the application temporarily locks access to the file to prevent brute-force attacks.

### Master Password

The application requires a master password before access is granted. The password is stored as a SHA-256 hash.

---

## File Structure After Encryption

Encrypted files follow this structure:

```
[LOCKED HEADER]
[SALT]
[IV]
[HMAC TAG]
[CIPHERTEXT]
```

This format ensures that all required information for decryption is securely stored inside the file.

---

## Requirements

Python 3.8 or later

Required libraries:

```
tkinter
tkinterdnd2
pycryptodome
```

Install dependencies using:

```
pip install tkinterdnd2 pycryptodome
```

---

## How to Run

1. Clone or download this repository.
2. Install the required dependencies.
3. Run the application:

```
python main.py
```

On first launch, you will be asked to create a master password.

---

## Usage

### Locking a File

1. Drag and drop a file into the application.
2. Select "Lock".
3. Enter a password.
4. The file will be encrypted and marked as locked.

### Unlocking a File

1. Drag the encrypted file into the application.
2. Select "Unlock".
3. Enter the correct password.
4. The file will be decrypted and restored.

---

## Security Notes

• If the password is lost, the encrypted file cannot be recovered.
• Do not modify encrypted files manually.
• The application performs encryption locally and does not transmit any data.

---

## Project Structure

```
project-folder/
│
├── main.py
├── master.lock
└── README.md
```

---

## Future Improvements

• Support for folder encryption
• Secure file preview mode
• Automatic backup of encrypted files
• Cross-platform executable builds
• Improved file management interface

---

## License

This project is intended for educational and personal use. You may modify and extend it as needed.

---

## Author

Developed as a Python security project demonstrating practical encryption and secure file handling techniques.
