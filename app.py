from viktor import ViktorController
from viktor import UserMessage, progress_message
from viktor.parametrization import ViktorParametrization, NumberField, ColorField, TextField, IntegerField, TextAreaField, OutputField, Image
from viktor.geometry import SquareBeam, Color, Material, Group, LinearPattern, Point, Sphere
from viktor.views import GeometryResult, GeometryView, DataView, DataResult, DataGroup, DataItem
from viktor.result import DownloadResult

#from speckle_worker import receive_from_speckle

class Parametrization(ViktorParametrization):
    x = NumberField('X')
    y = NumberField('Y')
    number = IntegerField('Enter some number', min=0, max=10, default=5)
    info = TextAreaField("This is area field", default="This is a default value")
    #img = Image("path=/assets/Regen.png")

class ModelController(ViktorController):
    label = 'Model'
    parametrization = Parametrization

    @GeometryView('3D Geometry', duration_guess=1, x_axis_to_right=True)
    def get_3d_view(self, params, **kwargs):
        geometry = Sphere(Point(0, 0, 0), radius=params.number)
        UserMessage.info("Dimensions were changed")
        return GeometryResult(geometry)
    
    @DataView('Data', duration_guess=1)
    def get_data_view(self, params, **kwargs):
        addition = params.x + params.y
        multiplication = params.x * params.y

        main_data_group = DataGroup(
            DataItem('Data item 1', addition),
            DataItem('Data item 2', multiplication)
        )

        return DataResult(main_data_group)

    def download_file(self, params, **kwargs):
        return DownloadResult('file content', 'file name')
