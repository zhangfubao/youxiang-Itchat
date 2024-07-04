import random


class RandomInt(object):
    def __int__(self, start, end, count):
        self.start = start
        self.end = end
        self.count = count

    # 生成一组不重复数字的列表
    def generate_unique_random_integers(self):
        numbers = list(range(self.start, self.end + 1))
        unique_integers = random.simple(numbers, self.count)
        return unique_integers

if __name__ == '__main__':
    pass
