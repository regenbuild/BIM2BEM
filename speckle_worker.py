from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_local_accounts, get_default_account
from specklepy.objects import Base
from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper

from collections.abc import Iterable, Mapping

# HOST = "https://app.speckle.systems"

# client = SpeckleClient(HOST)
# account = get_default_account()
# client.authenticate_with_account(account)
# streams = client.stream.list()

StreamID = "6c14c7d5e4"
StreamID2 = "0cf5412fbe"

CommitID = "1dd9d27dd5"
CommitID2 = "b2f865c0fc"


Link = "https://app.speckle.systems/projects/6c14c7d5e4/models/ebc1382b07"
Link2 = "https://app.speckle.systems/projects/0cf5412fbe/models/604bc1bedc"
# stream = client.stream.get(StreamID2)
# print(stream)
# commits = client.commit.list(StreamID2)
# print(commits)

# commit2 = client.commit.get(StreamID2, CommitID2)
# print(commit2)
# obj_id = commit2.referencedObject

# commit2_data = operations.receive(obj_id)
# print(commit2_data)

wrapper = StreamWrapper(Link2)
client = wrapper.get_client()
transport = wrapper.get_transport()

commit = client.commit.get(StreamID2, CommitID2)
ref_obj = commit.referencedObject

#print(commit.model_json_schema())
commit_data = operations.receive(ref_obj, transport)

print(commit_data.get_dynamic_member_names())
#print(commit_data["6b2365a59c04879f388e0997c195e872"])
####
#print(dir(commit_data))

def flatten(obj, visited = None):
    if visited is None:
        visited = set()

    if obj in visited:
        return
    
    visited.add(obj)

    should_include = any(
        [
            hasattr(obj, "displayValue"),
            hasattr(obj, "speckle_type") and
            obj.speckle_type == "Objects.Organization.Collection",
            hasattr(obj, "displayStyle")
        ]
    )

    if should_include:
        yield obj
    
    props = obj.__dict__

    for prop in props:
        value = getattr(obj, prop)

        if value is None:
            continue

        if isinstance(value, Base):
            yield from flatten(value, visited)

        elif isinstance(value, Mapping):
            for dict_value in value.values():
                if isinstance(dict_value, Base):
                    yield from flatten(dict_value, visited)

        elif isinstance(value, Iterable):
            for list_value in value:
                if isinstance(list_value, Base):
                    yield from flatten(list_value, visited)