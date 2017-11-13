

csvfile =open(r'''C:\Users\TSR\Desktop\python\ptt_tag_utf.csv''', 'rb')

a = csvfile.read()
a = str(a)
print(len(a))
print(type(a))
b = a.split(',')
print(a[0:100])
print(b[0])
print(b[1:10])