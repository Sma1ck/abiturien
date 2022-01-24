from os.path import exists

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import View, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from .forms import *

# Create your views here.
from .models import PublishTab, PublishRecTab


class MainPageView(TemplateView):
    template_name = 'regabitur/reg_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['custom_exist'] = hasattr(user, 'custom')
        context['addition_exist'] = hasattr(user, 'addition')
        return context

# def reg_info(request):
#     """отображает главную страницу приложения regabitur"""
#     return render(request, 'regabitur/reg_info.html')


def agreement_flag(request, pk):
    """обработчик соглашения о персональных данных"""
    if request.user.is_authenticated and request.user.pk == pk:
        if request.method == 'GET':
            abitur = CustomUser.objects.get(user_id=pk)
            abitur.agreement_flag = True
            abitur.save()
    else:
        login_template = 'regabitur/login_abitur.html'
        return render(request, login_template)

    # возвращаемся на предыдущую страницу, используя данные сессии
    request.session['return_path'] = request.META.get('HTTP_REFERER', '/')
    return redirect(request.session['return_path'])


def complete_send(request, pk):
    """Обработчик завершения подачи документов"""
    if (request.user.is_authenticated and request.user.pk == pk):
        if request.method == 'GET':
            abitur = CustomUser.objects.get( user_id=pk)
            abitur.sending_status = 'send'
            abitur.complete_flag = True
            abitur.save()
            print(CustomUser.objects.get(user_id=pk))
    else:
        login_template = 'regabitur/login_abitur.html'
        return render(request, login_template)

    template = 'regabitur/success.html'
    return render(request, template)


class CustomSuccessMessageMixin:
    """Миксин для вывода сообщений при работе с формами"""

    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        """если форма валидна добавляем значение текущего запроса и текущее сообщение (success_msg)"""
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


"""
    Личный кабинет пользователя
"""


class UserRoom(LoginRequiredMixin, ListView):
    """Личный кабинет пользователя"""
    model = CustomUser
    template_name = 'regabitur/user_room.html'

    def get_context_data(self, **kwargs):
        """Переопределяем базовый метод, чтобы передать свой контекст"""
        user = self.request.user
        custom_user = CustomUser.objects.get(user=user.id)
        profile = AdditionalInfo.objects.get(user=user.id)
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(user=user.id)
        context['profile'] = profile.education_profile.all() # выводим информацию из ManyToMany related
        context['status'] = custom_user.get_sending_status_display()
        context['success'] = custom_user.sending_status == 'success'
        context['error'] = custom_user.sending_status == 'error'
        context['agreement'] = custom_user.agreement_flag
        context['is_complete'] = custom_user.complete_flag
        context['custom_exist'] = hasattr(user, 'custom')
        context['addition_exist'] = hasattr(user, 'addition')
        return context


# def get_template_names(self):
#     user = self.request.user
#     custom_exist = hasattr(user, 'custom')
#     addition_exist = hasattr(user, 'addition')
#     if custom_exist and addition_exist:
#         self.template_name = 'regabitur/user_room.html'
#     elif custom_exist:
#         self.template_name = 'regabitur/reg_info.html'
#     else:
#         self.template_name = 'regabitur/reg_info.html'
#     return self.template_name


"""
    Добавляем доп. данные  
"""


class InfoCreateView(LoginRequiredMixin, CreateView):
    """Модель для добавления данных в расширенную модель User"""
    model = CustomUser
    template_name = 'regabitur/add_info.html'
    form_class = AddInfoForm
    success_url = reverse_lazy('add_additional_url')
    success_msg = 'Данные успешно добавлены!'

    def form_valid(self, form):
        """Метод сохранения записи за конкретным пользователем"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class InfoUpdateView(LoginRequiredMixin, UpdateView):
    """Класс обновления информации"""
    model = CustomUser
    template_name = 'regabitur/add_info.html'
    form_class = AddInfoForm
    success_url = reverse_lazy('user_room_url')
    success_msg = 'Данные успешно обновлены'

    def get_context_data(self, **kwargs):
        """Переопределяем базовый метод, чтобы передать свой контекст"""
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].user:
            return self.handle_no_permission()
        return kwargs


"""
    Выбираем формы обучения 
"""


class AdditionalInfoView(LoginRequiredMixin, CreateView):
    """Класс для выбора профиля обучения"""
    model = AdditionalInfo
    template_name = 'regabitur/add_profile.html'
    form_class = AdditionalInfoForm
    success_url = reverse_lazy('user_room_url')

    def form_valid(self, form):
        """Метод сохранения записи за конкретным пользователем"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


"""
    CRUD для документов
"""


class DocumentsAddView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = DocumentUser
    template_name = 'regabitur/add_doc.html'
    form_class = AddDocForm
    success_url = reverse_lazy('add_doc_url')
    success_msg = 'Документ успешно добавлен!'

    def get_context_data(self, **kwargs):
        """Переопределяем базовый метод, чтобы передать свой контекст"""
        context = super().get_context_data(**kwargs)
        id_user = self.request.user
        user = CustomUser.objects.get(user=id_user)
        document_user = DocumentUser.objects.filter(user=id_user)
        user_doc_done = user.complete_flag
        context['user_doc_done'] = user_doc_done
        context['document_user'] = document_user
        context['custom_exist'] = hasattr(id_user, 'custom')
        context['addition_exist'] = hasattr(id_user, 'addition')
        return context

    def form_valid(self, form):
        """Метод сохранения записи за конкретным пользователем"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления документов из таблиц"""
    model = DocumentUser
    template_name = 'regabitur/add_doc.html'
    success_url = reverse_lazy('add_doc_url')
    success_msg = 'Запись удалена'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        """Переопределяем метод удаления, чтобы запретить удалять чужие записи"""
        # получаем запись объекта из бд
        self.object = self.get_object()
        if self.request.user != self.object.user:
            return self.handle_no_permission()

        success_url = self.get_success_url()

        self.object.delete()
        return HttpResponseRedirect(success_url)


class DocumentsListView(LoginRequiredMixin, ListView):
    """Класс для отображения таблицы с документами пользователей"""
    model = DocumentUser
    template_name = 'regabitur/add_doc.html'
    context_object_name = 'documents'


"""
     Классы регистрации и авторизации пользователей
"""


class MyLoginView(LoginView):
    """обработчик авторизации"""
    template_name = 'regabitur/login_abitur.html'
    form_class = MyLoginForm

    # success_url = reverse_lazy('user_room_url')

    def get_success_url(self):
        """
        Определяем, есть ли связанные модели для дополнительной информации(CustomUser, AdditionalUser)|
        Если нет, отправляем на страницу с добавлением недостающей информации
        """
        user = self.request.user
        custom_exist = hasattr(user, 'custom')
        addition_exist = hasattr(user, 'addition')
        if custom_exist and addition_exist:
            self.success_url = reverse_lazy('user_room_url')
        elif custom_exist:
            self.success_url = reverse_lazy('add_additional_url')
        else:
            self.success_url = reverse_lazy('add_info_url')
        return self.success_url


class MyRegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    template_name = 'regabitur/register_abitur.html'
    form_class = MyRegisterForm
    success_url = reverse_lazy('add_info_url')

    def form_valid(self, form):
        """если пользователь зарегистрировался, сразу входим в систему"""
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class MyLogoutView(LogoutView):
    """ВЫход из системы """
    next_page = reverse_lazy('reg_info_url')


"""
    Списки подавших документы
"""

"""
    Бакалавриат
"""


class BacSubmitListMixin(ListView):
    """
    Миксин для списка подавших документы (БАК, СПЕЦ)
    in:
        filter_name  - название профиля, по которому фильтруем записи из базы
        profile_name  -  название профиля для html
        form_ed  -  название формы обучения для html
        test_type  -  тип вступительных испытаний для html
        type_ed  -  бак/маг/асп для html
    """
    model = PublishTab
    template_name = 'regabitur/submit/submit_list_bak.html'
    filter_name = None
    profile_name = None
    form_ed = None
    test_type = None
    test_type_EGE = None
    test_type_Vstup = None
    type_ed = None

    def get_context_data(self, **kwargs):
        """Передаем записи с фильтром по профилю и вступительным испытаниям """
        context = super().get_context_data(**kwargs)
        all_publish = PublishTab.objects.filter(
            Q(**{self.filter_name: True}) & (Q(test_type=self.test_type_EGE) | Q(test_type=self.test_type_Vstup))
        )
        context["list"] = all_publish
        context["form_ed"] = self.form_ed
        context["profile_name"] = self.profile_name
        context["test_type"] = self.test_type
        context["test_type_Vstup"] = self.test_type_Vstup
        context["test_type_EGE"] = self.test_type_EGE
        context["type_ed"] = self.type_ed
        return context

class BacOfoGp(BacSubmitListMixin):
    """БАК ОФО ГП"""
    filter_name = "bak_ofo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Очная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Бакалавриат"
    # model = PublishTab
    # template_name = 'regabitur/submit/bak_ofo_gp.html'
    #
    # def get_context_data(self, **kwargs):
    #     """Передаем записи с БАК ОФО true"""
    #     context = super().get_context_data(**kwargs)
    #     all_publish = PublishTab.objects.filter(bak_ofo_gp=True)
    #     context["list"] = all_publish
    #     return context


class BacOfoUp(BacSubmitListMixin):
    """БАК ОФО УП"""
    filter_name = "bak_ofo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Очная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Бакалавриат"
    # model = PublishTab
    # template_name = 'regabitur/submit/bak_ofo_up.html'
    #
    # def get_context_data(self, **kwargs):
    #     """Передаем записи с БАК ОФО true """
    #     context = super().get_context_data(**kwargs)
    #     all_publish = PublishTab.objects.filter(bak_ofo_up=True)
    #     context["list"] = all_publish
    #     return context


class BacZfoGp(BacSubmitListMixin):
    """БАК ЗФО ГП"""
    filter_name = "bak_zfo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Заочная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Бакалавриат"


class BacZfoUp(BacSubmitListMixin):
    """БАК ЗФО УП"""
    filter_name = "bak_zfo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Заочная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Бакалавриат"


class BacOzfoGp(BacSubmitListMixin):
    """БАК ОЗФО ГП"""
    filter_name = "bak_ozfo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Очно-Заочная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Бакалавриат"


class BacOzfoUp(BacSubmitListMixin):
    """БАК ОЗФО УП"""
    filter_name = "bak_ozfo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Очно-Заочная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Бакалавриат"


"""
    Специалитет
"""


class SpecOfoSd(BacSubmitListMixin):
    """СПЕЦ ОФО СД"""
    filter_name = "spec_ofo_sd"
    profile_name = "Судебная деятельность"
    form_ed = "Очная"
    test_type_EGE = "ЕГЭ"
    test_type_Vstup = 'Вступительные испытания'
    type_ed = "Специалитет"


"""
    Магистратура
"""


class MagAspSubmitListMixin(ListView):
    """
    Миксин для списка подавших документы (МАГ, АСП)
    in:
        filter_name  - название профиля, по которому фильтруем записи из базы
        profile_name  -  название профиля для html
        form_ed  -  название формы обучения для html
        test_type  -  тип вступительных испытаний для html
        type_ed  -  бак/маг/асп для html
    """
    model = PublishTab
    template_name = 'regabitur/submit/submit_list_mag_asp.html'
    filter_name = None
    profile_name = None
    form_ed = None
    test_type = None
    type_ed = None

    def get_context_data(self, **kwargs):
        """Передаем записи с фильтром по профилю и вступительным испытаниям """
        context = super().get_context_data(**kwargs)
        all_publish = PublishTab.objects.filter(
            Q(**{self.filter_name: True})
        )
        context["list"] = all_publish
        context["form_ed"] = self.form_ed
        context["profile_name"] = self.profile_name
        context["test_type"] = self.test_type
        context["type_ed"] = self.type_ed
        return context

class MagOfoPo(MagAspSubmitListMixin):
    """Маг ОФО По"""
    filter_name = "mag_ofo_po"
    profile_name = "Правовое обеспечение гражданского оборота и предпринимательства"
    form_ed = "Очная"
    test_type = 'Вступительные испытания'
    type_ed = "Магистратура"
    # model = PublishTab
    # template_name = 'regabitur/submit/mag_ofo_po.html'
    #
    # def get_context_data(self, **kwargs):
    #     """Передаем записи с БАК ОФО true """
    #     context = super().get_context_data(**kwargs)
    #     all_publish = PublishTab.objects.filter(mag_ofo_po=True)
    #     context["list"] = all_publish
    #     return context


class MagZfoPo(MagAspSubmitListMixin):
    """Маг ZФО По"""
    filter_name = "mag_zfo_po"
    profile_name = "Правовое обеспечение гражданского оборота и предпринимательства"
    form_ed = "Заочная"
    test_type = 'Вступительные испытания'
    type_ed = "Магистратура"


class MagOfoTp(MagAspSubmitListMixin):
    """Маг OФО TП"""
    filter_name = "mag_ofo_tp"
    profile_name = "Теория и практика применения законодательства в уголовно-правовой сфере"
    form_ed = "Очная"
    test_type = 'Вступительные испытания'
    type_ed = "Магистратура"


class MagZfoTp(MagAspSubmitListMixin):
    """Маг ZФО TП"""
    filter_name = "mag_zfo_tp"
    profile_name = "Теория и практика применения законодательства в уголовно-правовой сфере"
    form_ed = "Заочная"
    test_type = 'Вступительные испытания'
    type_ed = "Магистратура"


"""
    Аспирантура
"""


class AspOfoTip(MagAspSubmitListMixin):
    """Асп ОФО Тип"""
    filter_name = "asp_ofo_tip"
    profile_name = "Теория и история права и государства, история учений о праве и государстве"
    form_ed = "Очная"
    test_type = 'Вступительные испытания'
    type_ed = "Аспирантура"


class AspZfoTip(MagAspSubmitListMixin):
    """Асп ЗФО Тип"""
    filter_name = "asp_zfo_tip"
    profile_name = "Теория и история права и государства, история учений о праве и государстве"
    form_ed = "Заочная"
    test_type = 'Вступительные испытания'
    type_ed = "Аспирантура"


class AspOfoUp(MagAspSubmitListMixin):
    """Асп ОФО УП"""
    filter_name = "asp_ofo_up"
    profile_name = "Уголовный процесс"
    form_ed = "Очная"
    test_type = 'Вступительные и спытания'
    type_ed = "Аспирантура"


class AspZfoUp(MagAspSubmitListMixin):
    """Асп ЗФО УП"""
    filter_name = "asp_zfo_up"
    profile_name = "Уголовный процесс"
    form_ed = "Заочная"
    test_type = 'Вступительные испытания'
    type_ed = "Аспирантура"


class AspOfoKs(MagAspSubmitListMixin):
    """Асп ОФО КС"""
    filter_name = "asp_ofo_ks"
    profile_name = "Криминалистика; судебно-экспертная деятельность; оперативно-розыскная деятельность"
    form_ed = "Очная"
    test_type = 'Вступительные испытания'
    type_ed = "Аспирантура"


class AspZfoKs(MagAspSubmitListMixin):
    """Асп ЗФО КС"""
    filter_name = "asp_zfo_ks"
    profile_name = "Криминалистика; судебно-экспертная деятельность; оперативно-розыскная деятельность"
    form_ed = "Заочная"
    test_type = 'Вступительные испытания'
    type_ed = "Аспирантура"


"""
    Рекомендованные к зачислению 
"""

"""
    Бакалавриат / Специалитет
"""


class BakRecListMixin(ListView):
    """
    Миксин для списка рекомендованных к зачислению (БАК, СПЕЦ)
    in:
        filter_name  - название профиля, по которому фильтруем записи из базы
        profile_name  -  название профиля для html
        form_ed  -  название формы обучения для html
        test_type  -  тип вступительных испытаний для html
        type_ed  -  бак/маг/асп для html
    """
    model = PublishRecTab
    template_name = 'regabitur/rec/rec_list_bak.html'
    column_table_name = None
    filter_name = None
    profile_name = None
    form_ed = None
    test_type = None
    type_ed = None

    def get_context_data(self, **kwargs):
        """Передаем записи с фильтром по профилю и вступительным испытаниям """
        context = super().get_context_data(**kwargs)
        all_publish = PublishRecTab.objects.filter(
            Q(**{self.filter_name: True}) & Q(test_type=self.test_type)
        )
        context["list"] = all_publish
        context["column_name"] = self.column_table_name
        context["form_ed"] = self.form_ed
        context["profile_name"] = self.profile_name
        context["test_type"] = self.test_type
        context["type_ed"] = self.type_ed
        return context

# -- БАК ОФО --


class BakRecOfoGp(BakRecListMixin):
    """БАК ОФО ГП ЕГЭ """
    column_table_name = "История/Иностранный язык"
    filter_name = "bak_ofo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Очная"
    test_type = "ЕГЭ"
    type_ed = "Бакалавриат"


class BakRecOfoGpVstup(BakRecListMixin):
    """БАК ОФО ГП Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "bak_ofo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Бакалавриат"


class BakRecOfoUp(BakRecListMixin):
    """БАК ОФО УП ЕГЭ """
    column_table_name = "История/Иностранный язык"
    filter_name = "bak_ofo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Очная"
    test_type = "ЕГЭ"
    type_ed = "Бакалавриат"


class BakRecOfoUpVstup(BakRecListMixin):
    """БАК ОФО УП Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "bak_ofo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Бакалавриат"


# -- БАК ЗФО --


class BakRecZfoGp(BakRecListMixin):
    """БАК ЗФО ГП ЕГЭ """
    column_table_name = "История/Иностранный язык"
    filter_name = "bak_zfo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Заочная"
    test_type = "ЕГЭ"
    type_ed = "Бакалавриат"


class BakRecZfoGpVstup(BakRecListMixin):
    """БАК ЗФО ГП Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "bak_zfo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Бакалавриат"


class BakRecZfoUp(BakRecListMixin):
    """БАК ЗФО УП ЕГЭ """
    column_table_name = "История/Иностранный язык"
    filter_name = "bak_zfo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Заочная"
    test_type = "ЕГЭ"
    type_ed = "Бакалавриат"


class BakRecZfoUpVstup(BakRecListMixin):
    """БАК ЗФО УП Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "bak_zfo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Бакалавриат"

# -- БАК ОЗФО --


class BakRecOzfoGp(BakRecListMixin):
    """БАК ОЗФО ГП ЕГЭ """
    column_table_name = "История/Иностранный язык"
    filter_name = "bak_ozfo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Очно-заочная"
    test_type = "ЕГЭ"
    type_ed = "Бакалавриат"


class BakRecOzfoGpVstup(BakRecListMixin):
    """БАК ОЗФО ГП Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "bak_ozfo_gp"
    profile_name = "Гражданско правовой"
    form_ed = "Очно-заочная"
    test_type = "Вступительные испытания"
    type_ed = "Бакалавриат"


class BakRecOzfoUp(BakRecListMixin):
    """БАК ОЗФО УП ЕГЭ """
    column_table_name = "История/Иностранный язык"
    filter_name = "bak_ozfo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Очно-заочная"
    test_type = "ЕГЭ"
    type_ed = "Бакалавриат"


class BakRecOzfoUpVstup(BakRecListMixin):
    """БАК ОЗФО УП Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "bak_ozfo_up"
    profile_name = "Уголовно правовой"
    form_ed = "Очно-заочная"
    test_type = "Вступительные испытания"
    type_ed = "Бакалавриат"


# -- СПЕЦ ОФО --

class SpecRecOfoSd(BakRecListMixin):
    """ СПЕЦ ОФО СД Вступительные """
    column_table_name = "История/Иностранный язык"
    filter_name = "spec_ofo_sd"
    profile_name = "Судебная и прокурорская деятельность"
    form_ed = "Очная"
    test_type = "ЕГЭ"
    type_ed = "Специалитет"


class SpecRecOfoSdVstup(BakRecListMixin):
    """ СПЕЦ ОФО СД Вступительные """
    column_table_name = "История/ТГП/ОКП"
    filter_name = "spec_ofo_sd"
    profile_name = "Судебная и прокурорская деятельность"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Специалитет"


"""
    Рекомендованные к зачислению 
"""

"""
    Магистратура / Аспирантура 
"""


class MagRecListMixin(ListView):
    """
    Миксин для списка рекомендованных к зачислению (Маг / Асп)
    in:
        column_table_name  -  имя столбца в таблице (для разных вступительных)
        column_table_name_option  -  имя столбца в таблице для предмета по выбору (для разных вступительных)
        filter_name  - название профиля, по которому фильтруем записи из БД
        profile_name  -  название профиля для html
        form_ed  -  название формы обучения для html
        test_type  -  тип вступительных испытаний для html и для фильтра БД
        type_ed  -  бак/маг/асп для html
    """
    model = PublishRecTab
    template_name = 'regabitur/rec/rec_list_mag_asp.html'
    column_table_name = None
    column_table_name_option = None
    filter_name = None
    profile_name = None
    form_ed = None
    test_type = None
    type_ed = None

    def get_context_data(self, **kwargs):
        """Передаем записи с БАК ОФО true """
        context = super().get_context_data(**kwargs)
        all_publish = PublishRecTab.objects.filter(
            Q(**{self.filter_name: True})
        )
        context["list"] = all_publish
        context["column_name"] = self.column_table_name
        context["column_name_option"] = self.column_table_name_option
        context["form_ed"] = self.form_ed
        context["profile_name"] = self.profile_name
        context["test_type"] = self.test_type
        context["type_ed"] = self.type_ed
        return context

# -- МАГ ОФО --


class MagRecOfoPoVstup(MagRecListMixin):
    """МАГ ОФО ПО Вступительные """
    column_table_name = "Конституционное право"
    column_table_name_option = "Гражданское право / Уголовное право"
    filter_name = "mag_ofo_po"
    profile_name = "Правовое обеспечение гражданского оборота и предпринимательства"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Магистратура"


class MagRecOfoTpVstup(MagRecListMixin):
    """МАГ ОФО ТП Вступительные """
    column_table_name = "Конституционное право"
    column_table_name_option = "Гражданское право / Уголовное право"
    filter_name = "mag_ofo_tp"
    profile_name = "Теория и практика применения законодательства в уголовно-правовой сфере"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Магистратура"

# -- МАГ ЗФО --


class MagRecZfoPoVstup(MagRecListMixin):
    """МАГ ЗФО ПО Вступительные """
    column_table_name = "Конституционное право"
    column_table_name_option = "Гражданское право / Уголовное право"
    filter_name = "mag_zfo_po"
    profile_name = "Правовое обеспечение гражданского оборота и предпринимательства"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Магистратура"


class MagRecZfoTpVstup(MagRecListMixin):
    """МАГ ЗФО ТП Вступительные """
    column_table_name = "Конституционное право"
    column_table_name_option = "Гражданское право / Уголовное право"
    filter_name = "mag_zfo_tp"
    profile_name = "Теория и практика применения законодательства в уголовно-правовой сфере"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Магистратура"

# -- АСП ОФО --


class AspRecOfoTipVstup(MagRecListMixin):
    """АСП ОФО ТИП Вступительные """
    column_table_name = "Иностранный язык"
    column_table_name_option = "Специальная дисциплина"
    filter_name = "asp_ofo_tip"
    profile_name = "Теория и история права и государства, история учений о праве и государстве"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Аспирантура"


class AspRecOfoUpVstup(MagRecListMixin):
    """АСП ОФО УП Вступительные """
    column_table_name = "Иностранный язык"
    column_table_name_option = "Специальная дисциплина"
    filter_name = "asp_ofo_up"
    profile_name = "Уголовный процесс"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Аспирантура"


class AspRecOfoKsVstup(MagRecListMixin):
    """АСП ОФО КС Вступительные """
    column_table_name = "Иностранный язык"
    column_table_name_option = "Специальная дисциплина"
    filter_name = "asp_ofo_ks"
    profile_name = "Криминалистика; судебно-экспертная деятельность; оперативно-розыскная деятельность"
    form_ed = "Очная"
    test_type = "Вступительные испытания"
    type_ed = "Аспирантура"

# -- АСП ЗФО --


class AspRecZfoTipVstup(MagRecListMixin):
    """АСП ЗФО ТИП Вступительные """
    column_table_name = "Иностранный язык"
    column_table_name_option = "Специальная дисциплина"
    filter_name = "asp_zfo_tip"
    profile_name = "Теория и история права и государства, история учений о праве и государстве"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Аспирантура"


class AspRecZfoUpVstup(MagRecListMixin):
    """АСП ЗФО УП Вступительные """
    column_table_name = "Иностранный язык"
    column_table_name_option = "Специальная дисциплина"
    filter_name = "asp_zfo_up"
    profile_name = "Уголовный процесс"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Аспирантура"


class AspRecZfoKsVstup(MagRecListMixin):
    """АСП ЗФО КС Вступительные """
    column_table_name = "Иностранный язык"
    column_table_name_option = "Специальная дисциплина"
    filter_name = "asp_zfo_ks"
    profile_name = "Криминалистика; судебно-экспертная деятельность; оперативно-розыскная деятельность"
    form_ed = "Заочная"
    test_type = "Вступительные испытания"
    type_ed = "Аспирантура"