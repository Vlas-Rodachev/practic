class kpp:
    def __init__(self, number, worker_count=0, kpp_in=0, kpp_out=0):
        self.number = number
        self.kpp_in = kpp_in
        self.kpp_out = kpp_out
        self.worker_count = worker_count

    def worker_kpp_in(self):
        self.kpp_in += 1

    def worker_kpp_out(self):
        self.kpp_out += 1

    def count_worker(self):
        if  self.kpp_in - self.kpp_out < 0:
            self.worker_count = 0
        else:
            self.worker_count = self.kpp_in - self.kpp_out


class worker:
    def __init__(self, name, last_name, patronymic, number_otdel, indicative_number):
        self.name = name
        self.last_name = last_name
        self.patronymic = patronymic
        self.number_otdel = number_otdel
        self.iindicative_number = indicative_number

    def r_in(self, _kpp):
        if self.number_otdel == _kpp.number:
            print('Hello!!!!   ', self.last_name, self.name, self.patronymic)
            _kpp.worker_kpp_in()
            _kpp.count_worker()

    def r_out(self, _kpp):
        if self.number_otdel == _kpp.number:
            print('Good bye!!!!   ', self.last_name, self.name, self.patronymic)
            _kpp.worker_kpp_out()
            _kpp.count_worker()


kpp_1 = kpp(1)
kpp_2 = kpp(2)
kpp_3 = kpp(3)

worker_1 = worker('Ivan', 'Ivanov', 'Ivanovich', 1, 25)
worker_2 = worker('Ivan', 'Ivanov', 'Ivanovich', 1, 26)
worker_3 = worker('Ivan', 'Ivanov', 'Ivanovich', 1, 27)
worker_4 = worker('Ivan', 'Ivanov', 'Ivanovich', 2, 4)
worker_5 = worker('Ivan', 'Ivanov', 'Ivanovich', 3, 37)
worker_6 = worker('Ivan', 'Ivanov', 'Ivanovich', 2, 2)


worker_1.r_in(kpp_1)
worker_2.r_in(kpp_1)
worker_3.r_in(kpp_1)
worker_4.r_in(kpp_2)
worker_5.r_in(kpp_3)
worker_6.r_in(kpp_2)


count_rab = kpp_1.worker_count + kpp_2.worker_count + kpp_3.worker_count

print(count_rab)

print()

worker_1.r_out(kpp_1)
worker_2.r_out(kpp_1)
worker_3.r_out(kpp_1)
worker_4.r_out(kpp_2)
worker_5.r_out(kpp_3)
worker_6.r_out(kpp_2)
worker_6.r_out(kpp_3)
worker_6.r_out(kpp_1)

count_rab = kpp_1.worker_count + kpp_2.worker_count + kpp_3.worker_count

print(count_rab)