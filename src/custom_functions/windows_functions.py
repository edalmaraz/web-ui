"""
Windows System Control Functions
Note: These functions are powerful and should be used with caution
"""

import os
import sys
import json
import psutil
import winreg
import win32api
import win32con
import win32gui
import win32process
from typing import List, Dict, Any, Optional
from browser_use.agent.views import ActionResult
from .function_registry import registry
from ..safety.function_control import function_control


@registry.register("Get System Info")
async def get_system_info() -> ActionResult:
    """Get system information"""
    info = {
        "os": sys.platform,
        "python_version": sys.version,
        "cpu_count": psutil.cpu_count(),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": dict(psutil.disk_usage("/")._asdict()),
    }
    return ActionResult(extracted_content=json.dumps(info))


@registry.register("List Running Processes")
async def list_running_processes() -> ActionResult:
    """List all running processes"""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return ActionResult(extracted_content=json.dumps(processes))


@registry.register("Get Window Info")
async def get_window_info(window_title: str) -> ActionResult:
    """Get information about a specific window"""

    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title.lower() in title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                windows.append(
                    {"handle": hwnd, "title": title, "rect": rect, "pid": pid}
                )

    windows = []
    win32gui.EnumWindows(callback, windows)
    return ActionResult(extracted_content=json.dumps(windows))


@registry.register("Get Display Settings")
async def get_display_settings() -> ActionResult:
    """Get current display settings"""
    settings = {
        "resolution": (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)),
        "dpi": win32gui.GetDpiForSystem(),
        "monitors": [],
    }

    def callback(monitor, dc, rect, data):
        settings["monitors"].append(
            {"handle": str(monitor), "rect": (rect[0], rect[1], rect[2], rect[3])}
        )
        return True

    win32gui.EnumDisplayMonitors(None, None, callback, None)
    return ActionResult(extracted_content=json.dumps(settings))


@registry.register("Get Power Status")
async def get_power_status() -> ActionResult:
    """Get system power status"""
    battery = psutil.sensors_battery()
    status = {
        "battery_percent": battery.percent if battery else None,
        "power_plugged": battery.power_plugged if battery else None,
        "battery_time_left": battery.secsleft if battery else None,
    }
    return ActionResult(extracted_content=json.dumps(status))


@registry.register("Get Network Info")
async def get_network_info() -> ActionResult:
    """Get network information"""
    info = {
        "interfaces": psutil.net_if_addrs(),
        "connections": psutil.net_connections(),
        "stats": psutil.net_if_stats(),
    }
    return ActionResult(extracted_content=json.dumps(info))


@registry.register("Get Drive Info")
async def get_drive_info() -> ActionResult:
    """Get information about system drives"""
    drives = []
    for part in psutil.disk_partitions():
        usage = psutil.disk_usage(part.mountpoint)
        drives.append(
            {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "usage": dict(usage._asdict()),
            }
        )
    return ActionResult(extracted_content=json.dumps(drives))


@registry.register("Get Audio Devices")
async def get_audio_devices() -> ActionResult:
    """Get list of audio devices"""
    import sounddevice as sd

    devices = sd.query_devices()
    return ActionResult(extracted_content=json.dumps(devices))


@registry.register("Get Installed Software")
async def get_installed_software() -> ActionResult:
    """Get list of installed software"""
    software = []

    def get_software_from_key(key_path):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            i = 0
            while True:
                try:
                    name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, name)
                    try:
                        display_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        display_version = winreg.QueryValueEx(
                            sub_key, "DisplayVersion"
                        )[0]
                        publisher = winreg.QueryValueEx(sub_key, "Publisher")[0]
                        software.append(
                            {
                                "name": display_name,
                                "version": display_version,
                                "publisher": publisher,
                            }
                        )
                    except WindowsError:
                        pass
                    finally:
                        winreg.CloseKey(sub_key)
                    i += 1
                except WindowsError:
                    break
            winreg.CloseKey(key)
        except WindowsError:
            pass

    get_software_from_key(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    get_software_from_key(
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    )

    return ActionResult(extracted_content=json.dumps(software))


@registry.register("Get System Events")
async def get_system_events(num_events: int = 100) -> ActionResult:
    """Get recent system events"""
    import win32evtlog

    events = []

    server = "localhost"
    logtype = "System"
    hand = win32evtlog.OpenEventLog(server, logtype)
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    events_read = 0
    while events_read < num_events:
        events_list = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events_list:
            break

        for event in events_list:
            events.append(
                {
                    "timestamp": str(event.TimeGenerated),
                    "source": event.SourceName,
                    "type": event.EventType,
                    "category": event.EventCategory,
                    "event_id": event.EventID,
                }
            )
            events_read += 1
            if events_read >= num_events:
                break

    win32evtlog.CloseEventLog(hand)
    return ActionResult(extracted_content=json.dumps(events))


@registry.register("Get Clipboard Content")
async def get_clipboard_content() -> ActionResult:
    """Get current clipboard content"""
    import win32clipboard

    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            return ActionResult(extracted_content=data.decode("utf-8"))
        elif win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            return ActionResult(extracted_content=data)
        else:
            return ActionResult(extracted_content="No text content in clipboard")
    finally:
        win32clipboard.CloseClipboard()


@registry.register("Get System Performance")
async def get_system_performance() -> ActionResult:
    """Get system performance metrics"""
    performance = {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1, percpu=True),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "stats": psutil.cpu_stats()._asdict(),
            "times": psutil.cpu_times()._asdict(),
        },
        "memory": psutil.virtual_memory()._asdict(),
        "swap": psutil.swap_memory()._asdict(),
        "disk_io": (
            psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
        ),
        "network_io": psutil.net_io_counters()._asdict(),
    }
    return ActionResult(extracted_content=json.dumps(performance))


# Note: The following functions are disabled by default for safety
# They can be enabled through the function control system


@registry.register("Set Window Position")
async def set_window_position(
    window_title: str, x: int, y: int, width: int, height: int
) -> ActionResult:
    """Set position and size of a window"""
    if not function_control.is_function_allowed("Set Window Position"):
        return ActionResult(error="Function is disabled")

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if window_title.lower() in title.lower():
                win32gui.MoveWindow(hwnd, x, y, width, height, True)

    win32gui.EnumWindows(callback, None)
    return ActionResult(extracted_content="Window position updated")


@registry.register("Set Display Resolution")
async def set_display_resolution(width: int, height: int) -> ActionResult:
    """Set display resolution"""
    if not function_control.is_function_allowed("Set Display Resolution"):
        return ActionResult(error="Function is disabled")

    import win32api
    import win32con
    import pywintypes

    try:
        devmode = pywintypes.DEVMODEType()
        devmode.PelsWidth = width
        devmode.PelsHeight = height
        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

        win32api.ChangeDisplaySettings(devmode, 0)
        return ActionResult(extracted_content="Display resolution updated")
    except Exception as e:
        return ActionResult(error=str(e))


@registry.register("Control Audio")
async def control_audio(volume: int, mute: bool = False) -> ActionResult:
    """Control system audio"""
    if not function_control.is_function_allowed("Control Audio"):
        return ActionResult(error="Function is disabled")

    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = cast(interface, POINTER(IAudioEndpointVolume))

    # Set volume (0.0 to 1.0)
    volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)

    # Set mute
    volume_control.SetMute(mute, None)

    return ActionResult(extracted_content="Audio settings updated")
