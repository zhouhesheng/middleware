#+
# Copyright 2010 iXsystems
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# $FreeBSD$
#####################################################################

from django.db import models
from django import forms
from django.contrib.auth.models import User
import datetime
import time
from os import popen
from django.utils.text import capfirst
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from storage.models import MountPoint as MountPoint 
from freenasUI.choices import *

class CIFS_Share(models.Model):
    cifs_name = models.CharField(
            max_length=120, 
            verbose_name="Name"
            )
    cifs_comment = models.CharField(
            max_length=120, 
            verbose_name="Comment",
            blank=True,
            )
    cifs_path = models.ForeignKey(MountPoint)
    cifs_ro = models.BooleanField(
            verbose_name="Export Read Only")
    cifs_browsable = models.BooleanField(
            verbose_name="Browsable to Network Clients")
    cifs_inheritperms = models.BooleanField(
            verbose_name="Inherit Permissions")
    cifs_recyclebin = models.BooleanField(
            verbose_name="Export Recylce Bin")
    cifs_showhiddenfiles = models.BooleanField(
            verbose_name="Show Hidden Files")
    cifs_hostsallow = models.CharField(
            max_length=120, 
            blank=True, 
            verbose_name="Hosts allow",
            help_text="This option is a comma, space, or tab delimited set of hosts which are permitted to access this share. You can specify the hosts by name or IP number. Leave this field empty to use default settings."
            )
    cifs_hostsdeny = models.CharField(
            max_length=120, 
            blank=True, 
            verbose_name="Hosts deny",
            help_text="This option is a comma, space, or tab delimited set of host which are NOT permitted to access this share. Where the lists conflict, the allow list takes precedence. In the event that it is necessary to deny all by default, use the keyword ALL (or the netmask 0.0.0.0/0) and then explicitly specify to the hosts allow parameter those hosts that should be permitted access. Leave this field empty to use default settings."
            )
    cifs_auxsmbconf = models.TextField(
            max_length=120, 
            verbose_name="Auxiliary paramters", 
            blank=True,
            help_text="These parameters are added to [Share] section of smb.conf"
            )
    
    def __unicode__(self):
        return self.cifs_name
    class Meta:
        verbose_name = "Windows Share"

       
class AFP_Share(models.Model):
    afp_name = models.CharField(
            max_length=120, 
            verbose_name="Name",
            help_text="The volume name is the name that appears in the Chooser ot the 'connect to server' dialog on Macintoshes to represent the appropriate share. If volumename is unspecified, the last component of pathname is used. No two volumes may have the same name. The volume name cannot contain the ':'  character. The volume name is mangled if it is very long. Mac codepage volume name is limited to 27 characters. UTF8-MAC volume name is limited to 'Volume Name Length' parameter in Services:Apple Share"
            )
    afp_comment = models.CharField(
            max_length=120, 
            verbose_name="Share Comment",
            blank=True
            )
    afp_path = models.ForeignKey(MountPoint, verbose_name="Volume Path")
    afp_sharepw = models.CharField(
            max_length=120, 
            verbose_name="Share password",
            blank=True,
            help_text="This option allows you to set a volume password, which can be a maximum of 8 characters long (using ASCII strongly recommended at the time of this writing)."
        )
    afp_sharecharset = models.CharField(
            max_length=120, 
            verbose_name="Share character set", 
            blank=True,
            help_text="Specifies the share character set. For example UTF8, UTF8-MAC, ISO-8859-15, etc."
            )
    afp_allow = models.CharField(
            max_length=120, 
            verbose_name="Allow List",
            blank=True,
            help_text="This option allows the users and groups that access a share to be specified. Users and groups are specified, delimited by commas. Groups are designated by a @ prefix."
            )
    afp_deny = models.CharField(
            max_length=120, 
            verbose_name="Deny List",
            blank=True,
            help_text="The deny option specifies users and groups who are not allowed access to the share. It follows the same format as the allow option."
            )
    afp_ro = models.CharField(
            max_length=120, 
            verbose_name="Read-only access",
            blank=True,
            help_text="Allows certain users and groups to have read-only access to a share. This follows the allow option format."
        )
    afp_rw = models.CharField(
            max_length=120, 
            verbose_name="Read-write access",
            blank=True,
            help_text="Allows certain users and groups to have read/write access to a share. This follows the allow option format. "
            )
    afp_diskdiscovery = models.BooleanField(
            verbose_name="Disk Discovery",
            help_text="Allow other systems to discover this share as a disk for data, as a Time Machine backup volume or not at all."
            )
    afp_discoverymode = models.CharField(
            max_length=120, 
            choices=DISKDISCOVERY_CHOICES, 
            default='Default', 
            verbose_name="Disk discovery mode",
            help_text="Note! Selecting 'Time Machine' on multiple shares will may cause unpredictable behavior in MacOS.  Default mode exports the volume as a data volume for users."
            )
    afp_dbpath = models.CharField(
            max_length=120, 
            verbose_name="Database Path",
            blank=True,
            help_text="Sets the database information to be stored in path. You have to specifiy a writable location, even if the volume is read only."
            )
    afp_cachecnid = models.BooleanField(
            verbose_name="Cache CNID",
            help_text="If set afpd uses the ID information stored in AppleDouble V2 header files to reduce database load. Don't set this option if the volume is modified by non AFP clients (NFS/SMB/local)."
            )
    afp_crlf = models.BooleanField(
            verbose_name="Translate CR/LF",
            help_text="Enables crlf translation for TEXT files, automatically converting macintosh line breaks into Unix ones. Use of this option might be dangerous since some older programs store binary data files as type 'TEXT' when saving and switch the filetype in a second step. Afpd will potentially destroy such files when 'erroneously' changing bytes in order to do line break translation."
            )
    afp_mswindows = models.BooleanField(
            verbose_name="Windows File Names",
            help_text="This forces filenames to be restricted to the character set used by Windows. This is not recommended for shares used principally by Mac computers."
            )
    afp_noadouble = models.BooleanField(
            verbose_name="No .AppleDouble",
            help_text="This controls whether the .AppleDouble directory gets created unless absolutely needed. This option should not be used if files are access mostly by Mac computers.  Clicking this option disables their creation."
            )
    afp_nodev = models.BooleanField(
            verbose_name="Zero Device Numbers",
            help_text="Always use 0 for device number, helps when the device number is not constant across a reboot, cluster, ..."
            )
    afp_nofileid = models.BooleanField(
            verbose_name="Disable File ID",
            help_text="Don't advertise createfileid, resolveid, deleteid calls."
            )
    afp_nohex = models.BooleanField(
            verbose_name="Disable :hex Names",
            help_text="Disable :hex translations for anything except dot files. This option makes the '/' character illegal."
            )
    afp_prodos = models.BooleanField(
            verbose_name="ProDOS",
            help_text="Provide compatibility with Apple II clients."
            )
    afp_nostat = models.BooleanField(
            verbose_name="No Stat",
            help_text="Don't stat volume path when enumerating volumes list, useful for automounting or volumes created by a preexec script."
            )
    afp_upriv = models.BooleanField(
            verbose_name="AFP3 Unix Privs",
            help_text="Use AFP3 unix privileges."
            )
    
    def __unicode__(self):
        return self.as_path

    class Meta:
        verbose_name = "Share"
    
class NFS_Share(models.Model):
    nfs_comment = models.CharField(
            max_length=120, 
            verbose_name="Comment",
            blank=True,
            )
    nfs_path = models.ForeignKey(MountPoint, verbose_name="Volume Path")
    nfs_allroot = models.BooleanField(
            verbose_name="Map All Remote users as local Root",
            help_text="When enabled, map all remote access to local root.  THIS SETTING IS NOT RECOMMENDED FOR SECURITY REASONS."
            )
    nfs_network = models.CharField(
            max_length=120, 
            verbose_name="Authorized network",
            help_text="Network that is authorized to access the NFS share.  Specify network numbers of the form 1.2.3.4/xx where xx is the number of bits of netmask.",
            blank=True,
            )
    nfs_alldirs = models.BooleanField(
            verbose_name="All dirs",
            help_text="Allow mounting of any subdirectory under this mount point if selected.  Otherwise, only the top level directory can be mounted.",
            )
    nfs_ro = models.BooleanField(
            verbose_name="Read Only",
            help_text="Export the share read only.  Writes are not permitted."
            )
    nfs_quiet = models.BooleanField(
            verbose_name="Quiet",
            help_text="Inibit syslog warnings if there are problems with exporting this share."
            )
    
    def __unicode__(self):
        return self.nfs_path

    class Meta:
        verbose_name = "NFS Share"

