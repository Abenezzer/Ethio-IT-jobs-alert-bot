import requests



def send_jobs_alers(BOT_TOKEN:str, chat_id:str, title:str, link:str):

    url = url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"Job Title:{title}, Link: {link}"
    payload = {
        "chat_id": chat_id,
        "text": message,
       
    }
    response = requests.post(url=url, data=payload, timeout=15)
    response.raise_for_status()
    print(response.json())


send_jobs_alers('9107666693:AAEzXBnYQy2AqGZp4n4NCTJjnETjyV6kUfE','672196988', "Cyber Security", 'abenezzer.github.io' )