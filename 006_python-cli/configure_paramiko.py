import paramiko
import time
import logging

# Optionally enable logging
# logging.basicConfig(level=logging.DEBUG)


# We need to control the flow, and wait a little after each command
def wait_for_ios():
    time.sleep(0.5)


# Read the local config file with commands that will be sent to the router
router_1_config = open("router1.cfg").read()

#### Connect with SSH

# Create a new connection
router_1_connection = paramiko.SSHClient()

# Automatically accept the router's SSH fingerprint
router_1_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the router
router_1_connection.connect(
    "10.3.19.101",
    username="admin",
    password="automation",
    look_for_keys=False,  # Disable public-based authentication
)

# Inside the fundamental SSH connection we need an interactive shell.
router_1_shell = router_1_connection.invoke_shell()
wait_for_ios()  # Wait for the prompt


#### Send configuration commands

# Enter config mode
router_1_shell.send("conf t\n")
wait_for_ios()

router_1_commands = router_1_config.splitlines()
for command in router_1_commands:
    # New lines needs to be added to indicate the end of a command
    router_1_shell.send(command + "\n")

    # Give the router a moment to process
    wait_for_ios()

# Exit config mode
router_1_shell.send("end\n")
wait_for_ios()

#### Collect show-command output

# Don't use CLI pagination ("--More--")
router_1_shell.send("terminal length 0\n")
wait_for_ios()


# Define a reuable function to read output from the shell, maximum 65535 bytes at a time
def read_output(shell):
    output = ""
    while True:
        if shell.recv_ready():
            data = shell.recv(65535).decode("utf-8")
            output += data
        else:
            # Brief pause to see if more data is coming
            wait_for_ios()
            if not shell.recv_ready():
                break
    return output


read_output(router_1_shell)

# Run the show-command
router_1_shell.send("show interfaces\n")
wait_for_ios()

# output will contain the original command as well as the returned prompt in the end
output = read_output(router_1_shell)

# Remove the first and last line
cleaned_output_lines = output.splitlines()[1:-1]

# Join all line string with a newline character
cleaned_output = "\n".join(cleaned_output_lines)

print(cleaned_output)
