import subprocess

def time_sync(remote_host: str = "rover"):
    print(f"Synchronizing time with remote host: {remote_host}")
    try:
        subprocess.run(["ssh", remote_host, "sudo", "date", "--set='@$(date -u +%s)'"], check=True)
        print("Time synchronization successful.")
    except subprocess.CalledProcessError as e:
        print(f"Time synchronization failed: {e}")