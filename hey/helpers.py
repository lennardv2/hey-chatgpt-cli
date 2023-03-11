import distro
import platform

def get_os_friendly_name():
  
  # Get OS Name
  os_name = platform.system()
  
  if os_name == "Linux":
      return "Linux/"+distro.name(pretty=True)
  elif os_name == "Windows":
      return os_name
  elif os_name == "Darwin":
     return "Darwin/macOS"

def get_datetime():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")