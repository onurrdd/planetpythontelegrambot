# -*- coding: utf8 -*-

import json
import logging

import telepot
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import parse_planetpy_rss

from django.http import HttpResponse

#TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

TOKEN = 'x' # you should add here telegram bot token
TelegramBot = telepot.Bot(TOKEN)
logger = logging.getLogger('telegram.bot')


def simple_get_view(request):
    return HttpResponse("GET isteği alındı!")


def _display_help():
    return render_to_string('help.md')


def _display_planetpy_feed():
    return render_to_string('feed.md', {'items': parse_planetpy_rss()})




class CommandReceiveView(View):

    def get(self, request, bot_token):
        print("onur 2")
        print("get isteği geldi")

    def post(self, request, bot_token):
        print("Onur")

        if bot_token != TOKEN:
            return HttpResponseForbidden('Invalid token'.encode('utf-8'))

        commands = {
            '/start': _display_help,
            'help': _display_help,
            'feed': _display_planetpy_feed,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)
        #ben ekliyorum:

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest(
                'Invalid request body'.encode('utf-8'))
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id,
                                        'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView,
                     self).dispatch(request, *args, **kwargs)
