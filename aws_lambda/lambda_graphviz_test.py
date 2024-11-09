# LD_LIBRARY_PATH = /opt/python/lib64:/usr/lib64:/lib64

import subprocess
import os

def lambda_handler(event, context):

    # os.environ["CGO_ENABLED"] = "0"

    try:
        graph = "digraph G { A -> B; B -> C; C -> A; }"
        with open("/tmp/test.dot", "w") as f:
            f.write(graph)
        
        result = subprocess.run(
            ["/opt/python/bin/dot", "-Tpng", "/tmp/test.dot", "-o", "/tmp/test.png"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Error running dot:", result.stderr)
        else:
            print("dot ran successfully. Output file created at /tmp/test.png")
    except Exception as e:
        print(f"Error executing dot command: {e}")
