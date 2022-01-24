from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from transliterate import translit
from time import time
from django.core.files.storage import FileSystemStorage
from django.conf import settings


upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='/uploads')


class News (models.Model):
    """ модель для сущности 'новость' """
    title = models.CharField(max_length=200, db_index=True, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Основной текст')
    img = models.ImageField(upload_to='image/', verbose_name='Изображение', max_length=255, blank=True,
                            default='pictures/base.jpg', storage=upload_storage)
    slug = models.SlugField(max_length=150, default="", unique=True, blank=True)
    date_pub = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date = models.DateField()

    def save(self, *args, **kwargs):
        """переопределяем метод save"""
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """возвращает ссылку на конкретный экземпляр класса"""
        return reverse('news_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        """Переопределяем метод String"""
        return self.title

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Новость'
        verbose_name_plural = 'Добавить новости'


def gen_slug(s):
    """автогенерация слагов"""
    str1 = translit(s, "ru", reversed=True)
    new_slug = slugify(str1, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class NewsFile(models.Model):
    """ модель для сущности 'файлы для новости' """
    name_file = models.CharField(max_length=100, verbose_name='Имя файла (по умолчанию="Открыть"', default="Открыть")
    file = models.FileField(upload_to='files', storage=upload_storage, verbose_name='Прикрепить файл')
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='linked_file',
                             verbose_name='Выберите новость, для которой прикрепляется файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_file

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Файл для новости'
        verbose_name_plural = 'Добавить файлы для новости'


"""
    Бакалавриат
"""


class EducationalForm(models.Model):
    """модель для сущности 'Форма обучения' """
    name_educational_form = models.CharField(max_length=64)

    def __str__(self):
        """переопределяем метод String"""
        return self.name_educational_form


class Orders(models.Model):
    """ модель для сущности 'Приказы БАКАЛАВРИАТ' """
    name_order = models.CharField(max_length=256, verbose_name='Название')
    number_order = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalForm', on_delete=models.PROTECT, related_name='linked_orders',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_order

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Приказ о зачислении(бакалавриат)'
        verbose_name_plural = 'Приказы о зачислении - БАКАЛАВРИАТ'


class EducationalFormSpec(models.Model):
    """модель для сущности 'Форма обучения ' """
    name_educational_form = models.CharField(max_length=64)

    def __str__(self):
        """переопределяем метод String"""
        return self.name_educational_form


class OrdersSpec(models.Model):
    """ модель для сущности 'Приказы СПЕЦИАЛИТЕТ' """
    name_order = models.CharField(max_length=256, verbose_name='Название')
    number_order = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalFormSpec', on_delete=models.PROTECT, related_name='linked_orders', verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_order

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Приказ о зачислении(специалитет)'
        verbose_name_plural = 'Приказы о зачислении - СПЕЦИАЛИТЕТ'




class Result(models.Model):
    """ модель для сущности 'Результаты вступительных БАКАЛАВРИАТ' """
    name_result = models.CharField(max_length=256, verbose_name='Название')
    number_result = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalForm', on_delete=models.PROTECT, related_name='linked_results',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_result = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_result

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Результаты вступительных испытаний (бакалавриат)'
        verbose_name_plural = 'Результаты вступительных испытаний - БАКАЛАВРИАТ'


class RecommendedList(models.Model):
    """ модель для сущности 'Рекомендованные к зачислению БАКАЛАВРИАТ' """
    name_rec_list = models.CharField(max_length=256, verbose_name='Название')
    educational_form = models.ForeignKey('EducationalForm', on_delete=models.PROTECT, related_name='linked_rec_list',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_rec_list

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Списки рекомендованных к зачислению(бакалавриат)'
        verbose_name_plural = 'Списки рекомендованных к зачислению - БАКАЛАВРИАТ'


"""
    Магистратура
"""


class EducationalFormMag(models.Model):
    """модель для сущности 'Форма обучения ' """
    name_educational_form = models.CharField(max_length=64)

    def __str__(self):
        """переопределяем метод String"""
        return self.name_educational_form


class OrdersMag(models.Model):
    """ модель для сущности 'Приказы Магистратура' """
    name_order = models.CharField(max_length=256, verbose_name='Название')
    number_order = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalFormMag', on_delete=models.PROTECT, related_name='linked_orders',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_order

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Приказ о зачислении(магистратура)'
        verbose_name_plural = 'Приказы о зачислении - МАГИСТРАТУРА'


class ResultMag(models.Model):
    """ модель для сущности 'Результаты вступительных МАГИСТРАТУРА' """
    name_result = models.CharField(max_length=256, verbose_name='Название')
    number_result = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalFormMag', on_delete=models.PROTECT, related_name='linked_results',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_result = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_result

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Результаты вступительных испытаний (Магистратура)'
        verbose_name_plural = 'Результаты вступительных испытаний - МАГИСТРАТУРА'


class RecommendedListMag(models.Model):
    """ модель для сущности 'Рекомендованные к зачислению Магистратура' """
    name_rec_list = models.CharField(max_length=256, verbose_name='Название')
    educational_form = models.ForeignKey('EducationalFormMag', on_delete=models.PROTECT, related_name='linked_rec_list',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_rec_list

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Списки рекомендованных к зачислению(магистратура)'
        verbose_name_plural = 'Списки рекомендованных к зачислению - МАГИСТРАТУРА'


"""
    Аспирантура
"""


class EducationalFormAsp(models.Model):
    """модель для сущности 'Форма обучения ' """
    name_educational_form = models.CharField(max_length=64)

    def __str__(self):
        """переопределяем метод String"""
        return self.name_educational_form


class OrdersAsp(models.Model):
    """ модель для сущности 'Приказы Магистратура' """
    name_order = models.CharField(max_length=256, verbose_name='Название')
    number_order = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalFormAsp', on_delete=models.PROTECT, related_name='linked_orders',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_order

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Приказ о зачислении(аспирантура)'
        verbose_name_plural = 'Приказы о зачислении - АСПИРАНТУРА'


class ResultAsp(models.Model):
    """ модель для сущности 'Результаты вступительных АСПИРАНТУРА' """
    name_result = models.CharField(max_length=256, verbose_name='Название')
    number_result = models.CharField(max_length=64, verbose_name='Номер документа')
    educational_form = models.ForeignKey('EducationalFormAsp', on_delete=models.PROTECT, related_name='linked_results',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_result = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_result

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Результаты вступительных испытаний (Аспирантура)'
        verbose_name_plural = 'Результаты вступительных испытаний - АСПИРАНТУРА'


class RecommendedListAsp(models.Model):
    """ модель для сущности 'Рекомендованные к зачислению Аспирантура' """
    name_rec_list = models.CharField(max_length=256, verbose_name='Название')
    educational_form = models.ForeignKey('EducationalFormAsp', on_delete=models.PROTECT, related_name='linked_rec_list',
                                         verbose_name='Форма обучения')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_order = models.DateField(verbose_name='Дата создания приказа')
    file = models.FileField(upload_to='files', verbose_name='Файл')

    def __str__(self):
        """переопределяем метод String"""
        return self.name_rec_list

    def get_url_file(self):
        s = '/static/media'
        url_img = s + self.file.url
        return url_img

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Списки рекомендованных к зачислению(аспирантура)'
        verbose_name_plural = 'Списки рекомендованных к зачислению - АСПИРАНТУРА'


