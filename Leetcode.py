'''
Write a function called is_palindrome(s) that returns True if the string s is the same forwards and backwards, and False otherwise.
The function should ignore spaces and capitalization.
12:35 Uhr
print(is_palindrome("racecar")) # Expected: True
print(is_palindrome("hello")) # Expected: False
print(is_palindrome("A  Santa at NASA")) # Expected: True
'''

# def is_palindrome(s):
#     text = s.lower().split()
#     reverse_text = []
#     for item in text:
#         reverse_text.insert(0, item[::-1])
#     old_text = list_to_string(text)
#     new_text = list_to_string(reverse_text)
#     return old_text == new_text
    

# def list_to_string(list):
#     new_string = ""
#     for item in list:
#         new_string += item
#     return new_string

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    s_rev = s[::-1]
    return s == s_rev
            

print(is_palindrome("racecar")) # Expected: True
print(is_palindrome("hello")) # Expected: False
print(is_palindrome("A  Santa at NASA")) # Expected: True
