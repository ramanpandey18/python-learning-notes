import re
emails = ["alice@example.com", "test@123@gamil.com", "123@example.com", "test.com", "abc@gmailcom"]

def get_name(email, strict=False):
    email = email.strip()
    count = email.count("@")

    if count == 0:                        # no "@" -> always reject
        return None
    if strict and count > 1:              # multiple "@" -> reject only in strict mode
        return None

    name, domain = email.split("@", 1)    # otherwise keep the first "@"
    if not name or "." not in domain:
        return None
    return name


def get_name_regex(email):
    m = re.fullmatch(r"([^@\s]+)@([^@\s]+\.[^@\s]{2,})", email.strip())
    return m.group(1) if m else None

print("1. Handle multiple @ (keep the first):")
for e in emails:
    print(e, "->", get_name(e))

print("\n2. Reject multiple @ or 0 @:")
for e in emails:
    print(e, "->", get_name(e, strict=True))
