from requests.exceptions import ConnectionError
from datetime import datetime
from typing import Dict, Union
from cincanregistry import Remotes
from cincanregistry.models.tool_info import ToolInfo
from cincanregistry.models.version_info import VersionInfo
from cincanregistry.utils import parse_file_time, split_tool_tag
from ._registry import RegistryBase
import logging
import docker


class DaemonRegistry(RegistryBase):
    """
    Simple wrapper to handle images through local Docker Daemon
    """

    def __init__(self, *args, **kwargs):
        super(DaemonRegistry, self).__init__(*args, **kwargs)
        self.registry_name = "Docker Daemon"
        self.logger = logging.getLogger("daemon")
        try:
            self.client: docker.DockerClient = docker.from_env()
        except docker.errors.DockerException as e:
            self.logger.error(f"Failed to connect to Docker server: {e}")
            self.client = None

    def _is_docker_running(self):
        """
        Check if Docker Daemon is running
        """
        try:
            self.client.ping()
            return True
        except (ConnectionError, AttributeError):
            self.logger.error("Failed to connect to Docker Server. Is it running?")
            self.logger.error("Not able to list or use local tools.")
            return False

    def _get_version_from_container_config_env(self, attrs: dict) -> str:
        """
        Parse version information ENV from local image attributes
        """
        environment = attrs.get("Config").get("Env")
        for var in environment:
            if "".join(var).split("=")[0] == self.version_var:
                version = "".join(var).split("=")[1]
                return version
        return ""

    def get_version_by_image_id(self, image_id: str) -> str:
        """Get version of local image by ID"""
        if not self._is_docker_running():
            return ""
        image = self.client.images.get(image_id)
        version = self._get_version_from_container_config_env(image.attrs)
        return version

    def create_local_tool_info_by_name(self, name: str) -> Union[ToolInfo, None]:
        """Find local images by name, return ToolInfo object with version list"""
        if not self._is_docker_running():
            return None
        images = self.client.images.list(name, filters={"dangling": False})
        if not images:
            return None
        source = "local"
        name, tag = split_tool_tag(name)
        tool = ToolInfo(name, datetime.now(), source)
        images.sort(key=lambda x: parse_file_time(x.attrs["Created"]), reverse=True)
        versions = []
        for i in images:
            updated = parse_file_time(i.attrs["Created"])
            version = self._get_version_from_container_config_env(i.attrs)
            if not version:
                version = self.VER_UNDEFINED
            tags = set(i.tags)
            size = i.attrs.get("Size")
            if not versions:
                versions.append(VersionInfo(version, source, tags, updated, size=size))
                continue
            for v in versions:
                if v == version:
                    v.tags.union(tags)
                    break
                else:
                    versions.append(
                        VersionInfo(version, source, tags, updated, size=size)
                    )
        tool.versions = versions
        return tool

    async def get_tools(
            self,
            defined_tag: str = "",
            prefix: str = "cincan/",
    ) -> Dict[str, ToolInfo]:
        """
        List tools from the locally available docker images
        Only tools with starts with 'prefix' are listed.
        Additionally, if tag is defined, tool must have this tag
        before it is listed.
        """
        if not self._is_docker_running():
            return {}
        images = self.client.images.list(filters={"dangling": False})
        # images oldest first (tags are listed in proper order)
        images.sort(key=lambda x: parse_file_time(x.attrs["Created"]), reverse=True)
        ret = {}
        for i in images:
            if len(i.tags) == 0:
                continue  # not sure what these are...
            updated = parse_file_time(i.attrs["Created"])
            for t in i.tags:
                # version = default_ver
                existing_ver = False
                stripped_tags = [
                    split_tool_tag(tag)[1] if tag.startswith(prefix) else tag
                    for tag in i.tags
                ]
                name, tag = split_tool_tag(t)
                if name.startswith(prefix):
                    if not defined_tag or tag == defined_tag:
                        version = self._get_version_from_container_config_env(i.attrs)
                        if name in ret:
                            for j, v in enumerate(ret[name].versions):
                                if v.version == version:
                                    existing_ver = True
                                    self.logger.debug(
                                        f"same version found for tool {name} with version {version} as tag {tag} "
                                    )
                                    ret[name].versions[j].tags.union(set(stripped_tags))
                                    break
                            if not existing_ver:
                                self.logger.debug(
                                    f"Appending new version {version} to existing entry {name} with tag {tag}."
                                )
                                ret[name].versions.append(
                                    VersionInfo(
                                        version,
                                        self.registry_name,
                                        set(stripped_tags),
                                        updated,
                                        size=i.attrs.get("Size"),
                                    )
                                )
                        else:
                            ver_info = VersionInfo(
                                version,
                                self.registry_name,
                                set(stripped_tags),
                                updated,
                                size=i.attrs.get("Size"),
                            )
                            ret[name] = ToolInfo(
                                name, updated, "local", versions=[ver_info]
                            )
                            self.logger.debug(
                                f"Added local tool {name} based on tag {t} with version {version}"
                            )
                            continue
                    else:
                        continue
        return ret
