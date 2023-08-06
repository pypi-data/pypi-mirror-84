import os
import re
import subprocess
import sys

import docker
import docker.errors

HELP_TEXT = """\
Usage:
Use this script like you would with cp
to refer to the path of a docker volume, insert docker:<volume_name>/ instead
"""

DOCKER_VOLUME_RE = re.compile("(?<=docker:)[\\w]+(?=/)", re.ASCII)
DOCKER_CLIENT = docker.client.DockerClient(base_url=os.environ.get("DOCKER_API"))


def _get_dockerized_path(match: re.Match):
    """
    Calculate the absolute path for docker volumes
    :param match: Match of DOCKER_VOLUME_RE
    :return: base string of match with the match of DOCKER_VOLUME_RE replaced by the absolute path
    """
    try:
        path = DOCKER_CLIENT.volumes.get(match[0]).attrs["Mountpoint"]
    except docker.errors.NotFound:
        print("Error: Volume {} not found".format(match.group(0)))
        sys.exit(1)
    except docker.errors.APIError:
        print("Error: No API connection\nSet API address in environment variable DOCKER_API.")
        sys.exit(1)
    # Path replacement
    return match.string.replace("docker:{}".format(match[0]), path, 1)


def run():
    cp_args = ["cp"]
    if len(sys.argv) <= 1:
        # No arguments
        print(HELP_TEXT)
        sys.exit(1)
    for arg in sys.argv[1:]:
        # Iterate over all arguments except script name
        match = DOCKER_VOLUME_RE.search(arg)
        # Calculate path if necessary, else pass raw inpute
        cp_args.append(_get_dockerized_path(match) if match else arg)
    # Actually run cp and pass return code
    sys.exit(subprocess.call(cp_args))
