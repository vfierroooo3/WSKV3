"""Generate the gRPC Python code from protos/projects.proto.

Run from server-micro/ after any change to the .proto:
    python generate_protos.py
Writes projects_pb2.py, projects_pb2.pyi and projects_pb2_grpc.py next to this
file. The Dockerfile runs this too, so the generated files aren't committed.
"""
import pathlib
import sys

from grpc_tools import protoc

HERE = pathlib.Path(__file__).resolve().parent

result = protoc.main([
    "grpc_tools.protoc",
    f"-I{HERE / 'protos'}",
    f"--python_out={HERE}",
    f"--pyi_out={HERE}",
    f"--grpc_python_out={HERE}",
    str(HERE / "protos" / "projects.proto"),
])
if result != 0:
    sys.exit(f"protoc failed with exit code {result}")
print("Generated projects_pb2.py, projects_pb2.pyi, projects_pb2_grpc.py")
