from viktor import ViktorController
from viktor import UserMessage, progress_message
from viktor.parametrization import ViktorParametrization, NumberField, ColorField, TextField, IntegerField, TextAreaField, OutputField, Image, ActionButton, Text, Field, OptionField
from viktor.geometry import SquareBeam, Color, Material, Group, LinearPattern, Point, Sphere
from viktor.views import GeometryResult, GeometryView, DataView, DataResult, DataGroup, DataItem
from viktor.result import DownloadResult

from speckle_worker import pull_stream_names

class Parametrization(ViktorParametrization):
    intro = Text("RegenBuild v. 0.1 pulls data from Speckle ")
    user_token = TextField("Enter you Speckle Token", default=None)
    user_speckle_server_url = TextField("Enter Speckle sever URL, default is https://app.speckle.systems", default="https://app.speckle.systems")
    if user_token is not None:
        streams_data = pull_stream_names(token=user_token, host=user_speckle_server_url)
        #streams_names = list(streams_data.keys())
        print("\nDown to here\n")
        selected_stream = OptionField("Speckle streams from your account", options=streams_data, default="Stream 1")

class Controller(ViktorController):
    label = 'Repoting'
    parametrization = Parametrization
    text = Text("Here we are")

    # @GeometryView('3D Geometry', duration_guess=1, x_axis_to_right=True)
    # def get_3d_view(self, params, **kwargs):
    #     geometry = Sphere(Point(0, 0, 0), radius=params.number)
    #     UserMessage.info("Dimensions were changed")
    #     return GeometryResult(geometry)
    
    # @DataView('Data', duration_guess=1)
    # def get_data_view(self, params, **kwargs):
    #     addition = params.x + params.y
    #     multiplication = params.x * params.y
    #     text = Text("Here we are")

    #     main_data_group = DataGroup(
    #         DataItem('Data item 1', addition),
    #         DataItem('Data item 2', multiplication),
    #         DataItem('Some text', text)
    #     )

    #     return DataResult(main_data_group)

    # def download_file(self, params, **kwargs):
    #     return DownloadResult('file content', 'file name')
    
    # def perform_action(self, params, **kwargs):
    #     return OutputField("info")
