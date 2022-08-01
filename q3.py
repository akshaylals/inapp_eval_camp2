deno = (2000, 500, 200, 100, 50, 20, 10, 5, 2, 1)

while True:
    try:
        N = int(input('Enter an amount: '))
    except:
        print('Invalid Input')
    else:
        break

for i in deno:
    if N // i:
        print(i, N // i)
        N %= i