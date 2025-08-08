from app import security

def test_password_hash_and_verify():
    password = "MySecurePass123"
    hashed = security.hash_password(password)

    # Check the hash is not equal to the original
    assert hashed != password
    assert security.verify_password(password, hashed) is True

    # Check that a wrong password fails
    assert security.verify_password("WrongPassword", hashed) is False
