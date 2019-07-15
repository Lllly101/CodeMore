user_input = int(input())

hw = "Hello World"

if user_input==0: 
    print(hw)
elif(user_input > 0):
    t = ""
    for i in range(len(hw)):
        steps = i + 1
        t += hw[i]
        if (steps % 2 == 0 or steps == len(hw)):
            print(t)
            t = ""
            
else:
    for i in range(len(hw)):
        print(hw[i])
