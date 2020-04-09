from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import json
import requests
import subprocess

class VarnishPurgeManager(object):
    def __init__(self):
        registry = getUtility(IRegistry)
        self.ssh_root_password = registry.get('castle.csm.va_ssh_root_pass', None)
        self.ssh_password = registry.get('castle.va_ssh_pass', None)
        self.ssh_user = registry.get('castle.va_ssh_user', None)
        self.port = registry.get('castle.va_port', None)
        self.address = registry.get('castle.va_address', None)
        self.is_ssh = registry.get('castle.va_is_ssh', False)
        self.enabled = (
            self.ssh_password is not None or
            self.ssh_root_password is not None and
            (self.address is not None or
             self.is_ssh))
        self.site = api.portal.get()
        self.site_path = '/' + self.site.virtual_url_path()

    def purge_themes(self):
        self.generate_vcl_script()
        self.generate_ssh_command()
        try:
            sshsubprocess = subprocess.Popen(["ssh", "-t", self.ssh],
                                             stdin=subprocess.PIPE, 
                                             stdout=subprocess.PIPE,
                                             universal_newlines=True, 
                                             bufsize=0)

            with sshsubprocess.stdout
            
            if self.ssh_password is not None:
                sshsubprocess.stdin.write(self.ssh_password + "\n")
                
            sshsubprocess.stdin.write("sudo " + self.vcl_script+"\n")
            if self.ssh_root_password is not None:
                sshsubprocess.stdin.write(self.ssh_root_password + "\n")

            sshsubprocess.stdin.write("logout\n")
            sshsubprocess.stdin.close()
            
        except Exception as ex:
            logger.error("Something Went Wrong with the varnish purging")
            logger.error(ex)
                
    def generate_ssh_command(self):
        if self.is_ssh:
            if self.ssh_user is None:
                if self.port is None:
                    self.ssh = "%s" % self.address
                else:
                    self.ssh = "%s -p %s" % (self.address, self.port)
            else:
                if self.port is None:
                    self.ssh = "%s@%s" % (self.ssh_user, self.address)
                else:
                    self.ssh = "%s@%s -p %s" % (self.ssh_user, self.address, self.port)
        else:
            self.ssh = ""
        if self.ssh_password is None:
            self.ssh_password = ""
        if self.ssh_root_password is None:
            self.ssh_root_password = ""
                
    def generate_vcl_script(self):
        # Generates the vcl scripts for the varnish server 

        vcl_command = "obj.http.x-url ~ (%s).*(gif|jpeg|jpg|png|css|js)" % self.site_path
        
        self.vcl_script = 'varnishadm ban "%s"' % vcl_command
        
def get():
    return VarnishPurgeManager()