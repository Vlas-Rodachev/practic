freq_table = {'a': 'aa', 'b': 'bb', 'c': 'cc'}
reverse = {}
for k, v in freq_table.items():
    reverse[v] = k

print(reverse)