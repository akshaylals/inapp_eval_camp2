while True:
    try:
        N = int(input('Enter number of rows: '))
    except:
        print('Invalid Input')
    else:
        break


count = 1
for i in range(1, N + 1):
    for j in range(i):
        print(str(count).ljust(4, ' '), end='')
        count += 1
    print()