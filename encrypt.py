def encrypt_email(email):
    # email = "732199992@qq.com"
    #
    # email = "1054689185@qq.com"
    email3 = email
    count1 = len(email)

    email = email[0:email.rfind('@', 0)]
    print(email)
    count = len(email)
    email1 = email[0:int(count / 3)]

    email2 = email[int(count / 3):count]
    print(email2)
    email2 = email2.replace(email2, "***")
    email4 = email3[count:count1]
    print(email4)
    email5 = email1 + email2 + email4
    # email = email.replace()
    print(email5)
    return email5
    print(count)