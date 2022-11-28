def find(s):
    otkr = None
    for i in range(len(s)):
        if s[i] == '<':
            otkr = i

        if s[i] == '>' and otkr is not None:
            zakr = i
            res = s[otkr + 1:zakr]
            res = list(res.split(','))
            return res
    return ''

def dw_list(data):
    res = []
    lst = []
    for i in range(len(data)):
        if data[i][1] == '{' or data[i][0] == '{' or len(data[i]) == 1:
            lst.append(data[i][-1])
        if data[i][-1] == ']' or data[i][-1] == '}':
            lst.append(data[i][0])
            res.append(lst)
            lst = []
    return res

str = '<2,3,[{2,2},{3,3}]>'
print(find(str))
print(dw_list(find(str)[2:]))
