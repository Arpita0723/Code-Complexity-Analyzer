def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def count_even(nums):
    count = 0
    for num in nums:
        if num % 2 == 0:
            count += 1
    return count

def main():
    print(fib(5))
    print(count_even([1, 2, 3, 4, 5, 6]))
