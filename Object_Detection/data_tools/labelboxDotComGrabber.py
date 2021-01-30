# AUTHOR: Morgan Visnesky
# DATE: 01/10/2021
# FILENAME: labelboxDotComGrabber.py
#
# DESCRIPTION:
# Grabs labels from labelbox.com account


import requests
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJja2l4aHc0eW80czJwMDczNDZ1eWY0eDk4Iiwib3JnYW5pemF0aW9uSWQiOiJja2l4aHc0eTcycmJhMDc0MXFuN2xrOTZwIiwiYXBpS2V5SWQiOiJja2pyeTdlcXAwY3VkMDcyNng5YzZ6ejZpIiwiaWF0IjoxNjEwMzMyMTg1LCJleHAiOjIyNDE0ODQxODV9.VnvvoZfeSGQAdJ0n5_q-D2nAh2-qDZeq38LiYge3nVg"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJja2pzd3lueHdyMmZnMDc0MW5paXgwczI4Iiwib3JnYW5pemF0aW9uSWQiOiJja2l4aHc0eTcycmJhMDc0MXFuN2xrOTZwIiwiYXBpS2V5SWQiOiJja2tjM3lqaGpoZ2k3MDcxMjRxbm14OG41IiwiaWF0IjoxNjExNTUxMTczLCJleHAiOjIyNDI3MDMxNzN9.Nr6TttbVrYLC-aZ3gDuQCgD9GtCw5gcEAk995wwTfJI"
frames_url = "https://api.labelbox.com/v1/frames/ckkbp11mg00033c5m9hssn1qi"

headers = {'Authorization': "Bearer " + API_KEY}

# pulls frame annotations from labelbox API
data_response = requests.get(frames_url, headers=headers)

# separates into individual lines
x = data_response.iter_lines()

# writes dataset to .txt file
with open('sebastian_dataset.txt', 'w') as the_file:
    for i in x:
        the_file.write(str(i) + '\n')
