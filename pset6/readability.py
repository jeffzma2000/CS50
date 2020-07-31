from cs50 import get_string

# sets the values to 0


letters = 0
words = 1
sentences = 0

# gets text from user


s = get_string("Text: ")

# calculates length of the text


length = len(s)

# considers bad scenarios


if s[0] == " ":
    words = words - 1

if s[length - 1] == " ":
    words = words - 1

for i in range(length):
    if s[i].isalpha() == True:
        letters += 1
    # counts words
    if s[i] == " " and s[i - 1] != " ":
        words += 1
    # counts sentences
    if s[i] == "." or s[i] == "?" or s[i] == "!":
        sentences += 1

# calculates index and grade


L = float(letters) / float(words) * 100
S = float(sentences) / float(words) * 100
index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)


# determines what to print as output


if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
