import re

def advance_validate(password):
    #password length
    if len(password) < 8:
        return False, "Password must be atleasr 8 characters long."

    #basic char diversity
    if (not re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
            and re.search(r"[0-9]", password)
            and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False, "Password should contain uppercase, lowercase, numbers, and special characters."

    #identical repeating character
    if re.search(r"(.)\1\1", password):
        return False, "Avoid repeating the same character 3 or more times in a row."

    #sequential char validation
    password_lower = password.lower()
    for i in range(len(password_lower) - 3):
        chunk = password_lower[i:i+4]
        if ord(chunk[1]) == ord(chunk[0]) + 1 and \
            ord(chunk[2]) == ord(chunk[1]) + 1 and \
            ord(chunk[3]) == ord(chunk[2]) + 1: \
            return False, "Weak! Sequential characters like 1234."

        if ord(chunk[1]) == ord(chunk[0]) -1  and \
            ord(chunk[2]) == ord(chunk[1]) - 1 and \
            ord(chunk[3]) == ord(chunk[2]) - 1: \
            return False, "Weak! Reverse Sequential characters like 4321."
    
    # 5. Block notoriously common passwords
    common_blacklist = ["password", "qwerty", "welcome", "admin", "letmein"]
    if any(word in password_lower for word in common_blacklist):
        return False, "Weak! This password contains a commonly blacklisted phrase."
    
    return True, "Password approved."

def main():
    # Test Cases
    test_passwords = [
        "Aa1!aaaa",  # Fails repeating check
        "Abc1234!",  # Fails sequential check
        "Password1!",  # Fails blacklist check
        "P@ssw0rd2026!"  # Passes
    ]
    for pwd in test_passwords:
        result, msg = advance_validate(pwd)
        print(f"Password: {pwd:<15} -> Valid: {result} | Reason: {msg}")

if __name__ == "__main__":
    main()
