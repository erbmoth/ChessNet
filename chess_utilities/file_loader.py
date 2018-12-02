import numpy as np


def generator_data(file_list):
    for f in file_list:
        with open(f) as fd:
            for line in fd:
                a = np.fromstring(line.strip(), sep=',')
                x = a[0:768]
                y = a[768:896]
                yield (x, y)


def generator_batch(generator, size):
    k = 0
    x_batch = np.zeros([size, 768])
    y_batch = np.zeros([size, 128])
    for (x, y) in generator:
        x_batch[k, :] = x
        y_batch[k, :] = y
        k = k + 1
        if k == size:
            k = 0
            yield (x_batch, y_batch)


def generator_data_endless(file_list):
    while True:
        for f in file_list:
            with open(f) as fd:
                for line in fd:
                    a = np.fromstring(line.strip(), sep=',')
                    x = a[0:768]
                    y = a[768:896]
                    if x.size != 768 or y.size != 128 or np.sum(y) != -124:
                        # print('Falsche Daten')
                        # print(x)
                        # print(y)
                        break
                    yield (x, y)


def get_number_of_samples(file_list):
    number_of_samples = 0
    for f in file_list:
        with open(f) as fd:
            for line in fd:
                number_of_samples = number_of_samples + 1
    return number_of_samples


def load_into_ram(file_list, number_of_samples):
    data = np.zeros([number_of_samples, 768], dtype=np.int8)
    label = np.zeros([number_of_samples, 128], dtype=np.int8)
    c = 0
    for (x, y) in generator_data(file_list):
        data[c, :] = x
        label[c, :] = y
        c = c + 1
        if c % 3000 == 0:
            print(c * 100 / number_of_samples, '% loaded into RAM\r', end="")
    return [data, label]