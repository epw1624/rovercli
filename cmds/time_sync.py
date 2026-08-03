import subprocess

def time_sync(remote_host: str = "rover"):
    print(f"Synchronizing time with remote host: {remote_host}")
    try:
        date_output = subprocess.check_output(["date", "-u", "+%s"]).decode().strip()
        
        subprocess.run(["ssh", remote_host, "sudo", "-S", "date", f"--set='@{date_output}'"], check=True, input=input("Enter password for sudo: ").encode(), capture_output=True)
        print("Time synchronization successful.")
    except subprocess.CalledProcessError as e:
        print(f"Time synchronization failed: {e}")