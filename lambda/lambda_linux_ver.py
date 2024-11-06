import platform

def lambda_handler(event, context):
    return platform.platform()

    # Lambda: "Linux-5.10.226-235.879.amzn2.x86_64-x86_64-with-glibc2.2.5"
    # EC2:    "Linux-6.1.112-122.189.amzn2023.x86_64-x86_64 with glibc2.34"