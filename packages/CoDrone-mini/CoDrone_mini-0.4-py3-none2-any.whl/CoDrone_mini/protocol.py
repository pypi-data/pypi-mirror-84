import abc
from abc import ABC
from struct import *
from CoDrone_mini.system import *


# ISerializable Start


class ISerializable:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getSize(self):
        pass

    @abc.abstractmethod
    def ToArray(self):
        pass


# ISerializable End


class Data:
    def __init__(self):
        self.attitude = Angle(0, 0, 0)
        self.battery = 0
        self.pressure = 0
        self.temperature = 0
        self.height = 0
        self.trim = Flight(0, 0, 0, 0)
        self.acceleration = Acceleration(0,0,0)

    def event_attitude(self, data):
        self.attitude = Angle(data.roll, data.pitch, data.yaw)

    def event_battery(self, data):
        self.battery = data.battery

    def event_altitude(self, data):
        self.pressure = data.pressure
        self.temperature = data.temperature
        self.height = data.altitude

    def event_trim(self, data):
        self.trim = Flight(data.roll, data.pitch, data.yaw, data.throttle)

    def event_motion(self, data):
        self.trim = Flight(data.accelX, data.accelY, data.accelZ)


# DataType Start
class DataType(Enum):
    None_ = 0x00

    Ping = 0x01
    Ack = 0x02
    Error = 0x03
    Request = 0x04
    Message = 0x05
    Address = 0x06
    Information = 0x07
    Update = 0x08
    UpdateLocation = 0x09
    Encrypt = 0x0A
    SystemCount = 0x0B
    SystemInformation = 0x0C
    Registration = 0x0D
    Administrator = 0x0E
    Monitor = 0x0F

    Control = 0x10
    Command = 0x11
    Pairing = 0x12
    Rssi = 0x13

    LightManual = 0x20
    LightMode = 0x21
    LightEvent = 0x22
    LightDefault = 0x23

    RawMotion = 0x30
    RawFlow = 0x31

    # 상태, 센서
    State = 0x40
    Attitude = 0x41
    Position = 0x42
    Altitude = 0x43
    Motion = 0x44
    Range = 0x45

    # 설정
    Count = 0x50
    Bias = 0x51
    Trim = 0x52
    Weight = 0x53
    LostConnection = 0x54

    # Devices
    Motor = 0x60
    MotorSingle = 0x61
    Buzzer = 0x62
    Vibrator = 0x63

    # Input
    Button = 0x70
    Joystick = 0x71

    # Information Assembled
    InformationAssembledForController = 0xA0
    InformationAssembledForEntry = 0xA1
    EndOfType = 0xDC


# DataType End


# CommandType Start
class CommandType(Enum):
    None_ = 0x00  # 없음
    Stop = 0x01  # 정지
    # 설정
    ModeControlFlight = 0x02  # 비행 제어 모드 설정
    Headless = 0x03  # 헤드리스 모드 선택
    ControlSpeed = 0x04  # 제어 속도 설정
    ClearBias = 0x05  # 자이로 바이어스 리셋(트림도 같이 초기화 됨)
    ClearTrim = 0x06  # 트림 초기화
    FlightEvent = 0x07  # 비행 이벤트 실행
    SetDefault = 0x08  # 기본 설정으로 초기화
    Backlight = 0x09  # 조종기 백라이트 설정
    # 관리자
    ClearCounter = 0xA0  # 카운터 클리어(관리자 권한을 획득했을 경우에만 동작)
    GpsRtkBase = 0xEA
    GpsRtkRover = 0xEB
    EndOfType = 0xEC


# CommandType End


# Header Start
class Header(ISerializable):
    def __init__(self, d_type=DataType.None_, h_length=0, d_from=DeviceType.None_, d_to=DeviceType.None_):
        self.dataType = d_type
        self.length = h_length
        self.from_ = d_from
        self.to_ = d_to

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<BBBB', self.dataType.value, self.length, self.from_.value, self.to_.value)

    @classmethod
    def parse(cls, dataArray):
        header = Header()

        if len(dataArray) != cls.getSize():
            return None

        header.dataType, header.length, header.from_, header.to_ = unpack('<BBBB', dataArray)
        header.dataType = DataType(header.dataType)
        header.from_ = DeviceType(header.from_)
        header.to_ = DeviceType(header.to_)

        return header


# Header End


# Common Start
class Ping(ISerializable):
    def __init__(self, _time=0):
        self.systemTime = _time

    @classmethod
    def getSize(cls):
        return 8

    def toArray(self):
        return pack('<Q', self.systemTime)

    @classmethod
    def parse(cls, dataArray):
        data = Ping()
        if len(dataArray) != cls.getSize():
            return None
        data.systemTime, = unpack('<Q', dataArray)
        return data


class Ack(ISerializable):
    def __init__(self):
        self.systemTime = 0
        self.dataType = DataType.None_
        self.crc16 = 0

    @classmethod
    def getSize(cls):
        return 11

    def toArray(self):
        return pack('<QBH', self.systemTime, self.dataType.value, self.crc16)

    @classmethod
    def parse(cls, dataArray):
        data = Ack()

        if len(dataArray) != cls.getSize():
            return None

        data.systemTime, data.dataType, data.crc16 = unpack('<QBH', dataArray)
        data.dataType = DataType(data.dataType)
        return data


class Error(ISerializable):
    def __init__(self):
        self.systemTime = 0
        self.errorFlagsForSensor = 0
        self.errorFlagsForState = 0

    @classmethod
    def getSize(cls):
        return 16

    def toArray(self):
        return pack('<QII', self.systemTime, self.errorFlagsForSensor, self.errorFlagsForState)

    @classmethod
    def parse(cls, dataArray):
        data = Error()
        if len(dataArray) != cls.getSize():
            return None
        data.systemTime, data.errorFlagsForSensor, data.errorFlagsForState = unpack('<QII', dataArray)
        return data


class Request(ISerializable):
    def __init__(self, d_type=DataType.None_):
        self.dataType = d_type

    @classmethod
    def getSize(cls):
        return 1

    def toArray(self):
        return pack('<B', self.dataType.value)

    @classmethod
    def parse(cls, dataArray):
        data = Request()
        if len(dataArray) != cls.getSize():
            return None
        data.dataType, = unpack('<B', dataArray)
        data.dataType = DataType(data.dataType)
        return data


class Message():
    def __init__(self):
        self.message = ""

    def getSize(self):
        return len(self.message)

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.message.encode('ascii', 'ignore'))
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = Message()
        if len(dataArray) == 0:
            return ""
        data.message = dataArray[0:len(dataArray)].decode()
        return data


class SystemInformation(ISerializable):

    def __init__(self):
        self.crc32bootloader = 0
        self.crc32application = 0

    @classmethod
    def getSize(cls):
        return 8

    def toArray(self):
        return pack('<II', self.crc32bootloader, self.crc32application)

    @classmethod
    def parse(cls, dataArray):
        data = SystemInformation()
        if len(dataArray) != cls.getSize():
            return None
        data.crc32bootloader, data.crc32application = unpack('<II', dataArray)
        return data


class Version(ISerializable):

    def __init__(self):
        self.build = 0
        self.minor = 0
        self.major = 0
        self.v = 0  # build, minor, major을 하나의 UInt32로 묶은 것(버젼 비교 시 사용)

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<HBB', self.build, self.minor, self.major)

    @classmethod
    def parse(cls, dataArray):
        data = Version()
        if len(dataArray) != cls.getSize():
            return None
        data.v, = unpack('<I', dataArray)
        data.build, data.minor, data.major = unpack('<HBB', dataArray)
        return data


class Information(ISerializable):
    def __init__(self):
        self.modeUpdate = ModeUpdate.None_
        self.modelNumber = ModelNumber.None_
        self.version = Version()
        self.year = 0
        self.month = 0
        self.day = 0

    @classmethod
    def getSize(cls):
        return 13

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(pack('<B', self.modeUpdate.value))
        dataArray.extend(pack('<I', self.modelNumber.value))
        dataArray.extend(self.version.toArray())
        dataArray.extend(pack('<H', self.year))
        dataArray.extend(pack('<B', self.month))
        dataArray.extend(pack('<B', self.day))
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = Information()
        if len(dataArray) != cls.getSize():
            return None
        data.modeUpdate = unpack('<B', dataArray[0:1])
        data.modelNumber = unpack('<I', dataArray[1:5])
        data.version = Version.parse(dataArray[5:9])
        data.year = unpack('<H', dataArray[9:11])
        data.month = unpack('<B', dataArray[11:12])
        data.day = unpack('<B', dataArray[12:13])
        data.modeUpdate = ModeUpdate(data.modeUpdate)
        data.modelNumber = ModelNumber(data.modelNumber)
        return data


class UpdateLocation(ISerializable):
    def __init__(self):
        self.indexBlockNext = 0

    @classmethod
    def getSize(cls):
        return 2

    def toArray(self):
        return pack('<H', self.indexBlockNext)

    @classmethod
    def parse(cls, dataArray):
        data = UpdateLocation()
        if len(dataArray) != cls.getSize():
            return None
        data.indexBlockNext, = unpack('<H', dataArray)
        return data


class Address(ISerializable):
    def __init__(self):
        self.address = bytearray()

    @classmethod
    def getSize(cls):
        return 16

    def toArray(self):
        return self.address

    @classmethod
    def parse(cls, dataArray):
        data = Address()
        if len(dataArray) != cls.getSize():
            return None
        data.address = dataArray[0:16]
        return data


class RegistrationInformation(ISerializable):
    def __init__(self):
        self.address = bytearray()
        self.year = 0
        self.month = 0
        self.key = 0
        self.flagValid = 0

    @classmethod
    def getSize(cls):
        return 21

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.address)
        dataArray.extend(pack('<HBB?', self.year, self.month, self.key, self.flagValid))
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = RegistrationInformation()
        if len(dataArray) != cls.getSize():
            return None
        data.address = dataArray[0:16]
        data.year, data.month, data.key, data.flagValid = unpack('<HBB?', dataArray[16:21])
        return data


class Pairing(ISerializable):
    def __init__(self, address0=0, address1=0, address2=0, scramble=0, channel0=0, channel1=0, channel2=0, channel3=0):
        self.address0 = address0
        self.address1 = address1
        self.address2 = address2
        self.scramble = scramble
        self.channel0 = channel0
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3

    @classmethod
    def getSize(cls):
        return 11

    def toArray(self):
        return pack('<HHHBBBBB', self.address0, self.address1, self.address2,
                    self.scramble, self.channel0, self.channel1, self.channel2, self.channel3)

    @classmethod
    def parse(cls, dataArray):
        data = Pairing()
        if len(dataArray) != cls.getSize():
            return None

        data.address0, data.address1, \
        data.address2, data.scramble, \
        data.channel0, data.channel1, \
        data.channel2, data.channel3 = unpack('<HHHBBBBB', dataArray)
        return data


class Rssi(ISerializable):
    def __init__(self):
        self.rssi = 0

    @classmethod
    def getSize(cls):
        return 1

    def toArray(self):
        return pack('<b', self.rssi)

    @classmethod
    def parse(cls, dataArray):
        data = Rssi()
        if len(dataArray) != cls.getSize():
            return None
        data.rssi, = unpack('<b', dataArray)
        return data


class Command(ISerializable):
    def __init__(self, commandType=CommandType.None_, option=0):
        self.commandType = commandType
        self.option = option

    @classmethod
    def getSize(cls):
        return 2

    def toArray(self):
        return pack('<BB', self.commandType.value, self.option)

    @classmethod
    def parse(cls, dataArray):
        data = Command()
        if len(dataArray) != cls.getSize():
            return None
        data.commandType, data.option = unpack('<BB', dataArray)
        data.commandType = CommandType(data.commandType)
        return data


class CommandLightEvent(ISerializable):
    def __init__(self):
        self.command = Command()
        self.event = LightEvent()

    @classmethod
    def getSize(cls):
        return Command.getSize() + LightEvent.getSize()

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.command.toArray())
        dataArray.extend(self.event.toArray())
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = CommandLightEvent()
        if len(dataArray) != cls.getSize():
            return None
        cmd_size = Command.getSize()
        light_size = LightEvent.getSize()
        data.command = Command.parse(dataArray[0:cmd_size])
        data.event = LightEvent.parse(dataArray[cmd_size:light_size])

        return data


class CommandLightEventColor(ISerializable):
    def __init__(self):
        self.command = Command()
        self.event = LightEvent()
        self.color = Color()

    @classmethod
    def getSize(cls):
        return Command.getSize() + LightEvent.getSize() + Color.getSize()

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.command.toArray())
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = CommandLightEventColor()

        if len(dataArray) != cls.getSize():
            return None

        cmd_size = Command.getSize()
        l_event_size = LightEvent.getSize()
        l_color_size = Color.getSize()
        data.command = Command.parse(dataArray[0:cmd_size])
        data.event = LightEvent.parse(dataArray[cmd_size:cmd_size + l_event_size])
        data.color = Color.parse(dataArray[cmd_size + l_event_size:cmd_size + l_event_size + l_color_size])

        return data


class CommandLightEventColors(ISerializable):

    def __init__(self):
        self.command = Command()
        self.event = LightEvent()
        self.colors = Colors.Black

    @classmethod
    def getSize(cls):
        return Command.getSize() + LightEvent.getSize() + 1

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.command.toArray())
        dataArray.extend(self.event.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = Command()
        if len(dataArray) != cls.getSize():
            return None
        cmd_size = Command.getSize()
        l_event_size = LightEvent.getSize()
        l_colors_size = 1
        data.command = Command.parse(dataArray[0:cmd_size])
        data.event = LightEvent.parse(dataArray[cmd_size:cmd_size + l_event_size])
        data.colors = Colors(unpack('<B', dataArray[cmd_size + l_event_size:cmd_size + l_event_size + l_colors_size]))
        return data


# Common End

#
#
# # Monitor Start
#
#
# class MonitorHeaderType(Enum):
#
#     Monitor0            = 0x00
#     Monitor4            = 0x01
#     Monitor8            = 0x02
#
#     EndOfType           = 0x03
#
#
#
# class MonitorDataType(Enum):
#
#     U8          = 0x00,
#     S8          = 0x01,
#     U16         = 0x02,
#     S16         = 0x03,
#     U32         = 0x04,
#     S32         = 0x05,
#     U64         = 0x06,
#     S64         = 0x07,
#     F32         = 0x08,
#     F64         = 0x09,
#
#     EndOfType   = 0x0A
#
#
#
# class MonitorType(ISerializable):
#
#     def __init__(self):
#         self.monitorHeaderType    = MonitorHeaderType.Monitor8
#
#
#     @classmethod
#     def getSize(cls):
#         return 1
#
#
#     def toArray(self):
#         return pack('<B', self.monitorHeaderType.value)
#
#
#     @classmethod
#     def parse(cls, dataArray):
#         data = MonitorType()
#
#         if len(dataArray) != cls.getSize():
#             return None
#
#         data.monitorHeaderType, = unpack('<B', dataArray)
#
#         data.monitorHeaderType  = MonitorHeaderType(data.monitorHeaderType)
#
#         return data
#
#
#
# class Monitor0(ISerializable):
#
#     def __init__(self):
#         self.monitorDataType        = MonitorDataType.F32
#         self.index                  = 0
#
#
#     @classmethod
#     def getSize(cls):
#         return 2
#
#
#     def toArray(self):
#         return pack('<BB', self.monitorDataType.value, self.index)
#
#
#     @classmethod
#     def parse(cls, dataArray):
#         data = Monitor0()
#
#         if len(dataArray) != cls.getSize():
#             return None
#
#         data.monitorDataType, data.index = unpack('<BB', dataArray)
#
#         data.monitorDataType  = MonitorDataType(data.monitorDataType)
#
#         return data
#
#
#
# class Monitor4(ISerializable):
#
#     def __init__(self):
#         self.systemTime             = 0
#         self.monitorDataType        = MonitorDataType.F32
#         self.index                  = 0
#
#
#     @classmethod
#     def getSize(cls):
#         return 6
#
#
#     def toArray(self):
#         return pack('<IBB', self.systemTime, self.monitorDataType.value, self.index)
#
#
#     @classmethod
#     def parse(cls, dataArray):
#         data = Monitor4()
#
#         if len(dataArray) != cls.getSize():
#             return None
#
#         data.systemTime, data.monitorDataType, data.index = unpack('<IBB', dataArray)
#
#         data.monitorDataType  = MonitorDataType(data.monitorDataType)
#
#         return data
#
#
#
# class Monitor8(ISerializable):
#
#     def __init__(self):
#         self.systemTime             = 0
#         self.monitorDataType        = MonitorDataType.F32
#         self.index                  = 0
#
#
#     @classmethod
#     def getSize(cls):
#         return 10
#
#
#     def toArray(self):
#         return pack('<QBB', self.systemTime, self.monitorDataType.value, self.index)
#
#
#     @classmethod
#     def parse(cls, dataArray):
#         data = Monitor8()
#
#         if len(dataArray) != cls.getSize():
#             return None
#
#         data.systemTime, data.monitorDataType, data.index = unpack('<QBB', dataArray)
#
#         data.monitorDataType  = MonitorDataType(data.monitorDataType)
#
#         return data
#
#
#
# # Monitor End
#
#

# Control Start


class ControlQuad8(ISerializable):
    def __init__(self, _roll=0, _pitch=0, _yaw=0, _throttle=0):
        self.roll = _roll
        self.pitch = _pitch
        self.yaw = _yaw
        self.throttle = _throttle

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<bbbb', self.roll, self.pitch, self.yaw, self.throttle)

    @classmethod
    def parse(cls, dataArray):
        data = ControlQuad8()
        if len(dataArray) != cls.getSize():
            return None
        data.roll, data.pitch, data.yaw, data.throttle = unpack('<bbbb', dataArray)
        return data


class ControlWithRequestSensor(ISerializable, ABC):
    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.throttle = 0
        self.dataType = DataType.None_

    @classmethod
    def getSize(cls):
        return 5

    def toArray(self):
        return pack('<bbbbb', self.roll, self.pitch, self.yaw, self.throttle, self.dataType)

    @classmethod
    def parse(cls, dataArray):
        data = ControlWithRequestSensor()
        if len(dataArray) != cls.getSize():
            return None
        data.roll, data.pitch, data.yaw, data.throttle, data.dataType = unpack('<bbbbb', dataArray)
        data.dataType = DataType(data.dataType)
        return data


# Control End


# Light Start
class LightModeDrone(Enum):
    None_ = 0x00
    BodyNone = 0x20
    BodyManual = 0x21  # 수동 제어
    BodyHold = 0x22  # 지정한 색상을 계속 켬
    BodyFlicker = 0x23  # 깜빡임
    BodyFlickerDouble = 0x24  # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    BodyDimming = 0x25  # 밝기 제어하여 천천히 깜빡임
    BodySunrise = 0x26
    BodySunset = 0x27
    EndOfType = 0x56


class LightModeController(Enum):
    None_ = 0x00
    BodyNone = 0x10
    BodyManual = 0x11  # 수동 조작
    BodyHold = 0x12
    BodyFlicker = 0x13
    BodyFlickerDouble = 0x14
    BodyDimming = 0x15
    EndOfType = 0x16


class Color(ISerializable, ABC):
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    @classmethod
    def getSize(cls):
        return 3

    def toArray(self):
        return pack('<BBB', self.r, self.g, self.b)

    @classmethod
    def parse(cls, dataArray):
        data = Color()
        if len(dataArray) != cls.getSize():
            return None
        data.r, data.g, data.b = unpack('<BBB', dataArray)
        return data


class LightMode(ISerializable):
    def __init__(self):
        self.mode = 0
        self.interval = 0

    @classmethod
    def getSize(cls):
        return 3

    def toArray(self):
        return pack('<BH', self.mode, self.interval)

    @classmethod
    def parse(cls, dataArray):
        data = LightMode()
        if len(dataArray) != cls.getSize():
            return None
        data.mode, data.interval = unpack('<BH', dataArray)
        return data


class LightEvent(ISerializable):

    def __init__(self):
        self.event = 0
        self.interval = 0
        self.repeat = 0

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<BHB', self.event, self.interval, self.repeat)

    @classmethod
    def parse(cls, dataArray):
        data = LightEvent()
        if len(dataArray) != cls.getSize():
            return None
        data.event, data.interval, data.repeat = unpack('<BHB', dataArray)
        return data


class LightModeColor(ISerializable):
    def __init__(self):
        self.mode = LightMode()
        self.color = Color()

    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Color.getSize()

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = LightModeColor()

        if len(dataArray) != cls.getSize():
            return None

        data.mode = LightMode.parse(dataArray[0:3])
        data.color = Color.parse(dataArray[3:6])
        return data

# Light End


# Buzzer Start
class BuzzerMode(Enum):
    Stop = 0  # 정지(Mode에서의 Stop은 통신에서 받았을 때 Buzzer를 끄는 용도로 사용, set으로만 호출)
    Mute = 1  # 묵음 즉시 적용
    MuteReserve = 2  # 묵음 예약
    Scale = 3  # 음계 즉시 적용
    ScaleReserve = 4  # 음계 예약
    Hz = 5  # 주파수 즉시 적용
    HzReserve = 6  # 주파수 예약
    EndOfType = 7


class Note(Enum):
    C3 = 0x18
    CS3 = 0x19
    D3 = 0x1A
    DS3 = 0x1B
    E3 = 0x1C
    F3 = 0x1D
    FS3 = 0x1E
    G3 = 0x1F
    GS3 = 0x20
    A3 = 0x21
    AS3 = 0x22
    B3 = 0x23
    C4 = 0x24
    CS4 = 0x25
    D4 = 0x26
    DS4 = 0x27
    E4 = 0x28
    F4 = 0x29
    FS4 = 0x2A
    G4 = 0x2B
    GS4 = 0x2C
    A4 = 0x2D
    AS4 = 0x2E
    B4 = 0x2F
    C5 = 0x30
    CS5 = 0x31
    D5 = 0x32
    DS5 = 0x33
    E5 = 0x34
    F5 = 0x35
    FS5 = 0x36
    G5 = 0x37
    GS5 = 0x38
    A5 = 0x39
    AS5 = 0x3A
    B5 = 0x3B
    C6 = 0x3C
    CS6 = 0x3D
    D6 = 0x3E
    DS6 = 0x3F
    E6 = 0x40
    F6 = 0x41
    FS6 = 0x42
    G6 = 0x43
    GS6 = 0x44
    A6 = 0x45
    AS6 = 0x46
    B6 = 0x47
    C7 = 0x48
    CS7 = 0x49
    D7 = 0x4A
    DS7 = 0x4B
    E7 = 0x4C
    F7 = 0x4D
    FS7 = 0x4E
    G7 = 0x4F
    GS7 = 0x50
    A7 = 0x51
    AS7 = 0x52
    B7 = 0x53

    EndOfType = 0x60
    Mute = 0xEE  # 묵음
    Fin = 0xFF  # 악보의 끝


class Buzzer(ISerializable):
    def __init__(self):
        self.mode = BuzzerMode.Stop
        self.value = 0
        self.time = 0

    @classmethod
    def getSize(cls):
        return 5

    def toArray(self):
        return pack('<BHH', self.mode.value, self.value, self.time)

    @classmethod
    def parse(cls, dataArray):
        data = Buzzer()
        if len(dataArray) != cls.getSize():
            return None
        data.mode, data.value, data.time = unpack('<BHH', dataArray)
        data.mode = BuzzerMode(data.mode)
        return data


# Buzzer End


# Button Start
class ButtonFlagController(Enum):
    None_ = 0x0000
    FrontLeftTop = 0x0001
    FrontLeftBottom = 0x0002
    FrontRightTop = 0x0004
    FrontRightBottom = 0x0008
    TopLeft = 0x0010
    TopRight = 0x0020  # POWER ON/OFF
    MidUp = 0x0040
    MidLeft = 0x0080
    MidRight = 0x0100
    MidDown = 0x0200
    BottomLeft = 0x0400
    BottomRight = 0x0800


class ButtonFlagDrone(Enum):
    None_ = 0x0000
    Reset = 0x0001


class ButtonEvent(Enum):
    None_ = 0x00
    Down = 0x01
    Press = 0x02
    Up = 0x03
    EndContinuePress = 0x04


class Button(ISerializable):
    def __init__(self):
        self.button = 0
        self.event = ButtonEvent.None_

    @classmethod
    def getSize(cls):
        return 3

    def toArray(self):
        return pack('<HB', self.button, self.event.value)

    @classmethod
    def parse(cls, dataArray):
        data = Button()
        if len(dataArray) != cls.getSize():
            return None
        data.button, data.event = unpack('<HB', dataArray)
        data.event = ButtonEvent(data.event)
        return data


# Button End


# Joystick Start
class JoystickDirection(Enum):
    None_ = 0  # 정의하지 않은 영역(무시함)

    VT = 0x10  # 위(세로)
    VM = 0x20  # 중앙(세로)
    VB = 0x40  # 아래(세로)

    HL = 0x01  # 왼쪽(가로)
    HM = 0x02  # 중앙(가로)
    HR = 0x04  # 오른쪽(가로)

    TL = 0x11
    TM = 0x12
    TR = 0x14
    ML = 0x21
    CN = 0x22
    MR = 0x24
    BL = 0x41
    BM = 0x42
    BR = 0x44


class JoystickEvent(Enum):
    None_ = 0  # 이벤트 없음

    In = 1  # 특정 영역에 진입
    Stay = 2  # 특정 영역에서 상태 유지
    Out = 3  # 특정 영역에서 벗어남

    EndOfType = 4


class JoystickBlock(ISerializable):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = JoystickDirection.None_
        self.event = JoystickEvent.None_

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<bbBB', self.x, self.y, self.direction.value, self.event.value)

    @classmethod
    def parse(cls, dataArray):
        data = JoystickBlock()

        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.direction, data.event = unpack('<bbBB', dataArray)

        data.direction = JoystickDirection(data.direction)
        data.event = JoystickEvent(data.event)

        return data


class Joystick(ISerializable):

    def __init__(self):
        self.left = JoystickBlock()
        self.right = JoystickBlock()

    @classmethod
    def getSize(cls):
        return JoystickBlock().getSize() * 2

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.left.toArray())
        dataArray.extend(self.right.toArray())
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = Joystick()

        if len(dataArray) != cls.getSize():
            return None

        indexStart = 0
        indexEnd = JoystickBlock.getSize()
        data.left = JoystickBlock.parse(dataArray[indexStart:indexEnd])
        indexStart = indexEnd
        indexEnd += JoystickBlock.getSize()
        data.right = JoystickBlock.parse(dataArray[indexStart:indexEnd])

        return data


# Joystick End


# Sensor Raw Start


class RawMotion(ISerializable):

    def __init__(self):
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.gyroRoll = 0
        self.gyroPitch = 0
        self.gyroYaw = 0

    @classmethod
    def getSize(cls):
        return 12

    def toArray(self):
        return pack('<hhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw)

    @classmethod
    def parse(cls, dataArray):
        data = RawMotion()

        if len(dataArray) != cls.getSize():
            return None

        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw = unpack('<hhhhhh',
                                                                                                    dataArray)

        return data


class RawFlow(ISerializable):

    def __init__(self):
        self.x = 0
        self.y = 0

    @classmethod
    def getSize(cls):
        return 8

    def toArray(self):
        return pack('<ff', self.x, self.y)

    @classmethod
    def parse(cls, dataArray):
        data = RawFlow()

        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y = unpack('<ff', dataArray)

        return data


# Sensor Raw End


# Information Start


class State(ISerializable):

    def __init__(self):
        self.modeSystem = ModeSystem.None_
        self.modeFlight = ModeFlight.None_
        self.modeControlFlight = ModeControlFlight.None_
        self.modeMovement = ModeMovement.None_
        self.headless = Headless.None_
        self.controlSpeed = 0
        self.sensorOrientation = SensorOrientation.None_
        self.battery = 0

    @classmethod
    def getSize(cls):
        return 8

    def toArray(self):
        return pack('<BBBBBBBB', self.modeSystem.value, self.modeFlight.value, self.modeControlFlight.value,
                    self.modeMovement.value, self.headless.value, self.controlSpeed, self.sensorOrientation.value,
                    self.battery)

    @classmethod
    def parse(cls, dataArray):
        data = State()

        if len(dataArray) != cls.getSize():
            return None

        data.modeSystem, data.modeFlight, data.modeControlFlight, data.modeMovement, data.headless, data.controlSpeed, data.sensorOrientation, data.battery = unpack(
            '<BBBBBBBB', dataArray)

        data.modeSystem = ModeSystem(data.modeSystem)
        data.modeFlight = ModeFlight(data.modeFlight)
        data.modeControlFlight = ModeControlFlight(data.modeControlFlight)
        data.modeMovement = ModeMovement(data.modeMovement)
        data.headless = Headless(data.headless)
        data.sensorOrientation = SensorOrientation(data.sensorOrientation)

        return data


class Attitude(ISerializable):

    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    @classmethod
    def getSize(cls):
        return 6

    def toArray(self):
        return pack('<hhh', self.roll, self.pitch, self.yaw)

    @classmethod
    def parse(cls, dataArray):
        data = Attitude()

        if len(dataArray) != cls.getSize():
            return None

        data.roll, data.pitch, data.yaw = unpack('<hhh', dataArray)

        return data


class Position(ISerializable):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    @classmethod
    def getSize(cls):
        return 12

    def toArray(self):
        return pack('<fff', self.x, self.y, self.z)

    @classmethod
    def parse(cls, dataArray):
        data = Position()

        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.z = unpack('<fff', dataArray)

        return data


class Altitude(ISerializable):

    def __init__(self):
        self.temperature = 0
        self.pressure = 0
        self.altitude = 0
        self.rangeHeight = 0

    @classmethod
    def getSize(cls):
        return 16

    def toArray(self):
        return pack('<ffff', self.temperature, self.pressure, self.altitude, self.rangeHeight)

    @classmethod
    def parse(cls, dataArray):
        data = Altitude()

        if len(dataArray) != cls.getSize():
            return None

        data.temperature, data.pressure, data.altitude, data.rangeHeight = unpack('<ffff', dataArray)

        return data


class Motion(ISerializable):

    def __init__(self):
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.gyroRoll = 0
        self.gyroPitch = 0
        self.gyroYaw = 0
        self.angleRoll = 0
        self.anglePitch = 0
        self.angleYaw = 0

    @classmethod
    def getSize(cls):
        return 18

    def toArray(self):
        return pack('<hhhhhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw,
                    self.angleRoll, self.anglePitch, self.angleYaw)

    @classmethod
    def parse(cls, dataArray):
        data = Motion()

        if len(dataArray) != cls.getSize():
            return None

        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw, data.angleRoll, data.anglePitch, data.angleYaw = unpack(
            '<hhhhhhhhh', dataArray)

        return data


class Range(ISerializable):

    def __init__(self):
        self.left = 0
        self.front = 0
        self.right = 0
        self.rear = 0
        self.top = 0
        self.bottom = 0

    @classmethod
    def getSize(cls):
        return 12

    def toArray(self):
        return pack('<hhhhhh', self.left, self.front, self.right, self.rear, self.top, self.bottom)

    @classmethod
    def parse(cls, dataArray):
        data = Range()

        if len(dataArray) != cls.getSize():
            return None

        data.left, data.front, data.right, data.rear, data.top, data.bottom = unpack('<hhhhhh', dataArray)

        return data


class Trim(ISerializable):

    def __init__(self):
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.throttle = 0

    @classmethod
    def getSize(cls):
        return 8

    def toArray(self):
        return pack('<hhhh', self.roll, self.pitch, self.yaw, self.throttle)

    @classmethod
    def parse(cls, dataArray):
        data = Trim()

        if len(dataArray) != cls.getSize():
            return None

        data.roll, data.pitch, data.yaw, data.throttle = unpack('<hhhh', dataArray)

        return data


# Information End


# Sensor Start


class Vector(ISerializable):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    @classmethod
    def getSize(cls):
        return 6

    def toArray(self):
        return pack('<hhh', self.x, self.y, self.z)

    @classmethod
    def parse(cls, dataArray):
        data = Vector()

        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.z = unpack('<hhh', dataArray)

        return data


class Count(ISerializable):

    def __init__(self):
        self.timeFlight = 0

        self.countTakeOff = 0
        self.countLanding = 0
        self.countAccident = 0

    @classmethod
    def getSize(cls):
        return 14

    def toArray(self):
        return pack('<QHHH', self.timeFlight, self.countTakeOff, self.countLanding, self.countAccident)

    @classmethod
    def parse(cls, dataArray):
        data = Count()

        if len(dataArray) != cls.getSize():
            return None

        data.timeFlight, data.countTakeOff, data.countLanding, data.countAccident = unpack('<QHHH', dataArray)

        return data


class Bias(ISerializable):

    def __init__(self):
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.gyroRoll = 0
        self.gyroPitch = 0
        self.gyroYaw = 0

    @classmethod
    def getSize(cls):
        return 12

    def toArray(self):
        return pack('<hhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw)

    @classmethod
    def parse(cls, dataArray):
        data = Bias()

        if len(dataArray) != cls.getSize():
            return None

        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw = unpack('<hhhhhh',
                                                                                                    dataArray)

        return data


class Weight(ISerializable):

    def __init__(self):
        self.weight = 0

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<f', self.weight)

    @classmethod
    def parse(cls, dataArray):
        data = Weight()

        if len(dataArray) != cls.getSize():
            return None

        data.weight, = unpack('<f', dataArray)

        return data


class LostConnection(ISerializable):

    def __init__(self):
        self.timeNeutral = 0
        self.timeLanding = 0
        self.timeStop = 0

    @classmethod
    def getSize(cls):
        return 8

    def toArray(self):
        return pack('<HHI', self.timeNeutral, self.timeLanding, self.timeStop)

    @classmethod
    def parse(cls, dataArray):
        data = LostConnection()

        if len(dataArray) != cls.getSize():
            return None

        data.timeNeutral, data.timeLanding, data.timeStop = unpack('<HHI', dataArray)

        return data


# Sensor End


# Device Start


class MotorBlock(ISerializable):

    def __init__(self):
        self.rotation = Rotation.None_
        self.value = 0

    @classmethod
    def getSize(cls):
        return 3

    def toArray(self):
        return pack('<Bh', self.rotation.value, self.value)

    @classmethod
    def parse(cls, dataArray):
        data = MotorBlock()

        if len(dataArray) != cls.getSize():
            return None

        data.rotation, data.value = unpack('<Bh', dataArray)
        data.rotation = Rotation(data.rotation)

        return data


class Motor(ISerializable):

    def __init__(self):
        self.motor = []
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())

    @classmethod
    def getSize(cls):
        return MotorBlock.getSize() * 4

    def toArray(self):
        dataArray = bytearray()
        dataArray.extend(self.motor[0].toArray())
        dataArray.extend(self.motor[1].toArray())
        dataArray.extend(self.motor[2].toArray())
        dataArray.extend(self.motor[3].toArray())
        return dataArray

    @classmethod
    def parse(cls, dataArray):
        data = Motor()

        if len(dataArray) != cls.getSize():
            return None

        for index in range(4):
            data.motor[index] = MotorBlock.parse(dataArray[index * 3:index * 3 + 3])

        return data


class MotorSingle(ISerializable):

    def __init__(self):
        self.target = 0
        self.rotation = Rotation.None_
        self.value = 0

    @classmethod
    def getSize(cls):
        return 4

    def toArray(self):
        return pack('<BBh', self.target, self.rotation.value, self.value)

    @classmethod
    def parse(cls, dataArray):
        data = MotorSingle()

        if len(dataArray) != cls.getSize():
            return None

        data.target, data.rotation, data.value = unpack('<BBh', dataArray)
        data.rotation = Rotation(data.rotation)

        return data


class InformationAssembledForController(ISerializable):

    def __init__(self):
        self.angleRoll = 0
        self.anglePitch = 0
        self.angleYaw = 0

        self.rpm = 0

        self.positionX = 0
        self.positionY = 0
        self.positionZ = 0

        self.speedX = 0
        self.speedY = 0

        self.rangeHeight = 0

        self.rssi = 0

    @classmethod
    def getSize(cls):
        return 18

    def toArray(self):
        return pack('<hhhHhhhbbBb', self.angleRoll, self.anglePitch, self.angleYaw,
                    self.rpm,
                    self.positionX, self.positionY, self.positionZ,
                    self.speedX, self.speedY,
                    self.rangeHeight,
                    self.rssi)

    @classmethod
    def parse(cls, dataArray):
        data = InformationAssembledForController()

        if len(dataArray) != cls.getSize():
            return None

        (data.angleRoll, data.anglePitch, data.angleYaw,
         data.rpm,
         data.positionX, data.positionY, data.positionZ,
         data.speedX, data.speedY,
         data.rangeHeight,
         data.rssi) = unpack('<hhhHhhhbbBb', dataArray)

        return data


class InformationAssembledForEntry(ISerializable):

    def __init__(self):
        self.angleRoll = 0
        self.anglePitch = 0
        self.angleYaw = 0

        self.positionX = 0
        self.positionY = 0
        self.positionZ = 0

        self.rangeHeight = 0
        self.altitude = 0

    @classmethod
    def getSize(cls):
        return 18

    def toArray(self):
        return pack('<hhhhhhhf', self.angleRoll, self.anglePitch, self.angleYaw,
                    self.positionX, self.positionY, self.positionZ,
                    self.rangeHeight, self.altitude)

    @classmethod
    def parse(cls, dataArray):
        data = InformationAssembledForEntry()

        if len(dataArray) != cls.getSize():
            return None

        (data.angleRoll, data.anglePitch, data.angleYaw,
         data.positionX, data.positionY, data.positionZ,
         data.rangeHeight, data.altitude) = unpack('<hhhhhhhf', dataArray)

        return data

# Device End
