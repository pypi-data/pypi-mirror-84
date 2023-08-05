#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from typing import Optional, Generator
from typing import List

from zepben.cimbend.cim.iec61968.assets.asset import AssetContainer
from zepben.cimbend.cim.iec61968.common.location import Location
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import nlen, get_by_mrid, ngen, safe_remove

__all__ = ["Meter", "EndDevice", "UsagePoint"]

logger = logging.getLogger(__name__)


class EndDevice(AssetContainer):
    """
    Asset container that performs one or more end device functions. One type of end device is a meter which can perform
    metering, load management, connect/disconnect, accounting functions, etc. Some end devices, such as ones monitoring
    and controlling air conditioners, refrigerators, pool pumps may be connected to a meter. All end devices may have
    communication capability defined by the associated communication function(s).

    An end device may be owned by a consumer, a service provider, utility or otherwise.

    There may be a related end device function that identifies a sensor or control point within a metering application
    or communications systems (e.g., water, gas, electricity).

    Some devices may use an optical port that conforms to the ANSI C12.18 standard for communications.
    """

    customer_mrid: Optional[str] = None
    """The `zepben.cimbend.cim.iec61968.customers.customer.Customer` owning this `EndDevice`."""

    service_location: Optional[Location] = None
    """Service `zepben.cimbend.cim.iec61968.common.location.Location` whose service delivery is measured by this `EndDevice`."""

    _usage_points: Optional[List[UsagePoint]] = None

    def __init__(self, organisation_roles: List[AssetOrganisationRole] = None, usage_points: List[UsagePoint] = None):
        super().__init__(organisation_roles=organisation_roles)
        if usage_points:
            for up in usage_points:
                self.add_usage_point(up)

    def num_usage_points(self):
        """
        Returns The number of `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint`s associated with this `EndDevice`
        """
        return nlen(self._usage_points)

    @property
    def usage_points(self) -> Generator[UsagePoint, None, None]:
        """
        The `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint`s associated with this `EndDevice`
        """
        return ngen(self._usage_points)

    def get_usage_point(self, mrid: str) -> UsagePoint:
        """
        Get the `UsagePoint` for this `EndDevice` identified by `mrid`

        `mrid` the mRID of the required `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint`
        Returns The `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._usage_points, mrid)

    def add_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Associate `up` to this `zepben.cimbend.cim.iec61968.metering.metering.EndDevice`.

        `up` the `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` to associate with this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if another `UsagePoint` with the same `mrid` already exists for this `EndDevice`.
        """
        if self._validate_reference(up, self.get_usage_point, "A UsagePoint"):
            return self
        self._usage_points = list() if self._usage_points is None else self._usage_points
        self._usage_points.append(up)
        return self

    def remove_usage_point(self, up: UsagePoint) -> EndDevice:
        """
        Disassociate `up` from this `EndDevice`

        `up` the `zepben.cimbend.cim.iec61968.metering.metering.UsagePoint` to disassociate from this `EndDevice`.
        Returns A reference to this `EndDevice` to allow fluent use.
        Raises `ValueError` if `up` was not associated with this `EndDevice`.
        """
        self._usage_points = safe_remove(self._usage_points, up)
        return self

    def clear_usage_points(self) -> EndDevice:
        """
        Clear all usage_points.
        Returns A reference to this `EndDevice` to allow fluent use.
        """
        self._usage_points = None
        return self


class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed.
    Used at the place where a physical or virtual meter may be located; however, it is not required that a meter be present.
    """

    usage_point_location: Optional[Location] = None
    """Service `zepben.cimbend.cim.iec61968.common.location.Location` where the service delivered by this `UsagePoint` is consumed."""

    _equipment: Optional[List[Equipment]] = None
    _end_devices: Optional[List[EndDevice]] = None

    def __init__(self, equipment: List[Equipment] = None, end_devices: List[EndDevice] = None):
        if equipment:
            for eq in equipment:
                self.add_equipment(eq)
        if end_devices:
            for ed in end_devices:
                self.add_end_device(ed)

    def num_equipment(self):
        """
        Returns The number of `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment`s associated with this `UsagePoint`
        """
        return nlen(self._equipment)

    def num_end_devices(self):
        """
        Returns The number of `zepben.cimbend.cim.iec61968.metering.metering.EndDevice`s associated with this `UsagePoint`
        """
        return nlen(self._end_devices)

    @property
    def end_devices(self) -> Generator[EndDevice, None, None]:
        """
        The `EndDevice`'s (Meter's) associated with this `UsagePoint`.
        """
        return ngen(self._end_devices)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        The `zepben.model.Equipment` associated with this `UsagePoint`.
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` for this `UsagePoint` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment`
        Returns The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._equipment, mrid)

    def add_equipment(self, equipment: Equipment) -> UsagePoint:
        """
        Associate an `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` with this `UsagePoint`

        `equipment` The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` to associate with this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `UsagePoint`.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self

        self._equipment = list() if self._equipment is None else self._equipment
        self._equipment.append(equipment)
        return self

    def remove_equipment(self, equipment: Equipment) -> UsagePoint:
        """
        Disassociate an `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` from this `UsagePoint`

        `equipment` The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` to disassociate with this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if `equipment` was not associated with this `UsagePoint`.
        """
        self._equipment = safe_remove(self._equipment, equipment)
        return self

    def clear_equipment(self) -> UsagePoint:
        """
        Clear all equipment.
        Returns A reference to this `UsagePoint` to allow fluent use.
        """
        self._equipment = None
        return self

    def get_end_device(self, mrid: str) -> EndDevice:
        """
        Get the `EndDevice` for this `UsagePoint` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61968.metering.metering.EndDevice`
        Returns The `zepben.cimbend.cim.iec61968.metering.metering.EndDevice` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._end_devices, mrid)

    def add_end_device(self, end_device: EndDevice) -> UsagePoint:
        """
        Associate an `EndDevice` with this `UsagePoint`

        `end_device` The `zepben.cimbend.cim.iec61968.metering.metering.EndDevice` to associate with this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if another `EndDevice` with the same `mrid` already exists for this `UsagePoint`.
        """
        if self._validate_reference(end_device, self.get_end_device, "An EndDevice"):
            return self
        self._end_devices = list() if self._end_devices is None else self._end_devices
        self._end_devices.append(end_device)
        return self

    def remove_end_device(self, end_device: EndDevice) -> UsagePoint:
        """
        Disassociate `end_device` from this `UsagePoint`.

        `end_device` The `zepben.cimbend.cim.iec61968.metering.metering.EndDevice` to disassociate from this `UsagePoint`.
        Returns A reference to this `UsagePoint` to allow fluent use.
        Raises `ValueError` if `end_device` was not associated with this `UsagePoint`.
        """
        self._end_devices = safe_remove(self._end_devices, end_device)
        return self

    def clear_end_devices(self) -> UsagePoint:
        """
        Clear all end_devices.
        Returns A reference to this `UsagePoint` to allow fluent use.
        """
        self._end_devices = None
        return self

    def is_metered(self):
        """
        Check whether this `UsagePoint` is metered. A `UsagePoint` is metered if it's associated with at least one `EndDevice`.
        Returns True if this `UsagePoint` has an `EndDevice`, False otherwise.
        """
        return nlen(self._end_devices) > 0


class Meter(EndDevice):
    """
    Physical asset that performs the metering role of the usage point. Used for measuring consumption and detection of events.
    """

    @property
    def company_meter_id(self):
        """ Returns this `Meter`s ID. Currently stored in `zepben.cimbend.cim.iec61970.base.core.identified_object.IdentifiedObject.name` """
        return self.name

    @company_meter_id.setter
    def company_meter_id(self, meter_id):
        """
        `meter_id` The ID to set for this Meter. Will use `zepben.cimbend.cim.iec61970.base.core.identified_object.IdentifiedObject.name` as a backing field.
        """
        self.name = meter_id

