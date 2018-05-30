import os
import sys

# Try handle virtual env if provided
if '--virtual-env' in sys.argv:
  virtualEnvPath = sys.argv[sys.argv.index('--virtual-env') + 1]
  virtualEnv = virtualEnvPath + '/bin/activate_this.py'
  execfile(virtualEnv, dict(__file__=virtualEnv))

# import paraview modules.
from paraview.web import pv_wslink
from paraview.web import protocols as pv_protocols

from myProtocols import UserProtocol

# import RPC annotation
from wslink import register as exportRpc

from paraview import simple
from wslink import server

try:
    import argparse
except ImportError:
    # since  Python 2.6 and earlier don't have argparse, we simply provide
    # the source for the same as _argparse and we use it instead.
    from vtk.util import _argparse as argparse

# =============================================================================
# Create custom Pipeline Manager class to handle clients requests
# =============================================================================

class MultiViewServer(pv_wslink.PVServerProtocol):

    authKey = "wslink-secret"

    viewportScale=1.0
    viewportMaxWidth=2560
    viewportMaxHeight=1440

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("--virtual-env", default=None, help="Path to virtual environment to use")

    @staticmethod
    def configure(args):
        MultiViewServer.authKey = args.authKey

    def initialize(self):
        # Bring used components
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebMouseHandler())
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebViewPort(MultiViewServer.viewportScale, MultiViewServer.viewportMaxWidth, MultiViewServer.viewportMaxHeight))
        self.registerVtkWebProtocol(pv_protocols.ParaViewWebPublishImageDelivery(decode=False))

        # Update authentication key to use
        self.updateSecret(MultiViewServer.authKey)

        # tell the C++ web app to use no encoding. ParaViewWebPublishImageDelivery must be set to decode=False to match.
        self.getApplication().SetImageEncoding(0);

        # Create of 2 views with different content
        self.registerVtkWebProtocol(UserProtocol([self.addView(simple.Cone()), self.addView(simple.Sphere())]))

    def addView(self, sourceProxy):
      view = simple.CreateView('RenderView')
      view.EnableRenderOnInteraction = 0
      view.Background = [0,0,0]

      simple.Show(sourceProxy, view)

      return view.GetGlobalIDAsString()

# =============================================================================
# Main: Parse args and start server
# =============================================================================

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Multi View")

    # Add arguments
    server.add_arguments(parser)
    MultiViewServer.add_arguments(parser)
    args = parser.parse_args()
    MultiViewServer.configure(args)

    # Start server
    server.start_webserver(options=args, protocol=MultiViewServer)
