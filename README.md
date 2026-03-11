Secure Image Vault

A lightweight desktop tool for locking and unlocking files with strong encryption.
Built with Python and Tkinter, it allows you to drag and drop files and protect them with a password.

The application uses AES encryption with HMAC verification to ensure files remain private and tamper-proof.

Features

AES-256 Encryption

Password-based key derivation (PBKDF2)

Integrity protection using HMAC-SHA256

Drag & drop file interface

Master password protection

Protection against brute-force attempts

Simple GUI built with Tkinter

File lock status detection

How It Works

On first launch, the program asks you to create a master password.

Drag a file into the application window.

Choose whether to:

Lock the file (encrypt it)

Unlock the file (decrypt it)

Locked files are marked internally and cannot be decrypted without the correct password.

The application stores encrypted data in this format:

LOCKED + SALT + IV + HMAC + CIPHERTEXT

This ensures both confidentiality and integrity.

Security Details

Encryption: AES-256 (CBC mode)

Key Derivation: PBKDF2

Iterations: 100,000

Authentication: HMAC-SHA256

Salt Size: 16 bytes

Brute Force Protection:

Maximum 5 attempts

30 second lockout after exceeding attempts

Requirements

Python 3.8+

Required libraries:

tkinter
tkinterdnd2
pycryptodome

Install dependencies:

pip install tkinterdnd2 pycryptodome
Running the Application
python main.py

When the app starts:

Set your master password

Drag files into the window

Select Lock or Unlock

Important Notes

If you lose the file password, the file cannot be recovered.

If you lose the master password, the application will not allow access.

The program modifies the file directly, so backups are recommended for sensitive data.

Project Structure
project/
│
├── main.py
├── master.lock
└── README.md
Possible Improvements

File type filtering

Batch encryption

Progress indicator

Dark/light theme toggle

Packaging as a standalone executable

License

MIT License
