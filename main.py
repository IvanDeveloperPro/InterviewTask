from datetime import timedelta, datetime
import re

from dummy_server.server import get_random_request


weekend = {
        6: 'Saturday: 6️⃣',
        7: 'Sunday: 7️⃣'
    }
types = {
    'text': 0,
    'image': 0,
    'video': 0,
    'sound': 0
}


def process_text(request):
    """
     In dependence of request either print emoji weekend
     or content of request

    :param request:
    :return: None
    """
    timestamp = request.get('ts')
    weekday = timestamp.isoweekday()
    if weekday in weekend:
        print(weekend[weekday])
    else:
        text = request.get('content').lower()
        new_text = set(re.sub(r' ,;:/#@\\"\'', ' ', text).split())
        print(len(new_text))


def process_image(request):
    filename = request.get('content').split('.')
    if filename[1].lower() == 'jpg':
        print(filename[0])
    else:
        timestamp = request.get('ts')
        delta = timedelta(hours=24)
        print(timestamp - delta)


def process_video(request):
    file_ext = request.get('content').split('.')[1]
    timestamp = request.get('ts')
    weekday = timestamp.isoweekday()
    if weekday in weekend:
        if len(file_ext) == 4:
            print('OK')
        else:
            print('REJECT')
    else:
        if len(file_ext) == 3:
            print('OK')
        else:
            print('REJECT')


def process_sound(request):
    content = request.get('content').replace('.', '')
    new_dict = {x: 0 for x in content}
    for s in content:
        new_dict[s] += 1
    not_uniq = True
    for k, v in new_dict.items():
        if v != 1:
            continue
        else:
            print(k)
            not_uniq = False
            return
    if not_uniq:
        print('None')


def is_older_date(request) -> bool:
    request_time = request.get('ts')
    delta = timedelta(days=4)
    c_date = datetime.now()
    date = (c_date - delta).date()
    return date > request_time.date()


def start_request(times: int) -> None:
    """
     this function is working as a router. The allocate requests on basis they data types
    :param times: amount requests
    :return: None
    """
    for i in range(times):
        request = get_random_request()
        req_type = request.get('req_type')
        types[req_type] += 1
        if req_type == 'text':
            process_text(request)
        elif req_type == 'image':
            if is_older_date(request):
                continue
            process_image(request)
        elif req_type == 'video':
            if is_older_date(request):
                continue
            process_video(request)
        elif req_type == 'sound':
            process_sound(request)
        else:
            print(f'You have sent unsupporting type of request + {req_type}')
        if i == times-1:
            for k, v in types.items():
                if v > 0:
                    print(f'{k}:{v}', end=" ")


if __name__ == "__main__":
    start_request(10)
