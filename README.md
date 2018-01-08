# vault

Simple command line password (or other sensitive data) encryptor that wipes the text from the screen after displaying it for a given duration.

# Prequisites

This script requires PyCrypto, which you can install with something like
`pip install pycrypto`

# Usage
`Usage: vault [add|load] <filename>`

Example showing how to encrypt a new entry:
```
mon@expedit ~/vault $ ./vault.py add bankinfo
 New entry: Moneybags National Bank (acct/routing)              
  msg[masked]: 
 Show message? y/n: n
  key[masked]: 
   again to confirm
  key[masked]: 
 New entry: 
Bye
mon@expedit ~/vault $ 
```
The example above does not show back the secret string, and 'test' is entered as the key.

This example shows how the secret is displayed (in this case "1234567 / 1234567"). The entry is given an index when the file is loaded, and this index is used to choose the entry for decryption. The user is prompted for the key, and if the key is entered successfully, the user is prompted for how long to show the secret for. The example below was shown for 5 seconds, and there is 1 second left on the timer, as seen on the beginning of the line in front of the secret.
```
mon@expedit ~/vault $ ./vault.py load bankinfo
  0 Moneybags National Bank (acct/routing)
  1 Never Gonna Guess Me
Show which line?: 0
  key[masked]: 
   seconds to show (0 forever): 5
1   1234567 / 1234567
```

The seconds entered will tick down to 1 and finally the text will be wiped, after which the script is ready to decrypt another line or exit if [Enter] or [Ctrl-C] is pressed.
```
   seconds to show (0 forever): 5
    xxxxxxxxxxxxxxxxx
Show which line?: 
Bye
```

# Plaintext File Storage

The secret entries are stored in plain text as a label and Base64-encoded pair. The encryption is 128-bit AES in CBC mode, with RIPEMD 160 used to expand the key to the 16-byte needed for the blocksize. The initialization vector is randomly-generated for each message, so even if the same secret is encrypted several times with the same key, the ciphertext will differ dramatically.
```
Moneybags National Bank (acct/routing):ABz1kFrM3eyHcmMc0f4YaOLMSgTGiARaIys8aB2hxjH2HvnUmIy/N4A5YBT133FF
Never Gonna Guess Me:9Q4Tl2z3X00TB9LLk3eqBPi3hJ5Kpx5aS43v0jI4Zx9LGgquL8cylKaeZJfo1/Rz
```
I don't need to tell you why plaintext storage is great.

# Bounty
The entry "Never Gonna Guess Me" in the example above is left as a challenge to all takers to try and decrypt. I'm prepared to offer a laughably small bounty of $10 to the first person that can crack that entry.
