hallo=7
for y in range(0, 3):
    for x in range(0, 3):
        if y < x:
            print(' ',end='')
    print('*',end='')
    for x in range(0, 3):
        if y > x:
            print('*',end='')
            print('*',end='')
    print()
    
for y in range(0, 2):
    for x in range(-1, 3):
        if y > x:
            print(' ', end='')
    print('*',end='')
    for x in range(0, 2):
        if y < x:
            print('*',end='')
            print('*',end='')
    print()