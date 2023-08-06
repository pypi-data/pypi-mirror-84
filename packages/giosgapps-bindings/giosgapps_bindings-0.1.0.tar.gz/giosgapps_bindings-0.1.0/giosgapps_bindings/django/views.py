from django.views import View
from django.http import HttpResponseBadRequest
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
from ..django.utils import GiosgappTriggerContext


class ApplicationTriggerView(View):
    """
    This module expects to find "GIOSG_APP_SECRET" variable in Django settings.
    ! PLEASE READ FOLLOWING:
    This is intended to be subclassed, and used via "on_<trigger-type>" methods.
    """
    http_method_names = ['get']

    def get(self, request):
        # Leave validation to GiosgappTriggerContext object
        try:
            trigger = GiosgappTriggerContext(request, settings.GIOSG_APP_SECRET)
            handler = getattr(self, 'on_'+trigger.type, self.__unsupported_trigger_type)
            if trigger.type == 'manual_dialog' or trigger.type == 'manual_nav':
                handler = xframe_options_exempt(handler)
            return handler(request, trigger)

        # Handle any giosg-auth-token validation errors
        except ValueError as e:
            return HttpResponseBadRequest(e)

    def __unsupported_trigger_type(self, *args, **kwargs):
        return HttpResponseBadRequest('Unsupported trigger type')

    def on_install(self, request, trigger_context):
        """
        Redirected here within same browser window from Giosg Settings -> Apps -> (Install)
        Expects HTTP-200 with HTML containing app-specific setup page (e.g. configuration form) here.
        Setup page should redirect user back to Giosg Settings using trigger.redirect_uri, after configuring complete.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse with setup page HTML
        """
        raise NotImplementedError

    def on_setup(self, request, trigger_context):
        """
        Redirected here in a new window from Giosg Settings -> Apps -> (Setup)
        Expects HTTP-200 with HTML containing pre-filled setup page (configured on on_install).
        Setup page does not need to redirect back since this is in a new window.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse with setup page HTML
        """
        raise NotImplementedError

    def on_uninstall(self, request, trigger_context):
        """
        Server-to-server request, an app has been uninstalled from an organization (trigger_context.org_id).
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse (empty)
        """
        raise NotImplementedError

    def on_chat_start(self, request, trigger_context):
        """
        A new chat has been created. Chat details in trigger_context param.
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse (empty)
        """
        raise NotImplementedError

    def on_chat_end(self, request, trigger_context):
        """
        A chat has ended. Chat details in trigger_context param.
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse (empty)
        """
        raise NotImplementedError

    def on_console_load(self, request, trigger_context):
        """
        An operator loaded Giosg Console.
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse (empty)
        """
        raise NotImplementedError

    def on_manual_dialog(self, request, trigger_context):
        """
        This App was clicked by operator from Giosg Console chat-sidebar.
        Expects HTTP-200 with HTML containing app-specific dialog, which will be inserted to 300(w) x 368(h) px iframe.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse
        """
        raise NotImplementedError

    def on_manual_nav(self, request, trigger_context):
        """
        This App was clicked by operator from Giosg Console navigation-bar.
        Expects HTTP-200 with HTML containing app-specific dialog, which will be inserted to 700(w) x 400(h) px iframe.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse
        """
        raise NotImplementedError

    def on_chat_open(self, request, trigger_context):
        """
        An operator opened a chat window in Giosg Console. AJAX call. Planned for deprecation in future.
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse
        """
        raise NotImplementedError

    def on_chat_close(self, request, trigger_context):
        """
        An operator closed a chat window in Giosg Console. AJAX call. Planned for deprecation in future.
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse
        """
        raise NotImplementedError

    def on_chat_focus(self, request, trigger_context):
        """
        An operator focused a chat window in Giosg Console. AJAX call. Planned for deprecation in future.
        Expects HTTP-200 to acknowledge event received.

        :param request: django.http.HttpRequest
        :param trigger_context: giosgapps_bindings.django.utils.GiosgappTriggerContext
        :return: django.http.HttpResponse
        """
        raise NotImplementedError
