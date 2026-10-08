# types of loop in python
# 1. for loop
# 2. while loop
# 3. do-while loop

# for loop
for i in range(10):   # it print from 0 to 9
    print(i)  

# differente ways of writing for loop
# print even number from 1 to 10
for i in range(1, 10, 2):  # it print from 1 to 9 with step of 2
    print(i)

# print odd number from 1 to 10
for i in range(2, 10, 2):  # it print from 2 to 9 with step of 2
    print(i)    
     





# while loop
i = 1
while i < 10:
    print(i)           # it print from 0 to 9
    i += 1

# different ways of writing while loop
# print even number from 1 to 10
i = 2
while i < 10:
    print(i)
    i += 2

# print odd number from 1 to 10
i = 1
while i < 10:
    print(i)
    i += 2


# do-while loop in python
i = 0
while True:
    print(i)          # it print from 0 to 9
    i += 1
    if i == 10:
        break 


# print factorial of a number
n = 5
factorial = 1
for i in range(1, n+1):
    factorial *= i
print(factorial)   # output: 120   