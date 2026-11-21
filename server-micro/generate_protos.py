"""Generate the gRPC Python code from every .proto in protos/.

Run from server-micro/ after any change to a .proto:
    python generate_protos.py
The Dockerfile runs this too, so the generated files aren't committed.
"""
import pathlib
import sys

import grpc_tools
from grpc_tools import protoc

HERE = pathlib.Path(__file__).resolve().parent
# Google's built-in types (timestamp.proto, struct.proto), used by hardware.proto
WELL_KNOWN = pathlib.Path(grpc_tools.__file__).parent / "_proto"
protos = sorted(str(p) for p in (HERE / "protos").glob("*.proto"))

result = protoc.main([
    "grpc_tools.protoc",
    f"-I{HERE / 'protos'}",
    f"-I{WELL_KNOWN}",
    f"--python_out={HERE}",
    f"--pyi_out={HERE}",
    f"--grpc_python_out={HERE}",
    *protos,
])
if result != 0:
    sys.exit(f"protoc failed with exit code {result}")
print("Generated code for:", ", ".join(pathlib.Path(p).name for p in protos))