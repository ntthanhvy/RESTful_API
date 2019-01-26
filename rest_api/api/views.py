from django.shortcuts import render

import requests
import json

# Create your views here.
base_url = 'https://od-api.oxforddictionaries.com/api/v1/'
app_id = '5f071143'
app_key = '1930dfaed67e53bb7ac7e1b2b1b68f63'
list_lang = ['en','es']
list_api = {'Entries': 'entries', 'Lemmatron': 'inflections'}


def home(request):
    template = 'api/home.html'

    return render(request, template, {
        'list_lang': list_lang,
        'api_list': list_api,
        })


def result(request):
    template = 'api/result.html'

    if request.method == 'POST':
        api = request.POST.get('api')
        content_type = request.POST.get('type')
        language = request.POST.get('language')
        word_id = request.POST.get('word_id')

        try:
            url = base_url + list_api[api] + '/' + language + '/' + word_id.lower()

            r = requests.get(url, headers={
                'app_id': app_id,
                'app_key': app_key,
                "Accept": 'applications/' + content_type,
            })

            with open('result.' + content_type, 'a+') as fileout:
                json.dump(getattr(r, content_type)(), fileout)
                fileout.write('\n\n')

            return render(request, template, {
                'list_lang': list_lang,
                'api_list': list_api,
                'request_url': url,
                'status_code': r.status_code,
                'response_type': content_type,
                'response_text': json.dumps(getattr(r, content_type)()),
                })
        except Exception as e:
            print(type(e), e)

            error_mess = e, r.text
            return render(request, 'api/home.html', {
                'list_lang': list_lang,
                'api_list': list_api,
                'error_mess': error_mess

            })