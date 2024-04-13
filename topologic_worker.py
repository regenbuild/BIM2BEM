from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from specklepy.transports.server import ServerTransport
from specklepy.api.wrapper import StreamWrapper
from specklepy.api import operations
from specklepy.objects.geometry import Mesh, Point, Polyline

# from topologicpy.Topology import Topology
# from topologicpy.Speckle import Speckle

# HOST = "https://app.speckle.systems/"

# Rhino = {"STREAM_ID": "8e8d1d72f2", "BRANCH_ID": "f0f78ec5b5", 
#          "COMMIT_ID": "08c438b716", "BRANCH_NAME": "base design"}

# Revit = {"STREAM_ID": "1ee6b67f72", "BRANCH_ID": "'95a09c4e56'", 
#          "COMMIT_ID": "7bb81e4454", "BRANCH_NAME": "main"}

# Blender = {"STREAM_ID": "c6c6e4e829", "BRANCH_ID": "9c691752ef", 
#          "COMMIT_ID": "b11a6fd0ad", "BRANCH_NAME": "main"}

# client = SpeckleClient(host=HOST)
# account = get_account_from_token(token=TOKEN, server_url=HOST)
# client.authenticate_with_account(account=account)

# # print(client.stream.list())

# # print(client.branch.list(Blender["STREAM_ID"]))
# # print(client.commit.list(Blender["STREAM_ID"]))

# stream = client.stream.get(Revit["STREAM_ID"])
# commit = client.commit.get(commit_id=Revit["COMMIT_ID"], stream_id=Revit["STREAM_ID"])
# branch = client.branch.get(stream_id=Revit["STREAM_ID"], name=Revit["BRANCH_NAME"])

# # print(branch_panelka)

# # obj = Speckle.Object(client=client, stream=stream_panelka, branch=branch_panelka, commit=commit_panelka)
# # print(obj)

# transport = ServerTransport(stream_id=stream.id, client=client)
# last_obj_id = commit.referencedObject
# speckle_mesh = operations.receive(obj_id=last_obj_id, remote_transport=transport)

# data = speckle_mesh['elements']

# # for each in data:
# #     print(each)

# first_data = data[0]
# first_el = first_data.elements[0]
# print(dir(first_el))
# # print(first_el.parameters)

# # first = data[0]
# # first_el = first.elements[0]
# # print(first_el.elementId)