import requests
import json
import os

folder = "E:\\Tunz\\Python\\SlidePyNC"
file = "raw_data_visualize.json"
data = None
with open(os.path.join(folder,file),'r') as f:
    data = json.load(f)
    print("Load sucessful")
print(len(data))
url = "https://www.topuniversities.com/rankings/endpoint?nid=4061771&page=50&items_per_page=30&tab=indicators&region=&countries=&cities=&search=&star=&sort_by=&order_by=&program_type=&scholarship=&fee=&english_score=&academic_score=&mix_student=&loggedincache=7047458-1762402016123"

response = requests.get(url)
if response.status_code == 200:
    try:
        raw_data = response.json()
        score_node = raw_data["score_nodes"]
        # print(score_node)
        for node in score_node:
            university = {
                "score_nid" : node["score_nid"],
                "nid" : node["nid"],
                "core_id" : node["core_id"],
                "title" : node['title'],
                "path" : node["path"],
                "region" : node['region'],
                "country" : node["country"],
                "city" : node["city"],
                'logo' : node['logo'],
                "overall_score" : node["overall_score"],
                "rank_display" : node["rank_display"],
                "rank" : node['rank'],
                'more_info' : node['more_info'],
                'scores' : node['scores']
            }
            # print(node['path'])
            data.append(university)
        if len(data):
            with open(os.path.join(folder,file),'w') as f:
                json.dump(data,f,indent=4)
                print("Dumps sucessful")
    except:
        print("not json")
else:
    print("Loi request")
