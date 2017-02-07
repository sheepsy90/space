from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    ### Registration & Login ###

    url(r'^$', lambda x: HttpResponseRedirect('index/')),
    url(r'^index', 'core.controller.login.login_controller.index'),
    url(r'^view_registration_page', 'core.controller.registration.registration_controller.view_registration_page'),
    url(r'^logout', 'core.controller.login.login_controller.logoutpage'),
    url(r'^ajax/login_user', 'core.controller.login.login_controller.login_user'),
    url(r'^ajax/send_registration', 'core.controller.registration.registration_controller.send_registration'),


    ### Mission Mappings ###

    url(r'^planet', 'core.controller.mission.mission_controller.view_planet'),
    url(r'poll_available_missions/$', 'core.controller.mission.mission_controller.poll_available_missions'),
    url(r'^prepare_mission/(?P<mission_id>\d+)/$', 'core.controller.mission.mission_controller.prepare_mission'),
    url(r'^current_mission/$', 'core.controller.mission.mission_controller.current_mission'),
    url(r'^leave_mission/$', 'core.controller.mission.mission_controller.leave_mission'),
    url(r'^join_mission/(?P<mission_instance_id>\d+)/$', 'core.controller.mission.mission_controller.join_mission'),
    url(r'^start_mission/$', 'core.controller.mission.mission_controller.start_mission'),
    url(r'^poll_events/$', 'core.controller.mission.mission_controller.poll_events'),
    url(r'^complete_mission/$', 'core.controller.mission.mission_controller.complete_mission'),
    url(r'^handle_event/(?P<event_id>\d+)/$', 'core.controller.mission.mission_controller.handle_event'),
    url(r'^poll_party_members/$', 'core.controller.mission.mission_controller.poll_party_members'),


    ### Academy Mappings ###

    url(r'^academy', 'core.controller.academy.academy_controller.view_academy'),
    url(r'^can_join_program/$', 'core.controller.academy.academy_controller.can_join_program'),
    url(r'^answer_question/$', 'core.controller.academy.academy_controller.answer_question'),
    url(r'^ongoing_program/$', 'core.controller.academy.academy_controller.ongoing_program'),
    url(r'^finish_tutorial/$', 'core.controller.academy.academy_controller.finish_tutorial'),
    url(r'^enter_program/(?P<program_id>\d+)/$', 'core.controller.academy.academy_controller.enter_program'),


    ### Tutorial ###

    url(r'^tutorial/$', 'core.controller.tutorial.tutorial_controller.view_tutorial_page'),
    url(r'^choose_academy_program_in_tutorial/$', 'core.controller.tutorial.tutorial_controller.choose_academy_program_in_tutorial'),
    url(r'^tutorial_confirm/$', 'core.controller.tutorial.tutorial_controller.confirm_tutorial_science_letter'),

    ### Imprint ###
    url(r'^imprint/$', 'core.controller.views.view_imprint'),

    ### Information ###

    url(r'^information/$', 'core.controller.information.information_controller.view_information'),

    ### Settings ###

    url(r'^settings/$', 'core.controller.settings.settings_controller.view_settings'),
    url(r'^switch_sound_setting_state/$', 'core.controller.settings.settings_controller.switch_sound_setting_state'),

    ### Admin Site ###

    url(r'^admin/', include(admin.site.urls)),

    ### Catch All ###

    url(r'^(?P<url>.*)/$', 'core.controller.views.catch_all'),
)
