from specklepy.api.client import SpeckleClient
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from specklepy.api.wrapper import StreamWrapper

HOST = "https://app.speckle.systems"
TOKEN = "08edb0eea2f618aac0f3c5ef166605fcef34ce3f68"
StreamID2 = "0cf5412fbe"
NewLink = "https://app.speckle.systems/projects/0cf5412fbe/models/604bc1bedc"

client = SpeckleClient(host=HOST)
account = get_account_from_token(TOKEN, HOST)
client.authenticate_with_account(account=account)

def pull_stream_names(token, host="https://app.speckle.systems"):
    data = [(stream.name, stream.id) for stream in client.stream.list()]
    names = [i[0] for i in data]
    return names

#print(list(pull_stream_names(token="08edb0eea2f618aac0f3c5ef166605fcef34ce3f68").keys()))