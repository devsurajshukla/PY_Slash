name = "Suraj"
age = 34
email = "codingbrains62@gmail.com"
city = "Lucknow"
is_developer = True

print(f"My name is {name}")
print(f" I am {age} years old")
print(f"My email is {email}" )
print(f"I live in {city}")
print(f"Am I a developer? {is_developer}")


print(type(name))
print(type(age))
print(type(email))
print(type(city))
print(type(is_developer))


names = ["Suraj", "Rahul", "Ramesh", "Suresh"]

names.append("Rohit")

names.remove("Ramesh")

print(names)
print(names[0])
print(names[1])
print(names[2])
print(names[3])
print(len(names))



user = {
    "name": "Suraj",
    "age": 34,
    "email": "codingbrains62@gmail.com",
    "city": "Lucknow"
}
user["phone"] = "9999999999"
user["age"] = 99

print(user)
print(user["name"])
print(user["age"])
print(user["email"])
print(user["city"])
print(user["phone"])
print(len(user))

print(user.keys())
print(user.values())
print(user.items())
print(user.get("name"))
del user["phone"]
print(user)

print("------------------------------------ ")





userData = [
    {
        "id": 1,
        "name": "Suraj",
        "age": 34,
        "email": "codingbrains62@gmail.com",
        "city": "Lucknow",
    },
    
    {
        "id": 2,
        "name": "Rahul",
        "age": 30,
        "email": "codingbrains32@gmail.com",
        "city": "Delhi",
    },
    
    {
        "id": 3,
        "name": "Ramesh",
        "age": 28,
        "email": "codingbrains33@gmail.com",
        "city": "Mumbai",
    },
]

print(userData[0])

print("for Loop")
for name in userData:
    print(name["name"])
    print(name["age"])
    print(name["email"])
    print(name["city"])
    print("-------------------")


print("------------------------------------ ")

age = 35

if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")


user_input = input("Enter your age: ")
if user_input.isdigit():
    age = int(user_input)
    if age >= 18:
        print("You are eligible to vote.")
    else:
        print("You are not eligible to vote.")

user = {
    "name": "Suraj",
    "age": 34,
    "email": "codingbrains62@gmail.com",
    "city": "Lucknow",
    "Role": "Developer",
    "is_active": True
}

if user["is_active"]:
    print(f"{user['name']} is an active user.")
elif user["Role"] == "Developer":
    print(f"{user['name']} is a developer.")
else:
    print(f"{user['name']} is not an active user.")

print("------------------------------------ ")
print("for Loop")

users = [
    {
        "id": 1,
        "name": "Suraj",
        "role": "admin"
    },
    {
        "id": 2,
        "name": "Amit",
        "role": "user"
    },
    {
        "id": 3,
        "name": "Rahul",
        "role": "user"
    }
]

for user in users:
      print(user["name"])
      if user["role"] == "admin":
       print(f"{user['name']} is an admin.")



print("------------------------------------ ")
print("while Loop")

number = 1
while number <5:
    print(number)
    number += 1


print("------------------------------------ ")

def introduce(name, age, city):
    return f"My name is {name}, I am {age} years old and I live in {city}."


message = introduce("Suraj", 34, "Lucknow")

print(message)