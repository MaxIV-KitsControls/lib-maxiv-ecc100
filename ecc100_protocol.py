#!/usr/bin/python
# -*- coding: utf-8 -*-

##
#  Project:        ECC100 Interface
#
#  Filename:       ecc100_protocol.py
#
#  Purpose:        Control Protocol Constants for ECC100
#
#  Author:         MAXIV translated into python from N-Hands GmbH & Co KG
#
#****************************************************************************
#
#  Control Protocol Constants for ECC100
#
#  Product specific extension of the generic N-Hands device interface.
#  Defines constants to be used as parameters or parameter limits
#  for the control protocol of ucprotocol.h .
#
#

#  Maximum axis index
#
#  Most of the parameters are specific to an axis.
#  The axis is selected by the index field of the telegram.
#  It must be in the range of 0 ... ECC_AXIS_COUNT-1 .
#

ECC_AXIS_COUNT = 0x03    # Maximum number of axes

#  Output Control
#
#  The following addresses control the output data stream.
#  A synchronisation request requests an interrupt of all outputs of the
#  receiver for 2000ms to allow resynchronisation to the data stream.
#  It is valid for both directions.
#
#  To increase protocol performance some values may be sent as cyclic
#  events (Tell telegrams) by the controller.
#  The async enable telegram globally enables (value = 1) or disables (0)
#  all events. By default, events are disabled.
#

ID_SYNC_REQUEST = 0x000A   # Synchronisation request (command)
ID_ASYNC_EN = 0x0145   # Controls sending of events (bool)

#  Firmware Version
#
#  The firmware version is a 32 bit wide number which is the build date
#  coded in hex. I.e. 0x20120710 represents 2012/07/10.
#  The parameter is read-only: Get retreives the result, Set will fail.
#  Index must be 0.
#

ID_ECC_FIRMWARE_REV = 0x3038   # Firmware Version (read-only)     

#  Output Parameters
#
#  Parameters which affects the motor signal.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_OUTPUT_EN = 0x3030   # Controls the output relais of the selected axis. 1: on, 0: off
ID_ECC_AMPL = 0x3012   # Controls the amplitude of the actuator signal. Value is amplitude in mV
ID_ECC_FREQ = 0x3013   # Controls the frequency of the actuator signal. Value is frequency in mHz
ID_ECC_DC_EN = 0x3041   # Pro feature. Controls whether it is possibe to set a fixed voltage to the output. 1: on, 0: off.
ID_ECC_DC =0x3043   # Pro feature. Controls the fix output voltage in µV..

#  Position Parameters, Commands and Results
#
#  Parameters which affects the position information.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_POSITION_RESET = 0x302D   # Resets the actual position to zero and marks the reference position as invalid. Value must be 1, write i only
ID_ECC_POSITION = 0x3000   # Retrieves the current actor position. For linear type actors the position is defined in nm for goniometer an rotator type actors it is µ°. Read only.
ID_ECC_REFPOSITION = 0x3001   # Retrieves the reference position. For linear type actors the position is defined in nm for goniometer an rotator type actors it is µ°. Read only.

# Actor Selection
#
#  Parameters for actor selection and information.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
# 

class ECC_actorType:
	ECC_actorLinear = 0 # Actor is of linear type          
	ECC_actorGonio = 0 # Actor is of goniometer type 
	ECC_actorRot = 0  # Actor is of rotator type

ID_ECC_ACTOR_SEL = 0x3014   # Selects the actor to be used on selected axis from actor presets. Value determines the actor to select in the range from 0..255.
ID_ECC_AXIS_MOTORNAME_4 = 0x3003   # Name of the actual selected actor. The name consists of 20 characters each coded as a byte. This value represents the 4 characters 19..16. Read only.
ID_ECC_AXIS_MOTORNAME_3 = 0x3004   # Name of the actual selected actor. The name consists of 20 characters each coded as a byte. This value represents the 4 characters 15..12. Read only.
ID_ECC_AXIS_MOTORNAME_2 = 0x3005   # Name of the actual selected actor. The name consists of 20 characters each coded as a byte. This value represents the 4 characters 11..8. Read only.
ID_ECC_AXIS_MOTORNAME_1 = 0x3006   # Name of the actual selected actor. The name consists of 20 characters each coded as a byte. This value represents the 4 characters 7..4. Read only.
ID_ECC_AXIS_MOTORNAME_0 = 0x3007   # Name of the actual selected actor. The name consists of 20 characters each coded as a byte. This value represents the 4 characters 3..0. Read only.
ID_ECC_AXIS_TYPE = 0x3033   # Type of the actor. See @ref ECC_actorType

# Closed loop operation
#
#  Parameters for closed loop approach to a specific position.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_TARGET_POS = 0x3011   # Controls the target position for the approach function. For linear type actors the position is defined in nm for goniometer an rotator type actors it is µ°.
ID_ECC_MOVE_ABS = 0x3027   # Controls the approach of the actor to the target position. 1: enable approach, 0: Stop movement
ID_ECC_SGL_STEP_FWD = 0x3023   # Triggers a single step in forward direction. Value must be 1. Write only.
ID_ECC_SGL_STEP_BKWD = 0x3024   # Triggers a single step in backward direction. Value must be 1. Write only.
ID_ECC_CONT_FWD = 0x3025   # Controls continous movement in forward direction. A actual movement in the opposite direction is stopped. The parameter "false" stops all movement of the axis regardless its direction.
ID_ECC_CONT_BKWD = 0x3026   # Controls continous movement in backward direction. A actual movement in the opposite direction is stopped. The parameter "false" stops all movement of the axis regardless its direction.

# Parameter persistence
#
#  Commands for saving parameters to device flash.
#  All parameters belong to a specific axis,
#  The index has always to be 0.
#

ID_ECC_SAVE_USER_SETTINGS = 0x3028   # Saves user parameters to persistant flash in controller. Parameters that will be saved are amplitude, frequency and actor selection of each axis. Value must be 1.
ID_ECC_WRITING_FLASH = 0x302F   # Retrieves the status of a flah operation. While flash in progress, a read retrieves 1 otherwise 0. Read only.

#  Stati
#
#  Addresses for stati. A status will be sent by the ECC100 as an event
#  with the opcode UC_TELL whenever the status changes. A read is also possible.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_REFPOS_VALID = 0x302C   # Retrieves the status of the reference position. It may be valid or invalid (1 or 0).
ID_ECC_MOVING = 0x302E   # Retrieves the moving status. Moving means the actor is actively driven by the output stage either for approaching or continous/single stepping. 1: Moving, 0: Not moving.*/
ID_ECC_SENSOR_ERROR = 0x3031   # Retrieves the error status. Indicates a sensor malfunction. 1: Error, 0: no error.
ID_ECC_CONNECTED = 0x3002   # Retrieves the connected status. Indicates whether an actor is eletrically connected to the controller. 1: Connected, 0: Disconnected

#  Target range
#
#  Parameters of the target range feature. The ECC100 will detect when the actor is
#  in a specified target range.
#  Status will be sent as events (UC_TELL) when changing and can also be read.
#  This is a OEM feature. 
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_TARGET_RANGE = 0x3036   # OEM feature. Defines the range around the target position in which the flag target status become active. The value is nm or µ° depending on the actual actor type.
ID_ECC_TARGET_STATUS = 0x3037   # OEM feature. Retrieves the target status. Indicates whether the actual position is within the specified target range.




#End of travel detection (EOT)
#
#  Parameters of the end of travel detection.
#  Stati will be sent as events (UC_TELL) when changing and can also be read.
#  This is a Pro feature. 
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_EOT_FWD = 0x3039   # Pro Feature. Retrieves the status of the end of travel (EOT) detection in forward direction.
ID_ECC_EOT_BKWD = 0x303A   # Pro Feature. Retrieves the status of the end of travel (EOT) detection in backward direction.
ID_ECC_EOT_EN = 0x304A   # Pro feature. Defines the behavior of the output on EOT. If enabled, the output of the axis will be deactivated on positive EOT detection.

#  External interface
#
#  Parameters for the external interfaces.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_TRG_MODE = 0x3042   # Controls the input trigger for steps. 1: enable, 0: disable
ID_ECC_QUAD_IN_MODE = 0x3044   # Pro feature. Controls the AQuadB input for setpoint parameter. 1: enable 0: disable.
ID_ECC_QUAD_IN_PERIOD = 0x3045   # Pro feature. Controls the AQuadB input resolution for setpoint parameter. Value is set in nm or µ° depending on actual actor type.
ID_ECC_QUAD_OUT_MODE = 0x3046   # Pro feature. Controls the AQuadB output for position indication. 1: enable 0: disable.
ID_ECC_QUAD_OUT_PERIOD = 0x3047   # Pro feature. Controls the AQuadB output resolution for position indication. Value is set in nm or µ° depending on actual actor type.
ID_ECC_QUAD_OUT_CLOCK = 0x3048   # Pro feature. Controls the clock for AQuadB output. Clock in multiples of 20ns. Minimum 2 (40ns), maximum 65535 (1,310700ms)

#  Extended reference settings
#
#  Parameters for reference marking handling.
#  All parameters belong to a specific axis,
#  indicated by the index (0 ... ECC_MAX_AXIS-1) .
#

ID_ECC_REF_UPDATE = 0x3034   # OEM feature. When set, every time the reference marking is hit the reference position will be updated. When this function is disabled, the reference marking will be considered only the first time and after then ignored.
ID_ECC_AUTO_RESET = 0x3035   # OEM feature. When set, the position will be resetted for every time the reference position is detected.
