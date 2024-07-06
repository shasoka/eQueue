import requests

response = requests.get("https://edu.sfu-kras.ru/api/timetable/get_insts")
response.raise_for_status()
result = response.json()


def process_groups(data):
    unique_groups = []
    for group in data:
        # Избавляемся от подгрупп в имени группы
        base_name = group['name'].split(' (')[0]
        if base_name not in unique_groups:
            unique_groups.append(base_name)
    return [{'name': group} for group in unique_groups]


groups_data = process_groups(result)

for g in groups_data:
    print(g)
