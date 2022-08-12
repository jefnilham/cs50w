seq = ['abc123', 'def456', 'ghi789', 'ABC']
sub = 'a'

for elem in seq:
    if sub.lower() in elem.lower():
        print(elem)