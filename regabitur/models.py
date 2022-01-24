from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


def user_directory_path(instance, filename):
    """функция для записи файлов в папки с ф.и. абитуриента"""
    # file will be uploaded to MEDIA_ROOT/user_<id> + full_name
    filename = '{0}: {1}'.format(instance.name_doc, filename)
    return '{0}_{1}/{2}'.format(instance.user.pk, instance.user.get_full_name(), filename)


class CustomUser(models.Model):
    """Расширение для базового класса User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='',
                                verbose_name='Абитуриент', related_name='custom')
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    patronymic = models.CharField(verbose_name="Отчество (при наличии)", max_length=80,
                                  default='', blank=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=15, default='')
    status_list = (
        ('error', 'Вероятно, вы указали неверные данные электронной почты или номер телефона. '
                  'Пожалуйста, свяжитесь с сотрудниками академии по телефону'),
        ('no', 'Документы не поданы'),
        ('send',
         'Документы отправлены и ждут обработки сотрудниками приемной комисси'),
        ('working', 'Документы находятся в обработке'),
        ('success', 'Документы обработаны и приняты'),
        ('back', 'Документы отозваны')
    )
    # статус заявки
    sending_status = models.CharField(max_length=256, verbose_name="Статус заявки",
                                      choices=status_list, default='no')
    # статус отправки документов
    complete_flag = models.BooleanField(default=False, verbose_name="Документы отправлены?:")
    # статус принятия соглашения о персональных данных
    agreement_flag = models.BooleanField(default=False, verbose_name="Соглашение:")
    work_flag = models.BooleanField(default=False, verbose_name="Взят в работу:")
    success_flag = models.BooleanField(default=False, verbose_name="Отработан:")
    comment_admin = models.TextField(verbose_name="Комментарий для внутренней работы", blank=True)
    address = models.CharField(max_length=400, verbose_name="Адрес регистрации (по паспорту)", blank=True, default=' ')
    passport = models.CharField(max_length=20, verbose_name="Паспортные данные(серия-номер)", blank=True, default=' ')
    snils = models.CharField(max_length=32, verbose_name="Номер снилса", default=' ')
    name_uz = models.CharField(max_length=256, verbose_name="Наименование учебного заведения, которое окончил(а)",
                               blank=True, default=' ')
    date_of_doc = models.CharField(max_length=32,
                                   verbose_name="Дата выдачи документа об образовании в формате ДД.ММ.ГГГГ",
                                   default=" ")
    message = models.TextField(verbose_name='Сообщение от приемной комисии', default=' ', blank=True)

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Абитуриент'
        verbose_name_plural = 'Абитуриента'

    def __str__(self):
        """Переопределяем метод String"""
        name_field = ("id = " + str(self.user.id) + " / " + self.user.get_full_name())
        return name_field


class DocumentUser(models.Model):
    """модель БД для подачи документов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Абитуриент", default='')
    date_pub = models.DateTimeField(auto_now=True, blank=True)

    # лист для дроп меню документов
    document_list = (
        ('Заявление', 'Заявление'),
        ('Учетная карточка', 'Учетная карточка'),
        ('Согласие на зачисление', 'Согласие на зачисление'),
        ('Обработка персональных данных', 'Обработка персональных данных'),
        ('Фото (3х4)', 'Фото (3х4)'),
        ('Документ, удостоверяющий личность', 'Документ, удостоверяющий личность'),
        ('Временная регистрация', 'Временная регистрация(при наличии в СПб)'),
        ('Документ об образовании', 'Документ об образовании'),
        ('мед.справка', 'Медицинская справка по форме 086-У'),
        ('Прививочный сертификат', 'Прививочный сертификат'),
        ('Военный билет или приписное', 'Военный билет или приписное удостоверение'),
        ('Снилс', 'Снилс'),
        ('Индивидуальные достижения', 'Индивидуальные достижения'),
    )

    name_doc = models.CharField(max_length=256, verbose_name="Название документа",
                                choices=document_list)
    doc = models.FileField(upload_to=user_directory_path, verbose_name="Загрузить документ")

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Документы абитуриентов'
        verbose_name_plural = 'Документы абитуриентов'

    def delete(self, *args, **kwargs):
        """Функция удаления файла с сервера при удалении записи файла из БД"""
        # До удаления записи получаем необходимую информацию
        storage, path = self.doc.storage, self.doc.path
        # Удаляем сначала модель ( объект )
        super(DocumentUser, self).delete(*args, **kwargs)
        # Потом удаляем сам файл
        storage.delete(path)


class ChoicesProfile(models.Model):
    """Выбор профиля обучения"""
    description = models.CharField(max_length=256)

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Профиль обучения'
        verbose_name_plural = 'Профили обучения'

    def __str__(self):
        return self.description


class AdditionalInfo(models.Model):
    """Класс с дополнительной информацией о пользователе (прием 21/22)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", default='',
                                related_name='addition')
    education_profile = models.ManyToManyField(ChoicesProfile, verbose_name="Форма обучения")

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Выбранные профили обучения'
        verbose_name_plural = 'Выбранные профили обучения'


class PublishTab(models.Model):
    """Публикация пользователей в списках подавших документы"""

    choice_field = (
        ('ЕГЭ', 'ЕГЭ'),
        ('Вступительные испытания', 'Вступительные испытания'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", default='',
                                related_name='publish')
    individual_str = models.CharField(max_length=32, blank=True, verbose_name="Год/поток (после значения не забудьте"
                                                                              " поставить знак '-'", default='34/21-')
    test_type = models.CharField(max_length=256, verbose_name="Вступительные испытания",
                                 choices=choice_field)
    date_pub = models.DateTimeField(auto_now=True, blank=True, null=True)
    bak_ofo_up = models.BooleanField(default=False, verbose_name="Опубликовать в БАК ОФО УП")
    bak_ofo_gp = models.BooleanField(default=False, verbose_name="Опубликовать в БАК ОФО ГП")
    bak_zfo_up = models.BooleanField(default=False, verbose_name="Опубликовать в БАК ЗФО УП")
    bak_zfo_gp = models.BooleanField(default=False, verbose_name="Опубликовать в БАК ЗФО ГП")
    bak_ozfo_up = models.BooleanField(default=False, verbose_name="Опубликовать в БАК ОЗФО УП")
    bak_ozfo_gp = models.BooleanField(default=False, verbose_name="Опубликовать в БАК ОЗФО ГП")
    spec_ofo_sd = models.BooleanField(default=False, verbose_name="Опубликовать в СПЕЦ ОФО Судеб. деят.")
    mag_ofo_po = models.BooleanField(default=False, verbose_name="Опубликовать в МАГ ОФО Прав. обеспеч.")
    mag_zfo_po = models.BooleanField(default=False, verbose_name="Опубликовать в МАГ ЗФО Прав. обеспеч.")
    mag_ofo_tp = models.BooleanField(default=False, verbose_name="Опубликовать в МАГ ОФО Теор. и практ.")
    mag_zfo_tp = models.BooleanField(default=False, verbose_name="Опубликовать в МАГ ЗФО Теор. и практ.")
    asp_ofo_tip = models.BooleanField(default=False, verbose_name="Опубликовать в АСП ОФО Теор. и истор.")
    asp_zfo_tip = models.BooleanField(default=False, verbose_name="Опубликовать в АСП ЗФО Теор. и истор.")
    asp_ofo_up = models.BooleanField(default=False, verbose_name="Опубликовать в АСП ОФО Уголовный проц.")
    asp_zfo_up = models.BooleanField(default=False, verbose_name="Опубликовать в АСП ЗФО Уголовный проц")
    asp_ofo_ks = models.BooleanField(default=False, verbose_name="Опубликовать в АСП ОФО Криминалистика")
    asp_zfo_ks = models.BooleanField(default=False, verbose_name="Опубликовать в АСП ЗФО Криминалистика")

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Опубликовать в списки подавших'
        verbose_name_plural = 'Опубликовать в списки подавших'

    def __str__(self):
        return self.user.get_full_name()


class PublishRecTab(models.Model):
    """Класс для публикации абитуриентов в списах Рекомендованных к зачислению"""
    choice_field = (
        ('ЕГЭ', 'ЕГЭ'),
        ('Вступительные испытания', 'Вступительные испытания'),
    )
    choice_sost = (
        ('Рекомендован', 'Рекомендован'),
        ('Не рекомендован', 'Не рекомендован'),
    )
    choice_sogl = (
        ('Подано', 'Подано'),
        ('Не подано', 'Не подано'),
        ('Отозвано', 'Отозвано'),
    )
    choice_advantage = (
        ('Имеет', 'Имеет'),
        ('Не имеет', 'Не имеет'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", default='',
                                related_name='publishRec')
    test_type = models.CharField(max_length=256, verbose_name="Вступительные испытания",
                                 choices=choice_field)
    date_pub = models.DateTimeField(auto_now=True, blank=True, null=True)
    sogl = models.CharField(max_length=256, choices=choice_sogl,
                            default=choice_sogl[1], verbose_name="Согласие на зачисление")
    sost_type = models.CharField(max_length=256, verbose_name="Состояние",
                                 choices=choice_sost, default=choice_sost[0])
    advantage = models.CharField(max_length=256, blank=True, default=choice_advantage[1],
                                 choices=choice_advantage, verbose_name='Преимущественное право')
    individ = models.SmallIntegerField(blank=True, default=0, verbose_name='Индивид. достижения')
    rus_point = models.SmallIntegerField(blank=True, default=0, verbose_name='Русский язык')
    obsh_point = models.SmallIntegerField(blank=True, default=0, verbose_name='Обществознание')
    history_point = models.SmallIntegerField(blank=True, default=0, verbose_name='История')
    foreign_language_point = models.SmallIntegerField(blank=True, default=0, verbose_name='Иностранный язык')
    gp_point = models.SmallIntegerField(blank=True, default=0, verbose_name='ГП')
    tgp_point = models.SmallIntegerField(blank=True, default=0, verbose_name='ТГП')
    up_point = models.SmallIntegerField(blank=True, default=0, verbose_name='УП')
    kp_point = models.SmallIntegerField(blank=True, default=0, verbose_name='Конст. Право РФ')
    okp_point = models.SmallIntegerField(blank=True, default=0, verbose_name='ОКП')
    spec_point = models.SmallIntegerField(blank=True, default=0, verbose_name='Спец. дисциплина (Асп)')
    sum_points = models.SmallIntegerField(blank=True, default=0, verbose_name='Сумма баллов')

    bak_ofo_gp = models.BooleanField(default=False, verbose_name="БАК ОФО ГП")
    bak_ofo_up = models.BooleanField(default=False, verbose_name="БАК ОФО УП")
    bak_zfo_gp = models.BooleanField(default=False, verbose_name="БАК ЗФО ГП")
    bak_zfo_up = models.BooleanField(default=False, verbose_name="БАК ЗФО УП")
    bak_ozfo_gp = models.BooleanField(default=False, verbose_name="БАК ОЗФО ГП")
    bak_ozfo_up = models.BooleanField(default=False, verbose_name="БАК ОЗФО УП")
    # специалитет
    spec_ofo_sd = models.BooleanField(default=False, verbose_name="СПЕЦ ОФО СПД")
    # магистратура
    mag_ofo_po = models.BooleanField(default=False, verbose_name="МАГ ОФО Прав. обеспеч.")
    mag_zfo_po = models.BooleanField(default=False, verbose_name="МАГ ЗФО Прав. обеспеч.")
    mag_ofo_tp = models.BooleanField(default=False, verbose_name="МАГ ОФО Теор. и практ.")
    mag_zfo_tp = models.BooleanField(default=False, verbose_name="МАГ ЗФО Теор. и практ.")
    # аспирантура
    asp_ofo_tip = models.BooleanField(default=False, verbose_name="АСП ОФО Теор. и истор.")
    asp_zfo_tip = models.BooleanField(default=False, verbose_name="АСП ЗФО Теор. и истор.")
    asp_ofo_up = models.BooleanField(default=False, verbose_name="АСП ОФО Уголовный проц.")
    asp_zfo_up = models.BooleanField(default=False, verbose_name="АСП ЗФО Уголовный проц")
    asp_ofo_ks = models.BooleanField(default=False, verbose_name="АСП ОФО Криминалистика")
    asp_zfo_ks = models.BooleanField(default=False, verbose_name="АСП ЗФО Криминалистика")

    def save(self, *args, **kwargs):
        self.sum_points = self.rus_point + self.obsh_point + self.history_point + self.foreign_language_point +\
                          self.gp_point + self.tgp_point + self.up_point + self.okp_point + self.kp_point + \
                          self.individ + self.spec_point
        super().save(*args, **kwargs)

    class Meta:
        """перевод для админпанели"""
        verbose_name = 'Опубликовать в списки ромендованных к зачислению'
        verbose_name_plural = 'Опубликовать в списки ромендованных к зачислению'
        ordering = ['-sum_points']
