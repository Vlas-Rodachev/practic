import struct


class CBOR_Decoder:
    def __init__(self, data, byte_string_shift_1=0, byte_string_shift_2=1):
        self.data = data
        self.byte_string_shift_1 = byte_string_shift_1
        self.byte_string_shift_2 = byte_string_shift_2

    def data_decryption(self):
        main_type_information = bytes.fromhex(self.data[:2])

        incomplete_byte = (struct.unpack('B', main_type_information)[0])

        data_type = (int(incomplete_byte) & 0b11100000) >> 5
        bytes_string = bytes.fromhex(self.data[2:])
        additional_information = int(incomplete_byte) & 0b00011111

        def func_integer(byte_string, additional_information_byte):
            if additional_information_byte == 24:
                x = int(struct.unpack('>B', byte_string)[0])
                return x
            elif additional_information_byte == 25:
                x = int(struct.unpack('>H', byte_string)[0])
                return x
            elif additional_information_byte == 26:
                x = int(struct.unpack('>I', byte_string)[0])
                return x
            elif additional_information_byte == 27:
                x = int(struct.unpack('>Q', byte_string)[0])
                return x
            elif additional_information_byte < 24:
                return additional_information_byte

        def func_integer_negative(byte_string, additional_information_byte):
            if additional_information_byte == 24:
                x = int(struct.unpack('>B', byte_string)[0]) + 1
                return -x
            elif additional_information_byte == 25:
                x = int(struct.unpack('>H', byte_string)[0]) + 1
                return -x
            elif additional_information_byte == 26:
                x = int(struct.unpack('>I', byte_string)[0]) + 1
                return -x
            elif additional_information_byte == 27:
                x = int(struct.unpack('>Q', byte_string)[0]) + 1
                return -x
            elif additional_information_byte < 24:
                x = additional_information_byte + 1
                return -x

        def func_byte_string(byte_string, additional_information_byte):
            if additional_information_byte == 24:
                x = int(struct.unpack('>B', byte_string[:1])[0])
                return list(struct.unpack('s' * x, byte_string[1:]))
            elif additional_information_byte == 25:
                x = int(struct.unpack('>H', byte_string[:2])[0])
                return list(struct.unpack('s' * x, byte_string[2:]))
            elif additional_information_byte == 26:
                x = int(struct.unpack('>I', byte_string[:4])[0])
                return list(struct.unpack('s' * x, byte_string[4:]))
            elif additional_information_byte == 27:
                x = int(struct.unpack('>Q', byte_string[:8])[0])
                return list(struct.unpack('s' * x, byte_string[8:]))
            elif additional_information_byte < 24:
                return list(struct.unpack('s' * additional_information_byte, byte_string[:]))

        def func_string(byte_string, additional_information_byte):
            if additional_information_byte == 24:
                line_str = ''
                k = struct.unpack('>b', byte_string[:1])[0]
                for i in range(k):
                    line_str += str(struct.unpack('c' * k, byte_string[1:])[i])[2:3]
                return line_str
            elif additional_information_byte == 25:
                line_str = ''
                k = struct.unpack('>h', byte_string[:2])[0]
                for i in range(k):
                    line_str += str(struct.unpack('c' * k, byte_string[2:])[i])[2:3]
                return line_str
            elif additional_information_byte == 26:
                line_str = ''
                k = struct.unpack('>i', byte_string[:4])[0]
                for i in range(k):
                    line_str += str(struct.unpack('c' * k, byte_string[4:])[i])[2:3]
                return line_str
            elif additional_information_byte == 27:
                line_str = ''
                k = struct.unpack('>q', byte_string[:8])[0]
                for i in range(k):
                    line_str += str(struct.unpack('c' * k, byte_string[8:])[i])[2:3]
                return line_str
            elif additional_information_byte < 24:
                line_str = ''
                for i in range(additional_information_byte):
                    line_str += str(struct.unpack('c' * additional_information_byte, byte_string[:])[i])[2:3]
                return line_str

        def func_array(byte_string, additional_information_byte):
            if additional_information_byte < 24:
                x = additional_information_byte
                byte_string_truncated = byte_string
            elif additional_information_byte == 24:
                x = int(struct.unpack('>B', byte_string[:1])[0])
                byte_string_truncated = byte_string[1:]

            elif additional_information_byte == 25:
                x = int(struct.unpack('>H', byte_string[:2])[0])
                byte_string_truncated = byte_string[2:]

            elif additional_information_byte == 26:
                x = int(struct.unpack('>I', byte_string[:4])[0])
                byte_string_truncated = byte_string[4:]

            elif additional_information_byte == 27:
                x = int(struct.unpack('>Q', byte_string[:8])[0])
                byte_string_truncated = byte_string[8:]

            array_data = []
            for i in range(x):
                additional_truncated_string_bytes = \
                    byte_string_truncated[i+self.byte_string_shift_1:1+i+self.byte_string_shift_1]
                incomplete_byte_1 = (struct.unpack('>B', additional_truncated_string_bytes)[0])
                data_type_1 = (int(incomplete_byte_1) & 0b11100000) >> 5
                additional_information_1 = int(incomplete_byte_1) & 0b00011111
                if data_type_1 == 0:
                    if additional_information_1 < 24:
                        array_data.append(func_integer(additional_truncated_string_bytes, additional_information_1))
                    elif additional_information_1 == 24:
                        self.byte_string_shift_1 += 1
                        array_data.append(func_integer(
                            byte_string_truncated[i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 1
                    elif additional_information_1 == 25:
                        self.byte_string_shift_1 += 2
                        array_data.append(func_integer(
                            byte_string_truncated[i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 2
                    elif additional_information_1 == 26:
                        self.byte_string_shift_1 += 4
                        array_data.append(func_integer(
                            byte_string_truncated[i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 4
                    elif additional_information_1 == 27:
                        self.byte_string_shift_1 += 8
                        array_data.append(func_integer(
                            byte_string_truncated[i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 8
                elif data_type_1 == 1:
                    if additional_information_1 < 24:
                        array_data.append(func_integer_negative(
                            additional_truncated_string_bytes, additional_information_1))
                    elif additional_information_1 == 24:
                        self.byte_string_shift_1 += 1
                        array_data.append(func_integer_negative(
                            byte_string_truncated[i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 1
                    elif additional_information_1 == 25:
                        self.byte_string_shift_1 += 2
                        array_data.append(func_integer_negative(
                            byte_string_truncated[i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 2
                    elif additional_information_1 == 26:
                        self.byte_string_shift_1 += 4
                        array_data.append(func_integer_negative(
                            byte_string_truncated[i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 4
                    elif additional_information_1 == 27:
                        self.byte_string_shift_1 += 8
                        array_data.append(func_integer_negative(
                            byte_string_truncated[i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 8
                elif data_type_1 == 2:
                    if additional_information_1 < 24:
                        array_data.append(func_byte_string(byte_string_truncated
                                [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1+additional_information_1],
                                                           additional_information_1))
                        self.byte_string_shift_2 += additional_information_1
                        self.byte_string_shift_1 += additional_information_1
                    elif additional_information_1 == 24:
                        self.byte_string_shift_1 += 1
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_byte_string(byte_string_truncated
                                [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1 + q],
                                                           additional_information_1))
                        self.byte_string_shift_2 += 1
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                    elif additional_information_1 == 25:
                        self.byte_string_shift_1 += 2
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_byte_string(byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                           additional_information_1))
                        self.byte_string_shift_2 += 2
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                    elif additional_information_1 == 26:
                        self.byte_string_shift_1 += 4
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_byte_string(byte_string_truncated
                                [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                           additional_information_1))
                        self.byte_string_shift_2 += 4
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                    elif additional_information_1 == 27:
                        self.byte_string_shift_1 += 8
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_byte_string(byte_string_truncated
                                [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                           additional_information_1))
                        self.byte_string_shift_2 += 8
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                elif data_type_1 == 3:
                    if additional_information_1 < 24:
                        array_data.append(func_string(byte_string_truncated
                                [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1+additional_information_1],
                                                      additional_information_1))
                        self.byte_string_shift_2 += additional_information_1
                        self.byte_string_shift_1 += additional_information_1
                    elif additional_information_1 == 24:
                        self.byte_string_shift_1 += 1
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_string(byte_string_truncated
                                [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1 + q],
                                                      additional_information_1))
                        self.byte_string_shift_2 += 1
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                    elif additional_information_1 == 25:
                        self.byte_string_shift_1 += 2
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_string(
                            byte_string_truncated[i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                            additional_information_1))
                        self.byte_string_shift_2 += 2
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                    elif additional_information_1 == 26:
                        self.byte_string_shift_1 += 4
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_string(byte_string_truncated
                                                      [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                      additional_information_1))
                        self.byte_string_shift_2 += 4
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                    elif additional_information_1 == 27:
                        self.byte_string_shift_1 += 8
                        q = struct.unpack('>b', byte_string_truncated
                                [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0]
                        array_data.append(func_string(byte_string_truncated
                                                      [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                      additional_information_1))
                        self.byte_string_shift_2 += 8
                        self.byte_string_shift_2 += q
                        self.byte_string_shift_1 += q
                elif data_type_1 == 7:
                    if additional_information_1 < 24:
                        array_data.append(func_float(additional_truncated_string_bytes, additional_information_1))
                    elif additional_information_1 == 24:
                        self.byte_string_shift_1 += 1
                        array_data.append(func_float(byte_string_truncated
                                                     [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                     additional_information_1))
                        self.byte_string_shift_2 += 1
                    elif additional_information_1 == 25:
                        self.byte_string_shift_1 += 2
                        array_data.append(func_float(byte_string_truncated
                                                     [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                     additional_information_1))
                        self.byte_string_shift_2 += 2
                    elif additional_information_1 == 26:
                        self.byte_string_shift_1 += 4
                        array_data.append(func_float(byte_string_truncated
                                                     [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                     additional_information_1))
                        self.byte_string_shift_2 += 4
                    elif additional_information_1 == 27:
                        self.byte_string_shift_1 += 8
                        array_data.append(func_float(byte_string_truncated
                                                     [i+self.byte_string_shift_2:1 + i + self.byte_string_shift_1],
                                                     additional_information_1))
                        self.byte_string_shift_2 += 8
                # elif data_type_1 == 4:
                #     if additional_information_1 < 24:
                #         # self.u += 1
                #         # q = int(struct.unpack('>b', hh[i + self.uu:1 + i + self.u])[0])
                #         array_data.append(func_array(byte_string_truncated[i + self.byte_string_shift_1 + 1:],
                #                                      additional_information_1)[0])
                #         self.byte_string_shift_1 += additional_information_1
                #         self.byte_string_shift_2 += additional_information_1 + 1
                #     elif additional_information_1 == 24:
                #         self.byte_string_shift_1 += 1
                #         q = int(struct.unpack('>b', byte_string_truncated
                #                 [i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0])
                #         array_data.append(func_array(byte_string_truncated
                #                                      [i+self.byte_string_shift_1:1 + self.byte_string_shift_1 + i + q],
                #                                      additional_information_1)[0])
                #         self.byte_string_shift_1 += additional_information_1 - 1
                #         self.byte_string_shift_2 += additional_information_1
                #     elif additional_information_1 == 25:
                #         self.byte_string_shift_1 += 2
                #         q = int(struct.unpack('>h', byte_string_truncated[i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0])
                #         array_data.append(func_array(byte_string_truncated[i + self.byte_string_shift_2:self.byte_string_shift_1 + 1 + i + q], additional_information_1)[0])
                #         self.byte_string_shift_1 += q
                #         self.byte_string_shift_2 += q + 2
                #     elif additional_information_1 == 26:
                #         self.byte_string_shift_2 += 4
                #         q = int(struct.unpack('>h', byte_string_truncated[i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0])
                #         array_data.append(func_array(byte_string_truncated[i + self.byte_string_shift_2:self.byte_string_shift_1 + 1 + i + q], additional_information_1)[0])
                #         self.byte_string_shift_1 += q
                #         self.byte_string_shift_2 += q + 4
                #     elif additional_information_1 == 27:
                #         self.byte_string_shift_1 += 8
                #         q = int(struct.unpack('>h', byte_string_truncated[i + self.byte_string_shift_2:1 + i + self.byte_string_shift_1])[0])
                #         array_data.append(func_array(byte_string_truncated[i + self.byte_string_shift_2:self.byte_string_shift_1 + 1 + i + q], additional_information_1)[0])
                #         self.byte_string_shift_1 += q
                #         self.byte_string_shift_2 += q + 8

            return array_data

        def func_float(byte_string, additional_information_byte):
            if additional_information_byte == 24:
                x = struct.unpack('>B', byte_string)[0]
                return x
            elif additional_information_byte == 25:
                x = struct.unpack('>e', byte_string)[0]
                return x
            elif additional_information_byte == 26:
                x = struct.unpack('>f', byte_string)[0]
                return x
            elif additional_information_byte == 27:
                x = struct.unpack('>d', byte_string)[0]
                return x
            elif additional_information_byte == 22:
                return None
            elif additional_information_byte == 21:
                return True
            elif additional_information_byte == 20:
                return False

        if data_type == 0:
            return func_integer(bytes_string, additional_information)

        elif data_type == 1:
            return func_integer_negative(bytes_string, additional_information)

        elif data_type == 2:
            return func_byte_string(bytes_string, additional_information)

        elif data_type == 3:
            return func_string(bytes_string, additional_information)

        elif data_type == 4:
            return func_array(bytes_string, additional_information)

        elif data_type == 7:
            return func_float(bytes_string, additional_information)


a = CBOR_Decoder('841A1BBDA4A16568656C6C6F3A00081B56FB405EDD2F1A9FBE77')
print(a.data_decryption())