from viktor import ViktorController
from viktor import UserMessage, progress_message, UserError
from viktor.parametrization import ViktorParametrization, NumberField, ColorField, TextField, IntegerField, TextAreaField, OutputField, Image, ActionButton, Text, Field, OptionField, Step, OptionListElement
from viktor.geometry import SquareBeam, Color, Material, Group, LinearPattern, Point, Sphere
from viktor.views import GeometryResult, GeometryView, DataView, DataResult, DataGroup, DataItem
from viktor.result import DownloadResult

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token

def pull_stream_names(params, **kwargs):
    client = SpeckleClient(host=params.step_1.user_speckle_server_url)
    account = get_account_from_token(token=params.step_1.user_token,
                                     server_url=params.step_1.user_speckle_server_url)
    client.authenticate_with_account(account=account)
    data = [(stream.name, stream.id) for stream in client.stream.list()]

    #params.stream_map = {i[0]: i[1] for i in data.items()}

    names = [i[0] for i in data]
    return names

def pull_commits(params, **kwargs):
    client = SpeckleClient(host=params.step_1.user_speckle_server_url)
    account = get_account_from_token(token=params.step_1.user_token,
                                     server_url=params.step_1.user_speckle_server_url)
    client.authenticate_with_account(account=account)
    data = {stream.name: stream.id for stream in client.stream.list()}
    #stream = client.stream.get(STREAM_ID)
    #print(client.commit.list(stream_id=STREAM_ID))

    return [commit.message for commit in client.commit.list(stream_id=data[params.step_2.selected_stream])] 

def validate_step_1(params, **kwargs):
    if len(params.step_1.user_token) != 42:
        raise UserError("The length of token is bad")

class Parametrization(ViktorParametrization):

    #First Step
    step_1 = Step('Step 1 - Speckle data input', on_next=validate_step_1)
    step_1.intro = Text("Insert Speckle token with required permissions and if needed specify the Speckle seerver URL")
    step_1.user_token = TextField("Enter you Speckle Token")
    step_1.user_speckle_server_url = TextField("Enter Speckle sever URL, default is https://app.speckle.systems", 
                                               default="https://app.speckle.systems")

    #Second Step
    step_2 = Step('Step 2 - Speckle stream selection')
    step_2.intro = Text("Choose one of the streams")
    step_2.selected_stream = OptionField("Available Speckle streams from your account", 
                                         options=pull_stream_names)

    #Third Step
    step_3 = Step('Step 3 - Speckle commit selection')
    step_3.selected_commit = OptionField("Available commits in the selected stream",
                                          options=pull_commits)

class Controller(ViktorController):
    label = 'Repoting'
    parametrization = Parametrization
    text = Text("Here we are")

    @GeometryView('3D Geometry', duration_guess=1, x_axis_to_right=True)
    def get_3d_view(self, params, **kwargs):
        geometry = Sphere(Point(0, 0, 0), radius=params.number)
        UserMessage.info("Dimensions were changed")
        return GeometryResult(geometry)
    
    @DataView('Data', duration_guess=1)
    def get_data_view(self, params, **kwargs):
        addition = params.x + params.y
        multiplication = params.x * params.y
        text = Text("Here we are")

        main_data_group = DataGroup(
            DataItem('Data item 1', addition),
            DataItem('Data item 2', multiplication),
            DataItem('Some text', text)
        )

        return DataResult(main_data_group)

    def download_file(self, params, **kwargs):
        return DownloadResult('file content', 'file name')
    
    def perform_action(self, params, **kwargs):
        return OutputField("info")