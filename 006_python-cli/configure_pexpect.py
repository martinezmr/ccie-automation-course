import pexpect
import sys

router_1_config = open("router1.cfg").read()
router_1_commands = router_1_config.splitlines()

# Spawn a new SSH process
ssh_command = "ssh admin@10.3.19.101"
password = "automation"
child = pexpect.spawn(ssh_command, encoding="utf-8", timeout=20)

# Optionally enable logging
# child.logfile = sys.stdout

# Read the prompt
# The expected output can either a password prompt or ask for acceptance of SSH fingerprint
output = child.expect(["continue connecting (yes/no)?", "Password:", "password:"])

# The matched response is identified by a list item number. 0 means "continue connecting (yes/no)?"
# ("Password:" would be 1 and "password:" would be 2)
if output == 0:
    child.sendline("yes")
    child.expect(["Password:", "password:"])

# Enter the password
child.sendline(password)

# Wait for the router prompt ending with #
child.expect("#")

# Don"t use CLI pagination ("--More--")
child.sendline("terminal length 0")
child.expect("#")

# Enter config mode
child.sendline("conf t")
# Wait for config mode prompt
child.expect(r"\(config\)#")

# Send config command one by one and wait for the prompt to return every time
for command in router_1_commands:
    child.sendline(command)
    child.expect("#")

# Exit configuration mode
child.sendline("end")
child.expect("#")

# 7. Get the "show" output
child.sendline("show interfaces")
child.expect("#")

# .before contains everything before the expected "#" above
# This means we need to remove the first and last line to get a clean output
output = child.before

# Remove the first and last line
cleaned_output_lines = output.splitlines()[1:-1]

# Join all line string with a newline character
cleaned_output = "\n".join(cleaned_output_lines)

print(cleaned_output)
