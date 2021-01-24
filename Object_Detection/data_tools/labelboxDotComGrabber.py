# AUTHOR: Morgan Visnesky
# DATE: 01/10/2021
# FILENAME: labelboxDotComGrabber.py
#
# DESCRIPTION:
#
# Grabs labels from labelbox.com account


import requests

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJja2l4aHc0eW80czJwMDczNDZ1eWY0eDk4Iiwib3JnYW5pemF0aW9uSWQiOiJja2l4aHc0eTcycmJhMDc0MXFuN2xrOTZwIiwiYXBpS2V5SWQiOiJja2pyeTdlcXAwY3VkMDcyNng5YzZ6ejZpIiwiaWF0IjoxNjEwMzMyMTg1LCJleHAiOjIyNDE0ODQxODV9.VnvvoZfeSGQAdJ0n5_q-D2nAh2-qDZeq38LiYge3nVg"
frames_url = "https://api.labelbox.com/v1/frames/ckjqwwb9300053a6825dtlq8w"

headers = {'Authorization': "Bearer " + API_KEY}
data_response = requests.get(frames_url, headers=headers)

x = data_response.iter_lines()

for i in x:
    print(i)
