import subprocess

def time_sync(remote_host: str = "rover"):
    print(f"Synchronizing time with remote host: {remote_host}")
    try:
        pw = input("Enter password for sudo: ").encode()
        date_output = int(subprocess.check_output(["date", "-u", "+%s"]).decode().strip()) + 1
        date_output = str(date_output).strip()
        
        subprocess.run(["ssh", remote_host, "sudo", "-S", "date", f"--set='@{date_output}'"], check=True, input=pw, capture_output=True)
        print("Time synchronization successful.")
    except subprocess.CalledProcessError as e:
        print(f"Time synchronization failed: {e}")