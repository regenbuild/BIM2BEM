from viktor import ViktorController
from viktor import UserMessage, progress_message, UserError
from viktor.parametrization import ViktorParametrization, NumberField, ColorField, TextField, IntegerField, TextAreaField, OutputField, Image, ActionButton, Text, Field, OptionField, Step, OptionListElement
from viktor.geometry import SquareBeam, Color, Material, Group, LinearPattern, Point, Sphere
from viktor.views import GeometryResult, GeometryView, DataView, DataResult, DataGroup, DataItem
from viktor.result import DownloadResult

from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token

from topologicpy.Speckle import Speckle

def pull_client(params, **kwargs):
    """Temporary solution to get authentificated client
    There must be a way to cache authentificated client in viktor"""
    client = SpeckleClient(host=params.step_1.user_speckle_server_url)
    account = get_account_from_token(token=params.step_1.user_token,
                                     server_url=params.step_1.user_speckle_server_url)
    client.authenticate_with_account(account=account)
    return client

def pull_stream_names(params, **kwargs):
    """Pulls stream names from Speckle server for user to choose"""
    client = pull_client(params=params)
    return [stream.name for stream in client.stream.list()]

def pull_stream_itself(params, **kwargs):
    """Pulls stream object from Speckle server according to selection choice from user"""
    client = pull_client(params=params)
    data = {stream.name: stream.id for stream in client.stream.list()}
    return client.stream.get(data[params.step_2.selected_stream_name])

def pull_commits_names(params, **kwargs):
    """Pulls commits names from Speckle server for user to select"""
    client = pull_client(params=params)
    data = {stream.name: stream.id for stream in client.stream.list()}
    return [commit.message for commit in client.commit.list(stream_id=data[params.step_2.selected_stream_name])]

def pull_commit_itself(params, **kwargs):
    """Pulls commit object from Speckle server according to the user choice"""
    client = pull_client(params=params)
    data_stream = {stream.name: stream.id for stream in client.stream.list()}
    data_commit = {commit.message: commit.id for commit in client.commit.list(stream_id=data_stream[params.step_2.selected_stream_name])}
    return client.commit.get(stream_id=data_stream[params.step_2.selected_stream_name],
                             commit_id=data_commit[params.step_3.selected_commit_name])

def pull_branches_names(params, **kwargs):
    """Pulls branches names for user to select"""
    client = pull_client(params=params)
    data = {stream.name: stream.id for stream in client.stream.list()}
    return [branch.name for branch in client.branch.list(stream_id=data[params.step_2.selected_stream_name])]

def pull_branch_itself(params, **kwargs):
    """Pulls branch object from Speckle according to the selected parameters"""
    client = pull_client(params=params)
    #data_branch = {branch.name: branch.id for branch in client.branch.list()}
    data_stream = {stream.name: stream.id for stream in client.stream.list()}
    return client.branch.get(stream_id=data_stream[params.step_2.selected_stream_name],
                             name=params.step_3.selected_branch_name)

def validate_step_1(params, **kwargs):
    if len(params.step_1.user_token) != 42:
        raise UserError("The length of token is bad")

class Parametrization(ViktorParametrization):

    #Speckle credentials Step
    step_1 = Step('Step 1 - Speckle data input', on_next=validate_step_1)
    step_1.intro = Text("Insert Speckle token with required permissions and if needed specify the Speckle seerver URL")
    step_1.user_token = TextField("Enter you Speckle Token")
    step_1.user_speckle_server_url = TextField("Enter Speckle sever URL, default is https://app.speckle.systems", 
                                               default="https://app.speckle.systems")

    #Stream selection step
    step_2 = Step('Step 2 - Speckle stream selection')
    step_2.intro = Text("Choose one of the streams")
    step_2.selected_stream_name = OptionField("Available Speckle streams from your account", 
                                         options=pull_stream_names)

    #Commit and branch selection step
    step_3 = Step('Step 3 - Speckle commit selection and Branch selection')
    step_3.intro = Text("Choose commit and branch")
    step_3.selected_commit_name = OptionField("Available commits in the selected stream",
                                          options=pull_commits_names)
    step_3.selected_branch_name = OptionField("Available branches",
                                             options=pull_branches_names)
    
    step_4 = Step('Step 4 - Energy simulation parametrization', views="get_data_view")
    step_4.intro = Text("Soup iz semi zalup")

class Controller(ViktorController):
    label = 'Repoting'
    parametrization = Parametrization
    text = Text("Here we are")

    # @GeometryView('3D Geometry', duration_guess=1, x_axis_to_right=True)
    # def get_3d_view(self, params, **kwargs):
    #     geometry = Sphere(Point(0, 0, 0), radius=params.number)
    #     UserMessage.info("Dimensions were changed")
    #     return GeometryResult(geometry)
    
    @DataView('Data', duration_guess=1)
    def get_data_view(self, params, **kwargs):
        # addition = params.x + params.y
        # multiplication = params.x * params.y
        # text = Text("Here we are")
        stream = pull_stream_itself(params=params)
        commit = pull_commit_itself(params=params)
        branch = pull_branch_itself(params=params)
        client = SpeckleClient(host=params.step_1.user_speckle_server_url)
        account = get_account_from_token(token=params.step_1.user_token,
                                     server_url=params.step_1.user_speckle_server_url)
        client.authenticate_with_account(account=account)

        topologic_obj_flag = None
        try:
            topologic_obj = Speckle.Object(client=client, stream=stream, branch=branch, commit=commit)
            topologic_obj_flag = True
        except:
            topologic_obj_flag = False

        main_data_group = DataGroup(
            DataItem('Testing data from stream', stream.id),
            DataItem('Testing data from commit', commit.id),
            DataItem('Testing data from branch', branch.name),
            DataItem('Topologic obj', str(topologic_obj_flag))
        )

        return DataResult(main_data_group)

    def download_file(self, params, **kwargs):
        return DownloadResult('file content', 'file name')
    
    def perform_action(self, params, **kwargs):
        return OutputField("info")