"""Module contains the ec2 wrapper class."""
import json
import os
from typing import Any, Dict, Generator, List, Optional, Union

from fzfaws.utils import BaseSession, Pyfzf, Spinner, get_name_tag


class EC2(BaseSession):
    """A wrapper class for EC2.

    Handles the selection of ec2 instance and also
    fetching other ec2 related calls including VPC,
    subnet stuff as well.

    :param profile: profile to use for this operation
    :type profile: Union[bool, str], optional
    :param region: region to use for this operation
    :type region: Union[bool, str], optional
    """

    def __init__(
        self,
        profile: Optional[Union[str, bool]] = None,
        region: Optional[Union[str, bool]] = None,
    ) -> None:
        """Construct the instance."""
        super().__init__(profile=profile, region=region, service_name="ec2")
        self.instance_list: list = [{}]
        self.instance_ids: list = [""]

    def set_ec2_instance(
        self, multi_select: bool = True, header: str = None, no_progress: bool = False
    ) -> None:
        """Set ec2 instance for current operation.

        :param multi_select: enable multi select
        :type multi_select: bool, optional
        :param header: helper information to display in fzf header
        :type header: str, optional
        :param no_progress: don't display progress bar, useful for ls command
        :type no_progress: bool, optional
        """
        fzf = Pyfzf()
        with Spinner.spin(
            message="Fetching EC2 instances ...", no_progress=no_progress
        ):
            paginator = self.client.get_paginator("describe_instances")
            for result in paginator.paginate():
                response_generator = self._instance_generator(result["Reservations"])
                fzf.process_list(
                    response_generator,
                    "InstanceId",
                    "Status",
                    "InstanceType",
                    "Name",
                    "KeyName",
                    "PublicDnsName",
                    "PublicIpAddress",
                    "PrivateIpAddress",
                )
        selected_instance = fzf.execute_fzf(
            multi_select=multi_select, header=header, print_col=0
        )

        if multi_select:
            self.instance_ids[:] = []
            self.instance_list[:] = []
            for instance in selected_instance:
                curr = fzf.format_selected_to_dict(str(instance))
                self.instance_list.append(curr)
                self.instance_ids.append(curr["InstanceId"])
        else:
            self.instance_ids[:] = []
            self.instance_list[:] = []
            self.instance_list.append(
                fzf.format_selected_to_dict(str(selected_instance))
            )
            self.instance_ids.append(self.instance_list[0]["InstanceId"])
        if len(self.instance_ids) == 0:
            self.instance_ids = [""]
        if len(self.instance_list) == 0:
            self.instance_list = [{}]

    def print_instance_details(self) -> None:
        """Display information for the selected instances.

        Call this method before calling boto3 to do any ec2 opeartion
        and get confirmation.
        """
        for instance in self.instance_list:
            print(
                "InstanceId: %s  Name: %s" % (instance["InstanceId"], instance["Name"])
            )

    def wait(self, waiter_name: str, message: str = None) -> None:
        """Wait for the operation to be completed.

        This method uses the boto3 waiter.

        :param waiter_name: name of boto3 waiter
        :type waiter_name: str
        :param message: message to display during loading
        :type message: str, optional
        """
        with Spinner.spin(message=message):
            waiter = self.client.get_waiter(waiter_name)
            waiter_config = os.getenv(
                "FZFAWS_EC2_WAITER", os.getenv("FZFAWS_GLOBAL_WAITER", "")
            )
            delay: int = 15
            max_attempts: int = 40
            if waiter_config:
                waiter_config = json.loads(waiter_config)
                delay = int(waiter_config.get("delay", 15))
                max_attempts = int(waiter_config.get("max_attempts", 40))
            waiter.wait(
                InstanceIds=self.instance_ids,
                WaiterConfig={"Delay": delay, "MaxAttempts": max_attempts},
            )

    def get_security_groups(
        self,
        multi_select: bool = False,
        return_attr: str = "id",
        header: str = None,
        no_progress: bool = False,
    ) -> Union[str, list]:
        """Use paginator to get the user selected security groups.

        :param multi_select: allow multiple value selection
        :type multi_select: bool, optional
        :param return_attr: what attribute to return (id|name)
        :type return_attr: str, optional
        :param header: header to display in fzf
        :type header: str, optional
        :param no_progress: don't display progress bar, useful for ls command
        :type no_progress: bool, optional
        :return: selected security groups/ids
        :rtype: Union[str, list]
        """
        fzf = Pyfzf()
        with Spinner.spin(
            message="Fetching SecurityGroups ...", no_progress=no_progress
        ):
            paginator = self.client.get_paginator("describe_security_groups")
            for result in paginator.paginate():
                response_generator = self._name_tag_generator(
                    result.get("SecurityGroups", [])
                )
                if return_attr == "id":
                    fzf.process_list(response_generator, "GroupId", "GroupName", "Name")
                elif return_attr == "name":
                    fzf.process_list(response_generator, "GroupName", "Name")
        return fzf.execute_fzf(
            multi_select=multi_select, empty_allow=True, header=header
        )

    def get_instance_id(
        self, multi_select: bool = False, header: str = None
    ) -> Union[str, list]:
        """Use paginator to get instance id and return it.

        :param multi_select: allow multiple value selection
        :type multi_select: bool, optional
        :param header: header to display in fzf header
        :type header: str, optional
        :return: selected instance id
        :rtype: Union[str, list]
        """
        fzf = Pyfzf()
        with Spinner.spin(message="Fetching EC2 instances ..."):
            paginator = self.client.get_paginator("describe_instances")
            for result in paginator.paginate():
                response_generator = self._instance_id_generator(
                    result.get("Reservations", [])
                )
                fzf.process_list(response_generator, "InstanceId", "Name")
        return fzf.execute_fzf(
            multi_select=multi_select, empty_allow=True, header=header
        )

    def get_subnet_id(
        self, multi_select: bool = False, header: str = None, no_progress: bool = False
    ) -> Union[str, list]:
        """Get user selected subnet id through fzf.

        :param multi_select: allow multiple value selection
        :type multi_select: bool, optional
        :param header: header to display in fzf header
        :type header: str, optional
        :return: selected subnet id
        :param no_progress: don't display progress bar, useful for ls command
        :type no_progress: bool, optional
        :rtype: Union[str, list]
        """
        fzf = Pyfzf()
        with Spinner.spin(message="Fetching Subnets ...", no_progress=no_progress):
            paginator = self.client.get_paginator("describe_subnets")
            for result in paginator.paginate():
                response_generator = self._name_tag_generator(result.get("Subnets", []))
                fzf.process_list(
                    response_generator,
                    "SubnetId",
                    "AvailabilityZone",
                    "CidrBlock",
                    "Name",
                )
        return fzf.execute_fzf(
            multi_select=multi_select, empty_allow=True, header=header
        )

    def get_volume_id(
        self, multi_select: bool = False, header: str = None, no_progress: bool = False
    ) -> Union[str, list]:
        """Get user selected volume id through fzf.

        :param multi_select: allow multiple value selection
        :type multi_select: bool, optional
        :param header: header to display in fzf header
        :type header: str, optional
        :param no_progress: don't display progress bar, useful for ls command
        :type no_progress: bool, optional
        :return: selected volume id
        :rtype: Union[str, list]
        """
        fzf = Pyfzf()
        with Spinner.spin(message="Fetching EBS volumes ...", no_progress=no_progress):
            paginator = self.client.get_paginator("describe_volumes")
            for result in paginator.paginate():
                response_generator = self._name_tag_generator(result.get("Volumes", []))
                fzf.process_list(response_generator, "VolumeId", "Name")
        return fzf.execute_fzf(
            multi_select=multi_select, empty_allow=True, header=header
        )

    def get_vpc_id(
        self, multi_select: bool = False, header: str = None, no_progress: bool = False
    ) -> Union[str, list]:
        """Get user selected vpc id through fzf.

        :param multi_select: allow multiple value selection
        :type multi_select: bool, optional
        :param header: header to display in fzf header
        :type header: str, optional
        :param no_progress: don't display progress bar, useful for ls command
        :type no_progress: bool, optional
        :return: selected vpc id
        :rtype: Union[str, list]
        """
        fzf = Pyfzf()
        with Spinner.spin(message="Fetching VPCs ...", no_progress=no_progress):
            paginator = self.client.get_paginator("describe_vpcs")
            for result in paginator.paginate():
                response_generator = self._name_tag_generator(result.get("Vpcs", []))
                fzf.process_list(
                    response_generator, "VpcId", "IsDefault", "CidrBlock", "Name"
                )
        return fzf.execute_fzf(
            empty_allow=True, multi_select=multi_select, header=header
        )

    def _name_tag_generator(
        self, response: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        for item in response:
            yield {**item, "Name": get_name_tag(item)}

    def _instance_id_generator(
        self, instances: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Create a generator for listing instance ids.

        :param instances: list of instance from boto3 response
        :type instances: List[Dict[str, Any]]
        :return: formatted dict of instance id information in generator form
        :rtype: Generator[Dict[str,Any], None, None]
        """
        for instance in instances:
            yield {
                "InstanceId": instance["Instances"][0]["InstanceId"],
                "Name": get_name_tag(instance["Instances"][0]),
            }

    def _instance_generator(
        self, instances: List[Dict[str, Any]]
    ) -> Generator[Dict[str, str], None, None]:
        """Get ec2 instance helper, format ec2 response and return generator.

        :param instances: list of instance response from boto3
        :type instances: List[Dict[str, Any]]
        :return: formatted dict of instance information in generator form
        :rtype: Generator[Dict[str,str], None, None]
        """
        for instance in instances:
            instance_information = {
                "InstanceId": instance["Instances"][0].get("InstanceId"),
                "InstanceType": instance["Instances"][0].get("InstanceType"),
                "Status": instance["Instances"][0]["State"].get("Name"),
                "Name": get_name_tag(instance["Instances"][0]),
                "KeyName": instance["Instances"][0].get("KeyName"),
                "PublicDnsName": instance["Instances"][0].get("PublicDnsName")
                if instance["Instances"][0].get("PublicDnsName")
                else None,
                "PublicIpAddress": instance["Instances"][0].get("PublicIpAddress"),
                "PrivateIpAddress": instance["Instances"][0].get("PrivateIpAddress"),
            }
            yield instance_information
