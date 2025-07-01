def analyze(num):
    if num > 0:
        if num % 2 == 0:
            for i in range(num):
                print(i)
        else:
            print("Odd positive")
    else:
        print("Negative")
