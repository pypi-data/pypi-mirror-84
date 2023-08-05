from datetime import datetime
import random


class long:
    def __init__(self, data):
        self.time2 = datetime.now()
        self.now2 = self.time2.strftime("%Y-%m-%d %H:%M:%S")
        self.dt_start = datetime.strptime(self.now2, "%Y-%m-%d %H:%M:%S")
        self.now_date = datetime.now()
        self.now = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        self.time = 0

    def seconds(self):
        self.time = self.dt_start - self.now
        self.time = int(self.time.total_seconds())

        return self.time

    def minutes(self):
        self.time = self.dt_start - self.now
        self.time = int(self.time.total_seconds() // 60)

        return self.time

    def hours(self):
        self.time = self.dt_start - self.now
        self.time = int(self.time.total_seconds() // 60) // 60

        return self.time

    def days(self):
        self.time = self.dt_start - self.now
        self.time = int((self.time.total_seconds() // 60) // 60) // 24

        return self.time

    def mounts(self):
        self.time = self.dt_start - self.now
        self.time = int(((self.time.total_seconds() // 60) // 60) // 24) // 30

        return self.time

    def years(self):
        self.time = self.dt_start - self.now
        self.time = int(((self.time.total_seconds() // 60) // 60) // 24) // 365

        return self.time


class mathematics:
    def __init__(self):
        self.kolv = 0
        self.result = 0

    def average(self, *nums: int):
        for i in nums:
            self.kolv += 1
            self.result += i
        return float(self.result) / self.kolv


rand = {}


class randoms:

    def __init__(self):
        self.num3 = 0
        self.args_list2 = []
        self.out = []
        self.args_list = {}

    def randint(self, number: int = 1, number2: int = None, key: str = None, array_long: int = 2,
                shuffle_long: int = 1):
        self.num3 += 1
        if key is None:
            key = str(random.randint(1, 999999))
        if number2 is None:
            rand[key] = []
            for i in range(array_long):
                rand[key].append(random.randint(1, number))
            for i in range(shuffle_long):
                random.shuffle(rand[key])

            return rand[key][0], rand[key]
        else:
            rand[key] = []
            for i in range(array_long):
                rand[key].append(random.randint(number, number2))
            for i in range(shuffle_long):
                random.shuffle(rand[key])
            return rand[key][0], rand[key]

    def coise(self, *args, output: int = 1, shuffle_long: int = 2, array_long: int = 1, key: str = None):
        if key is None:
            key = str(random.randint(1, 999999))
        rand[key] = []
        for i in args:
            self.args_list2.append(i)
        for i in range(len(args)):
            self.args_list[str(i)] = self.args_list2[random.randint(0, len(args) - 1)]
        for i in range(array_long):
            rand[key].append(self.args_list[str(random.randint(0, len(args) - 1))])
        for i in range(shuffle_long):
            random.shuffle(rand[key])
        for i in range(output):
            self.out.append(rand[key][i])
        return self.out
