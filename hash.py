from PIL import Image
import numpy
import scipy.fftpack


def phash(img):
    img = img.convert("L").resize((96, 96), Image.ANTIALIAS)  # Сжимаем изображение
    img_pixels = numpy.array(img.getdata(), dtype=numpy.float).reshape((96, 96))  # Получаем его пиксели в NP массив
    transformed = scipy.fftpack.dct(scipy.fftpack.dct(img_pixels, axis=0), axis=1)  # Дискретное косинусное преобразование по
    # обоим осям
    lowfreq = transformed[:24, :24]
    median = numpy.median(lowfreq)  # рассчитываем медианные значения
    return lowfreq > median  # Строит хеш путём поэлементного сравнения
