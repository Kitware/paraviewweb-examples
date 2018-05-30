# import paraview modules.
from paraview.web.protocols import ParaViewWebProtocol
from paraview import simple

# import RPC annotation
from wslink import register as exportRpc

class UserProtocol(ParaViewWebProtocol):
  def __init__(self, viewIds):
    super(UserProtocol, self).__init__()
    self.viewIds = viewIds

  # return a dictionary of numeric column names and their ranges, plus other initialization info.
  @exportRpc('my.protocols.views')
  def getViews(self):
    return self.viewIds
