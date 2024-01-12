import re
import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .credentials import TELEGRAM_API_URL, URL
from instatoyt.views import ReelViewSet

@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    update = json.loads(request.body.decode('utf-8'))
    print(update)
    handle_update(update)
    return HttpResponse('ok')
  else:
    return HttpResponseBadRequest('Bad Request')

def send_message(method, data):
  return requests.post(TELEGRAM_API_URL + method, data)

def handle_update(update):
  if 'message' not in update:
    print('message is not present')
    return
  chat_id = update['message']['chat']['id']
  text = update['message']['text']

  # Define a regular expression pattern to match the reel ID
  pattern = r"/reel/([^/?]+)"
  # Use re.search to find the match
  match = re.search(pattern, text)

  if match:
    reel_id = match.group(1)
    print("Reel ID:", reel_id)
    send_message("sendMessage", {
      'chat_id': chat_id,
      'text': f'Instagram reel detected {reel_id}. Uploading to YT$'
    })
    response = call_yt_upload_api(reel_id)
    print(f"response: {response}")

    if response["successful"]:
      send_message("sendMessage", {
        'chat_id': chat_id,
        'text': f'Reel uploaded successfully ✅'
      })
    else:
      send_message("sendMessage", {
        'chat_id': chat_id,
        'text': f'The Reel failed to upload ⚠️'
      })


  else:
    print("Reel ID not found in the URL.")
    send_message("sendMessage", {
      'chat_id': chat_id,
      'text': f'This is not a instagram reel link'
    })

def setwebhook(request):
  response = requests.post(TELEGRAM_API_URL+ "setWebhook?url=" + URL + "/telegrambot/getpost/").json()
  return HttpResponse(f"{response}")

def call_yt_upload_api(reel_id):
  # Implement the logic to call the other API using the reel_id
  other_api_url = URL + '/api/reel/'
  payload = {'reel_id': reel_id}

  response = requests.post(other_api_url, json=payload)
  print(f"response: {response}")

  # Check the response status and handle accordingly
  if response.status_code == 201:
      return {"successful":True}
  else:
      return {"successful": False}