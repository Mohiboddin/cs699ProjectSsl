import re
import os
import shutil
import sys
import codecs
from datetime import datetime
import secrets
import string

import pexpect #this library is used to insert the password aumatically

#------------------------------------------
#                                         #
#             servers                     #
#                                         #
#------------------------------------------



# Create a custom file-like object for logging (this is very usefull to display the log of pexpect library)
class ConsoleAdapter:
    def write(self, data):
        sys.stdout.write(data.decode())
    def flush(self):
        pass  # This is required to avoid the 'flush' attribute error




# for password less access
#ssh-copy-id server

#------------------------------------------
#                                         #
#       Basic utitilites                  #
#                                         #
#------------------------------------------


date=str(datetime.now().date())

def days_left(t):
    time_left = round((t-datetime.now()).total_seconds())
    return round(time_left/(60*60*24))

def rand_password(l):
    password = ""
    for _ in range(l):
        password += secrets.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits)
    return password

#------------------------------------------
#                                         #
#             SHELL COMMANDS              #
#                                         #
#------------------------------------------

def cmd_if_exists( f ):
    return 'test -e '+ f

def cmd_cp( src, dst ):
    cmd = ['cp', src, dest]
    cmd = ' '.join(cmd)
    return cmd

def cmd_mkdir( d ):
    cmd = ['mkdir -p', d]
    cmd = ' '.join(cmd)
    return cmd

def cmd_mv( src, dst ):
    cmd = ['mv', src, dest]
    cmd = ' '.join(cmd)
    return cmd

def cmd_if_exists( f, cmd ):
    return 'test -e '+ f + ' && '+ cmd

def cmd_if_does_not_exists( f, cmd ):
    return 'test -e '+ f + ' || '+ cmd


def ask_sudo( server, cmds ):
    f.write('#!/bin/bash\n')
    for cmd in cmds:
        f.write('sudo '+ cmd+'\n')


#
# Make it passwordless or password typed locally and transffered to server safely
#
def direct_sudo( server, cmds ):
    pass

#------------------------------------------
#                                         #
#     SEND EMAIL VIA THUNDERBIRD          #
#                                         #
#------------------------------------------

def thunderbird_send( fr, to, subject, body, attachments):
   
# thunderbird -compose "subject='test',to='test@mail.test',body=$output"

#------------------------------------------
#                                         #
#     FIND EMAIL IN THUNDERBIRD           #
#                                         #
#------------------------------------------




#------------------------------------------
#                                         #
#     passwordless scp                    #
#                                         #
#------------------------------------------

# this function helps us to run the command and automatically enter the password.
def run_scp_command(remote_password,command, returnSomething=None):
    # Create an SCP command with the provided command
    scp_command = command

    # Use pexpect to automate password entry
    #child = pexpect.spawn(scp_command, logfile=ConsoleAdapter())
    child = pexpect.spawn(scp_command)
    print (scp_command)
    # Expect the password prompt and capture it
    password_prompt_index = child.expect([pexpect.EOF, ".*[Pp]assword.*"])

    if password_prompt_index == 1:
        last_line = child.after.strip()
        print(last_line)

        # Send the password
        child.sendline(remote_password)

    # Wait for the command to complete
    child.expect(pexpect.EOF)
    
    #if returnSomething is not None:
     #   return child.before.decode()



#------------------------------------------
#                                         #
#     passwordless sshAndThenSudo         #
#                                         #
#------------------------------------------



def sshSudo(hostname, username, password, sudo_command, expectedResponse=None):
    try:
        # Start the SSH session
        ssh_session = pexpect.spawn(f'ssh {username}@{hostname}')
        ssh_session.logfile_read = sys.stdout.buffer

        # Expect the password prompt
        ssh_session.expect([pexpect.EOF, ".*[Pp]assword.*"])
       
        # Temporarily set tActive: active (running)he log file to None for this command so that log will not capture the password.
        #ssh_session.logfile = None
        ssh_session.sendline(password)
        #ssh_session.logfile = ConsoleAdapter()
        ssh_session.expect('[#$] ')

        captured_output = []
        
        for i, cmd in enumerate(sudo_command):
            if 'sudo' in cmd:
                ssh_session.sendline(cmd)
                ssh_session.expect([pexpect.EOF, ".*[Pp]assword.*"])
                # Temporarily set the log file to None for this command so that the log will not capture the password.
                #ssh_session.logfile = None
                ssh_session.sendline(password)
                #ssh_session.logfile = ConsoleAdapter()
                ssh_session.after
                ssh_session.expect('[#$] ')
            else:
                ssh_session.sendline(cmd)
                ssh_session.expect('[#$] ')
             # Check if we need to capture the output of this command
            if expectedResponse is not None and i == expectedResponse:
                captured_output.append(ssh_session.before.decode())

        # Close the SSH session
        ssh_session.sendline('exit')
        ssh_session.expect(pexpect.EOF)
        
        return captured_output

  
    except Exception as e:
        print(f"An error occurred: {str(e)}")


