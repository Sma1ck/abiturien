from django.urls import re_path
from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='reg_info_url'),
    path('accounts/login/', MyLoginView.as_view(), name='login_abitur_url'),
    path('login/', MyLoginView.as_view(), name='login_abitur_url'),
    path('register-abitur/', MyRegisterView.as_view(), name='register_abitur_url'),
    path('logout-abitur', MyLogoutView.as_view(), name='logout_abitur_url'),
    path(r'^password-reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    path(r'^password-reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',  views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path(r'^password-reset/complete/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('add_dok', DocumentsAddView.as_view(), name='add_doc_url'),
    path('add_info', InfoCreateView.as_view(), name='add_info_url'),
    path('add_addition/', AdditionalInfoView.as_view(), name='add_additional_url'),
    path('user-room/', UserRoom.as_view(), name='user_room_url'),
    path('update_info/<int:pk>', InfoUpdateView.as_view(), name='update_info_url'),
    path('complete_send/<int:pk>', complete_send, name='complete_send_url'),
    path('agreement_flag/<int:pk>', agreement_flag, name='agreement_flag_url'),
    path('delete-page/<int:pk>', DocumentDeleteView.as_view(), name='delete_page_url'),
]

# пути для списков подавших документы
urlpatterns += [
    # БАК
    path('submit/bak_ofo_gp', BacOfoGp.as_view(), name='submit_bak_ofo_gp'),
    path('submit/bak_ofo_up', BacOfoUp.as_view(), name='submit_bak_ofo_up'),
    path('submit/bak_zfo_gp', BacZfoGp.as_view(), name='submit_bak_zfo_gp'),
    path('submit/bak_zfo_up', BacZfoUp.as_view(), name='submit_bak_zfo_up'),
    path('submit/bak_ozfo_gp', BacOzfoGp.as_view(), name='submit_bak_ozfo_gp'),
    path('submit/bak_ozfo_up', BacOzfoUp.as_view(), name='submit_bak_ozfo_up'),
    # СПЕЦ
    path('submit/spec_ofo_sd', SpecOfoSd.as_view(), name='submit_spec_ofo_sd'),
    # МАГ
    path('submit/mag_ofo_po', MagOfoPo.as_view(), name='submit_mag_ofo_po'),
    path('submit/mag_zfo_po', MagZfoPo.as_view(), name='submit_mag_zfo_po'),
    path('submit/mag_ofo_tp', MagOfoTp.as_view(), name='submit_mag_ofo_tp'),
    path('submit/mag_zfo_tp', MagZfoTp.as_view(), name='submit_mag_zfo_tp'),
    # АСП
    path('submit/asp_ofo_tip', AspOfoTip.as_view(), name='submit_asp_ofo_tip'),
    path('submit/asp_zfo_tip', AspZfoTip.as_view(), name='submit_asp_zfo_tip'),
    path('submit/asp_ofo_up', AspOfoUp.as_view(), name='submit_asp_ofo_up'),
    path('submit/asp_zfo_up', AspZfoUp.as_view(), name='submit_asp_zfo_up'),
    path('submit/asp_ofo_ks', AspOfoKs.as_view(), name='submit_asp_ofo_ks'),
    path('submit/asp_zfo_ks', AspZfoKs.as_view(), name='submit_asp_zfo_ks'),
]

# пути для рекомендованных к зачислению
urlpatterns += [
    # Бак
    path('rec/rec_bak_ofo_gp', BakRecOfoGp.as_view(), name='rec_bak_ofo_gp'),
    path('rec/rec_bak_ofo_gp_vstupit', BakRecOfoGpVstup.as_view(), name='rec_bak_ofo_gp_vstupit'),
    path('rec/rec_bak_ofo_up', BakRecOfoUp.as_view(), name='rec_bak_ofo_up'),
    path('rec/rec_bak_ofo_up_vstupit', BakRecOfoUpVstup.as_view(), name='rec_bak_ofo_up_vstupit'),
    path('rec/rec_bak_zfo_gp', BakRecZfoGp.as_view(), name='rec_bak_zfo_gp'),
    path('rec/rec_bak_zfo_gp_vstupit', BakRecZfoGpVstup.as_view(), name='rec_bak_zfo_gp_vstupit'),
    path('rec/rec_bak_zfo_up', BakRecZfoUp.as_view(), name='rec_bak_zfo_up'),
    path('rec/rec_bak_zfo_up_vstupit', BakRecZfoUpVstup.as_view(), name='rec_bak_zfo_up_vstupit'),
    path('rec/rec_bak_ozfo_gp', BakRecOzfoGp.as_view(), name='rec_bak_ozfo_gp'),
    path('rec/rec_bak_ozfo_gp_vstupit', BakRecOzfoGpVstup.as_view(), name='rec_bak_ozfo_gp_vstupit'),
    path('rec/rec_bak_ozfo_up', BakRecOzfoUp.as_view(), name='rec_bak_ozfo_up'),
    path('rec/rec_bak_ozfo_up_vstupit', BakRecOzfoUpVstup.as_view(), name='rec_bak_ozfo_up_vstupit'),
    # Спец
    path('rec/rec_spec_ofo_sd', SpecRecOfoSd.as_view(), name='rec_spec_ofo_sd'),
    path('rec/rec_spec_ofo_sd_vstupit', SpecRecOfoSdVstup.as_view(), name='rec_spec_ofo_sd_vstupit'),
    # Маг
    path('rec/rec_mag_ofo_po_vstupit', MagRecOfoPoVstup.as_view(), name='rec_mag_ofo_po_vstupit'),
    path('rec/rec_mag_ofo_tp_vstupit', MagRecOfoTpVstup.as_view(), name='rec_mag_ofo_tp_vstupit'),
    path('rec/rec_mag_zfo_po_vstupit', MagRecZfoPoVstup.as_view(), name='rec_mag_zfo_po_vstupit'),
    path('rec/rec_mag_zfo_tp_vstupit', MagRecZfoTpVstup.as_view(), name='rec_mag_zfo_tp_vstupit'),
    # Асп
    path('rec/rec_asp_ofo_tip_vstupit', AspRecOfoTipVstup.as_view(), name='rec_asp_ofo_tip_vstupit'),
    path('rec/rec_asp_ofo_up_vstupit', AspRecOfoUpVstup.as_view(), name='rec_asp_ofo_up_vstupit'),
    path('rec/rec_asp_ofo_ks_vstupit', AspRecOfoKsVstup.as_view(), name='rec_asp_ofo_ks_vstupit'),
    path('rec/rec_asp_zfo_tip_vstupit', AspRecZfoTipVstup.as_view(), name='rec_asp_zfo_tip_vstupit'),
    path('rec/rec_asp_zfo_up_vstupit', AspRecZfoUpVstup.as_view(), name='rec_asp_zfo_up_vstupit'),
    path('rec/rec_asp_zfo_ks_vstupit', AspRecZfoKsVstup.as_view(), name='rec_asp_zfo_ks_vstupit'),
]
