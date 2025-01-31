import pgpy

#Generate a new key pair
"""
This creates a new PGP key pair (public & private key).
Uses RSA algorithm (which supports both encryption and signing).
The key size is 2048 bits (a good balance between security and performance).
"""
key = pgpy.PGPKey.new(pgpy.constants.PubKeyAlgorithm.RSAEncryptOrSign, 2048)
uid = pgpy.PGPUID.new("User", comment="Test key", email="example@example.com")

#Self-sign the key
"""
Self-signing ensures the key is trusted by the owner.
The key is assigned capabilities:
EncryptCommunications: Can be used to encrypt messages.
EncryptStorage: Can be used to encrypt files.
Security parameters:
Hashing Algorithm: SHA256 (for digital signatures).
Encryption Algorithm: AES-256 (strong encryption).
Compression Algorithm: ZLIB (reduces message size before encryption).
"""

key.add_uid(uid, usage={pgpy.constants.KeyFlags.EncryptCommunications,
                        pgpy.constants.KeyFlags.EncryptStorage},
            hashes=[pgpy.constants.HashAlgorithm.SHA256],
            ciphers=[pgpy.constants.SymmetricKeyAlgorithm.AES256],
            compression=[pgpy.constants.CompressionAlgorithm.ZLIB])

#Save the keys
with open("private_key.asc", "w") as f:
    f.write(str(key))

with open("public_key.asc", "w") as f:
    f.write(str(key.pubkey))

print("PGP key generated and saved")