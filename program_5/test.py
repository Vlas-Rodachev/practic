import struct

a = bytes.fromhex('2f')
print(len(a))

b = struct.unpack('>b', a)[0]
# c = int(bin(b)[2:])

print((b & 0b11100000) >> 5)
print((b & 0b00011111))
print(int("100001110", 2))


# arr = []
# while a > 0:
#     arr.append(a % 2)
#     a //= 2
#
# while len(arr) % 8 != 0:
#     arr.append(0)
#
# print(len(arr))
# arr.reverse()
#
# print(arr)
#
# t = ''
# for i in arr:
#     t += str(i)
#
# i = 8
# tx = int(t[:3], 2)
# print(tx)
# tr = int(t[3:i], 2)
# print(tr)
# x = int(t[i:i+32], 2)
# print(x)
#
#
# # c = struct.unpack('b', b)
# # print(c)
#
# # 101010100101010
# # &
# # 111000000000000
# # 101000000000000 >>
