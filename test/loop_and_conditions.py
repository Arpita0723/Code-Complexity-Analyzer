def check_numbers(nums):
    for num in nums:
        if num % 2 == 0:
            print(num, "is even")
        else:
            print(num, "is odd")

    i = 0
    while i < len(nums):
        print("Index:", i)
        i += 1
