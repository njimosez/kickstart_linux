#!/usr/bin/python
# Graphical Kickstart Script
#
# This script was written by Frank Caviggia, Red Hat Consulting
# Last update was 29 April 2015
# This script is NOT SUPPORTED by Red Hat Global Support Services.
#
# Author: Frank Caviggia (fcaviggia@gmail.com)
# Copyright: Red Hat, (C) 2014
# License: Apache License, Version 2.0
#
# #### CHANGES #############
# 1. Modified and Expanded Developer workstation 
# packages for TACSIM : Edwin Ngwa 2/10/2021

import os,sys,re,crypt,random
try:
	os.environ['DISPLAY']
	import pygtk,gtk
except:
	print "Error: DISPLAY environment varible not set."
	sys.exit(1)

# Class containing verification items
class Verification:
	# Name/Comment Check
	def check_name(self,name):
		pattern = re.compile(r"^[ a-zA-Z']+$",re.VERBOSE)
		if re.match(pattern,name):
			return True
		else:
			return False

	# Check for vaild Unix username
	def check_username(self,username):
		pattern = re.compile(r"^\w{5,255}$",re.VERBOSE)
		if re.match(pattern,username):
			return True
		else:
			return False

	# Check for vaild Unix UID
	def check_uid(self,uid):
		pattern = re.compile(r"^\d{1,10}$",re.VERBOSE)
		if re.match(pattern,uid):
			return True
		else:
			return False

	# Check for vaild IP address
	def check_ip(self,ip):
		pattern = re.compile(r"\b(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5])\b",re.VERBOSE)
		if re.match(pattern,ip) and ip != "0.0.0.0":
			return True
		else:
			return False

        # Check for vaild system hostanme
        def check_hostname(self,hostname):
                pattern = re.compile(r"^[a-zA-Z0-9\-\.]{1,100}$",re.VERBOSE)
                if re.match(pattern,hostname):
                        return True
                else:
                        return False


# Display Menu
class Display_Menu:
        def __init__(self):

		# Initalize Additional Configuration Files
		f = open('/tmp/hardening-post','w')
		f.write('')
		f.close()
		f = open('/tmp/hardening-packages','w')
		f.write('')
		f.close()

                # Data Storage
		self.data = {}

		# Verification Functions
                self.verify = Verification()

                # Create Main Window
                self.window = gtk.Window()
                self.window.set_title("Red Hat Enterprise Linux 6 - TACSIM SSG Installation")
                self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.connect("delete_event",gtk.main_quit)
		self.display = gtk.gdk.display_get_default()
		self.screen = self.display.get_default_screen()
		self.hres = self.screen.get_width()
		self.vres = self.screen.get_height()
		self.window.connect("key-release-event",self.event_key)

                # Create Main Vertical Box to Populate
                self.vbox = gtk.VBox()

                if self.hres == 640:
                        self.window.resize(640,480)
                elif self.hres > 640:
                        self.window.resize(800,600)
			# RedHat Logo
			self.logo = gtk.Image()
			self.logo.set_from_file("/usr/share/anaconda/pixmaps/anaconda_header.png")
			self.logo.set_alignment(0,0)
			self.logo.set_padding(0,0)
			self.vbox.add(self.logo)

                # Creates Header
                self.header = gtk.HBox()
                self.label = gtk.Label("<span font_family='liberation-sans' weight='bold' foreground='red' size='large'>  Red Hat Enterprise Linux 6 - SCAP Security Guide Installation  </span>")
                self.label.set_use_markup(True)
                self.header.add(self.label)
                self.vbox.add(self.header)

                # Creates Information Message
                self.label = gtk.Label('This DVD installs Red Hat Enterprise Linux 6 with configurations required by multiple government regulations')
                self.vbox.add(self.label)
		self.label = gtk.Label('using the SCAP Security Guide (SSG) as a hardening script.                  RHEL 6.10 (TACSIM SSG DVD Installer)')
                self.vbox.add(self.label)

                # Blank Label
                self.label = gtk.Label("")
                self.vbox.add(self.label)    

		# System Configuration
                self.system = gtk.HBox()
                self.label = gtk.Label("   Hostame: ")
                self.system.pack_start(self.label,False,True, 0)
                self.hostname = gtk.Entry(100)
		self.hostname.set_size_request(225,-1)
                self.system.pack_start(self.hostname,False,True,0)
		try:
			if os.environ['HOSTNAME'] != '':
				self.hostname.set_text(os.environ['HOSTNAME'])
			else:
				self.hostname.set_text('localhost.localdomain')
		except:
			self.hostname.set_text('localhost.localdomain')
		self.label = gtk.Label("              System Profile: ")                
		self.system.pack_start(self.label,False,True, 0)
                self.system_profile = gtk.combo_box_new_text()
		self.system_profile.append_text("Minimal Installation")
		self.system_profile.append_text("User Workstation")
		self.system_profile.append_text("TACSIM I&T Workstation")
		# TODO : TACSIM ETL Workstation, TACSIM VM
		#self.system_profile.append_text("IdM Authentication Server")
		#self.system_profile.append_text("RHN Satellite 5.7 Server")
		#self.system_profile.append_text("RHN Satellite 6.0 Server")
		#self.system_profile.append_text("Proprietary Database Server")
		#self.system_profile.append_text("RHEV-Attached KVM Server")
		#self.system_profile.append_text("Standalone KVM Server")
		#self.system_profile.append_text("Apache Web Server")
		#self.system_profile.append_text("Tomcat Web Server")
		#self.system_profile.append_text("PostgreSQL Database Server")
		#self.system_profile.append_text("MySQL Database Server")
		self.system_profile.set_active(0)
		self.system_profile.connect('changed',self.configure_system_profile)
                self.system.pack_start(self.system_profile,False,True,0)
		self.vbox.add(self.system)

                self.classification = gtk.HBox()
		self.label = gtk.Label("                                                                               System Classification: ")
                self.classification.pack_start(self.label,False,True, 0)
                self.system_classification = gtk.combo_box_new_text()
		self.system_classification.append_text("UNCLASSIFIED")
		self.system_classification.append_text("UNCLASSIFIED//FOUO")
		self.system_classification.append_text("CONFIDENTIAL")
		self.system_classification.append_text("SECRET")
		self.system_classification.append_text("TOP SECRET")
		self.system_classification.append_text("TOP SECRET//SCI")
		self.system_classification.append_text("TOP SECRET//SCI//NOFORN")
		self.system_classification.set_active(0)
                self.classification.pack_start(self.system_classification,False,True,0)
		self.vbox.add(self.classification)

                self.security = gtk.HBox()
		self.label = gtk.Label("                                                                     SCAP Security Guide Profile: ")
                self.security.pack_start(self.label,False,True, 0)
                self.system_security = gtk.combo_box_new_text()
		self.system_security.append_text("DISA STIG")
		#self.system_security.append_text("USGCB")
		self.system_security.set_active(0)
		self.system_security.connect('changed',self.configure_system_profile)
                self.security.pack_start(self.system_security,False,True,0)
		self.vbox.add(self.security)

                # Blank Label
                self.label = gtk.Label("")
                self.vbox.add(self.label)


		# System Information
		self.cpu_cores = 0
		self.cpu_model = ''
		self.cpu_arch = ''
		self.system_memory = {}
		with open('/proc/cpuinfo') as f:
	    		for line in f:
				if line.strip():
		    			if line.rstrip('\n').startswith('model name'):
						self.cpu_model = line.rstrip('\n').split(':')[1]
						self.cpu_cores += 1
            				elif line.rstrip('\n').startswith('flags') or line.rstrip('\n').startswith('Features'):
                				if 'lm' in line.rstrip('\n').split():
                   		 			self.cpu_arch = '64-bit'
                				else:
                   		 			self.cpu_arch = '32-bit'
		f.close()

		with open('/proc/meminfo') as f:
			for line in f:
				self.system_memory[line.split(':')[0]] = line.split(':')[1].strip()
		f.close()
						
                self.cpu_information = gtk.HBox()
                self.label = gtk.Label("   CPU Model: ")
                self.cpu_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label(" %s "%(self.cpu_model))
                self.cpu_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label("   CPU Threads: ")
                self.cpu_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label(" %d "%(self.cpu_cores))
                self.cpu_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label("   Architecure: ")
                self.cpu_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label(" %s "%(self.cpu_arch))
                self.cpu_information.pack_start(self.label,False,True, 0)
		self.vbox.add(self.cpu_information)

                self.memory_information = gtk.HBox()
                self.label = gtk.Label("   Total System Memory: ")
                self.memory_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label(" %s "%(self.system_memory['MemTotal']))
                self.memory_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label("   Free Memory: ")
                self.memory_information.pack_start(self.label,False,True, 0)
                self.label = gtk.Label(" %s "%(self.system_memory['MemFree']))
                self.memory_information.pack_start(self.label,False,True, 0)
		self.vbox.add(self.memory_information)

                # Disk Partitioning Section
                self.label = gtk.Label("\n<span font_family='liberation-sans' weight='bold'>Disk Partitioning</span>")
                self.label.set_use_markup(True)
                self.vbox.add(self.label)

                # Blank Label
                self.label = gtk.Label("")
                self.vbox.add(self.label)

                # List Disks
                self.disk_list = gtk.HBox()

                self.disk_info = []
		self.disk_total = 0
                self.output = os.popen('list-harddrives')
                for self.line in self.output:
                        self.line = self.line.strip()
			if not ('fd0' in self.line or 'sr0' in self.line):
				self.disk_info.append(self.line.split(' '))
               
		self.label = gtk.Label("   Available Disks: ")
                self.disk_list.pack_start(self.label, False, True, 0)

		if len(self.disk_info) == 0:
                        self.label = gtk.Label("No Drives Available.")
                        self.disk_list.pack_start(self.label,False,True,0)
                else:
                        for i in range(len(self.disk_info)):
				if len(self.disk_info) > 5:
					exec("self.disk%d = gtk.CheckButton(self.disk_info[%d][0])"%(i,i))
                               	else:
					exec("self.disk%s = gtk.CheckButton(self.disk_info[%d][0] +' ('+ str(int(float(self.disk_info[%d][1]))/1024) +'Gb)')"%(i,i,i))
                                exec("self.disk%d.set_active(True)"%(i))
                                exec("self.disk_list.pack_start(self.disk%d, False, True, 0)"%(i))
				self.disk_total += int(float(self.disk_info[i][1])/1024)

                self.vbox.add(self.disk_list)

                # Disk Encryption (Ability to disable LUKS for self encrypting drives)
                self.encrypt = gtk.HBox()

		self.label = gtk.Label("                             ")
                self.encrypt.pack_start(self.label, False, True, 0)

		self.encrypt_disk = gtk.CheckButton('Encrypt Drives with LUKS')
		self.encrypt_disk.set_active(True)
		self.encrypt.pack_start(self.encrypt_disk, False, True, 0)

		self.label = gtk.Label("   ")
                self.encrypt.pack_start(self.label, False, True, 0)

		self.fips_kernel = gtk.CheckButton('Kernel in FIPS 140-2 Mode')
		self.fips_kernel.set_active(True)
		self.encrypt.pack_start(self.fips_kernel, False, True, 0)

                self.nousb_kernel = gtk.CheckButton('Disable USB (nousb)')
		self.nousb_kernel.set_active(False)
		self.encrypt.pack_start(self.nousb_kernel, False, True, 0)

		self.vbox.add(self.encrypt)


		# Minimal Installation Warning
		if self.disk_total < 8:
			self.MessageBox(self.window,"<b>Recommended minimum of 8Gb disk space for a Minimal Install!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)

                # Blank Label
                self.label = gtk.Label("")
                self.vbox.add(self.label)

		# Partitioning
                self.label = gtk.Label('Required LVM Partitioning Percentage')
                self.vbox.add(self.label)
		self.partitioning1 = gtk.HBox()
                self.label = gtk.Label("           ROOT (/) ")
                self.partitioning1.pack_start(self.label,False,True,0)
		self.root_range = gtk.Adjustment(30,1,95,1,0, 0)
      		self.root_partition = gtk.SpinButton(adjustment=self.root_range,climb_rate=1,digits=0)
		self.root_partition.connect('value-changed',self.lvm_check)
                self.partitioning1.pack_start(self.root_partition,False,True,0)
		self.label = gtk.Label("%  HOME (/home) ")
                self.partitioning1.pack_start(self.label,False,True,0)
		self.home_range = gtk.Adjustment(25,1,95,1,0, 0)
   		self.home_partition = gtk.SpinButton(adjustment=self.home_range,climb_rate=1,digits=0)
		self.home_partition.connect('value-changed',self.lvm_check)
                self.partitioning1.pack_start(self.home_partition,False,True,0)
                self.label = gtk.Label("%  TMP (/tmp) ")
                self.partitioning1.pack_start(self.label,False,True,0)
		self.tmp_range = gtk.Adjustment(10,1,60,1,0, 0)
   		self.tmp_partition = gtk.SpinButton(adjustment=self.tmp_range,climb_rate=1,digits=0)
		self.tmp_partition.connect('value-changed',self.lvm_check)
                self.partitioning1.pack_start(self.tmp_partition,False,True,0)
                self.label = gtk.Label("%  VAR (/var) ")
                self.partitioning1.pack_start(self.label,False,True,0)
		self.var_range = gtk.Adjustment(10,1,95,1,0, 0)
   		self.var_partition = gtk.SpinButton(adjustment=self.var_range,climb_rate=1,digits=0)
		self.var_partition.connect('value-changed',self.lvm_check)
                self.partitioning1.pack_start(self.var_partition,False,True,0)
                self.label = gtk.Label("%")
                self.partitioning1.pack_start(self.label,False,True,0)

		self.vbox.add(self.partitioning1)
		self.partitioning2 = gtk.HBox()
                self.label = gtk.Label("  LOG (/var/log) ")
                self.partitioning2.pack_start(self.label,False,True,0)
		self.log_range = gtk.Adjustment(10,1,75,1,0, 0)
   		self.log_partition = gtk.SpinButton(adjustment=self.log_range,climb_rate=1,digits=0)
		self.log_partition.connect('value-changed',self.lvm_check)
                self.partitioning2.pack_start(self.log_partition,False,True,0)
                self.label = gtk.Label("%  AUDIT (/var/log/audit) ")
                self.partitioning2.pack_start(self.label,False,True,0)
		self.audit_range = gtk.Adjustment(10,1,75,1,0, 0)
   		self.audit_partition = gtk.SpinButton(adjustment=self.audit_range,climb_rate=1,digits=0)
		self.audit_partition.connect('value-changed',self.lvm_check)
                self.partitioning2.pack_start(self.audit_partition,False,True,0)
                self.label = gtk.Label("%  SWAP ")
                self.partitioning2.pack_start(self.label,False,True,0)
		self.swap_range = gtk.Adjustment(5,1,25,1,0, 0)
   		self.swap_partition = gtk.SpinButton(adjustment=self.swap_range,climb_rate=1,digits=0)
		self.swap_partition.connect('value-changed',self.lvm_check)
                self.partitioning2.pack_start(self.swap_partition,False,True,0)
                self.label = gtk.Label("%")
                self.partitioning2.pack_start(self.label,False,True,0)
		self.vbox.add(self.partitioning2)
                # Blank Label
                self.label = gtk.Label("")
                self.vbox.add(self.label)
                self.label = gtk.Label('Optional LVM Partitioning Percentage')
                self.vbox.add(self.label)
		self.partitioning3 = gtk.HBox()
                self.label = gtk.Label("           WWW (/var/www) ")
                self.partitioning3.pack_start(self.label,False,True,0)
		self.www_range = gtk.Adjustment(0,0,90,1,0, 0)
      		self.www_partition = gtk.SpinButton(adjustment=self.www_range,climb_rate=1,digits=0)
		self.www_partition.connect('value-changed',self.lvm_check)
                self.partitioning3.pack_start(self.www_partition,False,True,0)
                self.label = gtk.Label("%   OPT (/opt) ")
                self.partitioning3.pack_start(self.label,False,True,0)
		self.opt_range = gtk.Adjustment(0,0,90,1,0, 0)
      		self.opt_partition = gtk.SpinButton(adjustment=self.opt_range,climb_rate=1,digits=0)
		self.opt_partition.connect('value-changed',self.lvm_check)
                self.partitioning3.pack_start(self.opt_partition,False,True,0)
                self.label = gtk.Label("%")
                self.partitioning3.pack_start(self.label,False,True,0)
		self.vbox.add(self.partitioning3)

                # Blank Label
                self.label = gtk.Label("")
                self.vbox.add(self.label)
         
          	self.partition_message = gtk.HBox()
                self.label = gtk.Label('Note:LVM Partitions should add up to less than 100% if you intend to reserve space for a restore partition on the same drive.\n-Free space if available may be used to create a restore partition later.  <b>Currently Used:</b> ')
		self.label.set_use_markup(True)
                self.partition_message.pack_start(self.label,False,True,0)
		self.partition_used = gtk.Label('100%')
                self.partition_message.pack_start(self.partition_used,False,True,0)
                self.vbox.add(self.partition_message)

                # Button Bar at the Bottom of the Window
                self.label = gtk.Label("")
                self.vbox.add(self.label)
                self.button_bar = gtk.HBox()

                # Apply Configurations
                self.button1 = gtk.Button(None,gtk.STOCK_OK)
                self.button1.connect("clicked",self.apply_configuration)
                self.button_bar.pack_end(self.button1,False,True,0)

                # Help
                self.button2 = gtk.Button(None,gtk.STOCK_HELP)
                self.button2.connect("clicked",self.show_help_main)
                self.button_bar.pack_end(self.button2,False,True,0)

                # Network Configuration
                self.button3 = gtk.Button("Network",None)
                self.button3.connect("clicked",self.configure_network,self.window)
                self.button_bar.pack_end(self.button3,False,True,0)

		# Network Configuration Default Values
		self.network_device = 0
		self.network_dhcp = True
		self.network_ip = "192.168.0.2"
		self.network_netmask = "255.255.255.0"
		self.network_gateway = "192.168.0.1"
		self.network_dns1 = "8.8.8.8"
		self.network_dns2 = "8.8.4.4"
	
                self.vbox.add(self.button_bar)
                self.window.add(self.vbox)
                self.window.show_all()

		## STOCK CONFIGURATIONS (Minimal Install)
		# Default SSG Profile (DISA STIG)
		self.profile='stig-rhel6-server-upstream'
		# Post Configuration (nochroot)
		f = open('/tmp/hardening-post-nochroot','w')
		f.write('')
		f.close()
		# Post Configuration
		f = open('/tmp/hardening-post','w')
		# Run Hardening Script
		f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
		# Firewall Configuration
		f.write('cp /root/hardening/iptables.sh /root/\n')
		f.write('/root/iptables.sh\n')
		f.close()
		# Package Selection
		f = open('/tmp/hardening-packages','w')
		f.write('')
		f.close()

	# Key Press Event
	def event_key(self,args,event):
		if event.keyval == gtk.keysyms.F12:	
			self.apply_configuration(args)
		elif event.keyval == gtk.keysyms.F1:
			self.show_help_main(args)

	# Shows Help for Main Install
        def show_help_main(self,args):
		self.help_text = ("<b>Install Help</b>\n\n- All LVM partitions need to take less than or equal to 100% of the LVM Volume Group.\n\n- Pressing OK prompts for a password to encrypt Disk (LUKS), GRUB, and Root password.\n\n- The sshusers group controls remote access, wheel group is for root users, and isso group is for limited root with auditing permissions.\n\n- To access root remotely via ssh you need to create a user and add them to the wheel and sshusers groups.\n\n- Minimum password length is 14 characters, using a strong password is recommended.\n")
                self.MessageBox(self.window,self.help_text,gtk.MESSAGE_INFO)


	# System Profile Configuration
	def configure_system_profile(self,args):

		# Turn on FIPS 140-2 mode for Kernel (Default)
		self.fips_kernel.set_active(True)

		# Zero out partitioning values
		self.opt_partition.set_value(0)
		self.www_partition.set_value(0)
		self.swap_partition.set_value(0)
		self.tmp_partition.set_value(0)
		self.var_partition.set_value(0)
		self.log_partition.set_value(0)
		self.audit_partition.set_value(0)
		self.home_partition.set_value(0)
		self.root_partition.set_value(0)

		# Define SSG Security Profile
		if int(self.system_security.get_active()) == 0:
			self.profile='stig-rhel6-server-upstream'
		if int(self.system_security.get_active()) == 1:
			self.profile='usgcb-rhel6-server'
			if int(self.system_classification.get_active()) > 1:
				# WARNING - Classification Requires DISA STIG
 				self.MessageBox(self.window,"<b>Warning:</b> DISA STIG is requred for the Classification of the System Specified!",gtk.MESSAGE_WARNING)
				self.system_security.set_active(0)
				self.profile='stig-rhel6-server-upstream'	

		################################################################################################################
		# Minimal (Defaults to Kickstart)
		################################################################################################################
		if int(self.system_profile.get_active()) == 0:
			# Partitioning
			if self.disk_total < 8:
				self.MessageBox(self.window,"<b>Recommended minimum of 8Gb disk space for a Minimal Install!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('')
			f.close()

		################################################################################################################
		# User Workstation
		################################################################################################################
		if int(self.system_profile.get_active()) == 1:
			# Partitioning
			if self.disk_total < 12:
				self.MessageBox(self.window,"<b>Recommended minimum of 12Gb disk space for a User Workstation!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('cp /mnt/source/hardening/classification-banner.py /mnt/sysimage/usr/local/bin/\n')
			f.write('chmod a+rx /mnt/sysimage/usr/local/bin/classification-banner.py\n')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('@basic-desktop\n')
			f.write('@desktop-platform\n')
			f.write('@directory-client\n')
			f.write('@general-desktop\n')
			f.write('@graphical-admin-tools\n')
			f.write('@input-methods\n')
			f.write('@internet-browser\n')
			f.write('@x11\n')
			f.write('pcsc*\n')
			f.write('coolkey\n')
			f.write('liberation-*\n')
			f.write('dejavu-*\n')
			f.write('icedtea-web\n')
			f.write('krb5-auth-dialog\n')
			f.write('seahorse-plugins\n')
			f.write('vim-X11\n')
			f.write('system-config-lvm\n')
			f.write('audit-viewer\n')
			f.write('openmotif\n')
			f.write('libXmu\n')
			f.write('libXp\n')
			f.write('openmotif22\n')
			f.write('-samba-winbind\n')
			f.write('-certmonger\n')
			f.write('-gnome-applets\n')
			f.write('-vino\n')
			f.write('-ypbind\n')
			f.write('-cheese\n')
			f.write('-gnome-backgrounds\n')
			f.write('-compiz-gnome\n')
			f.write('-gnome-bluetooth\n')
			f.write('-gnome-user-share\n')
			f.write('-sound-juicer\n')
			f.write('-rhythmbox\n')
			f.write('-brasero\n')
			f.write('-brasero-nautilus\n')
			f.write('-brasero-libs\n')
			f.write('-NetworkManager\n')
			f.write('-NetworkManager-gnome\n')
			f.write('-evolution-data-server\n')
			f.write('-NetworkManager-glib\n')
			f.write('-m17n-contrib-bengali\n')
			f.write('-m17n-contrib-punjabi\n')
			f.write('-ibus-sayura\n')
			f.write('-m17n-contrib-assamese\n')
			f.write('-m17n-contrib-oriya\n')
			f.write('-m17n-contrib-kannada\n')
			f.write('-m17n-contrib-telugu\n')
			f.write('-m17n-contrib-hindi\n')
			f.write('-m17n-contrib-maithili\n')
			f.write('-m17n-db-sinhala\n')
			f.write('-m17n-contrib-marathi\n')
			f.write('-m17n-db-thai\n')
			f.write('-ibus-pinyin\n')
			f.write('-m17n-contrib-urdu\n')
			f.write('-m17n-contrib-tamil\n')
			f.write('-ibus-chewing\n')
			f.write('-ibus-hangul\n')
			f.write('-ibus-anthy\n')
			f.write('-m17n-contrib-malayalam\n')
			f.write('-m17n-contrib-gujarati\n')
			f.close()


		################################################################################################################
		# TACSIM I&T Workstation
		################################################################################################################
		if int(self.system_profile.get_active()) == 2:
			# Partitioning
			if self.disk_total < 150:
				self.MessageBox(self.window,"<b>Recommended minimum 150Gb disk space for a TACSIM I&T Workstation!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('cp /mnt/source/hardening/classification-banner.py /mnt/sysimage/usr/local/bin/\n')
			f.write('chmod a+rx /mnt/sysimage/usr/local/bin/classification-banner.py\n')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('@additional-devel\n')
			f.write('@basic-desktop\n')
			f.write('@desktop-platform\n')
			f.write('@desktop-platform-devel\n')
			f.write('@development\n')
			f.write('@directory-client\n')
			f.write('@eclipse\n')
			f.write('@general-desktop\n')
			f.write('@graphical-admin-tools\n')
			f.write('@input-methods\n')
			f.write('@internet-browser\n')
			f.write('@java-platform\n')
			f.write('@legacy-x\n')
			f.write('@server-platform-devel\n')
			f.write('@x11\n')
			f.write('pcsc*\n')
			f.write('coolkey\n')
			f.write('liberation-*\n')
			f.write('dejavu-*\n')
			f.write('icedtea-web\n')
			f.write('libXinerama-devel\n')
			f.write('openmotif-devel\n')
			f.write('libXmu-devel\n')
			f.write('xorg-x11-proto-devel\n')
			f.write('startup-notification-devel\n')
			f.write('libgnomeui-devel\n')
			f.write('libbonobo-devel\n')
			f.write('junit\n')
			f.write('libXau-devel\n')
			f.write('libgcrypt-devel\n')
			f.write('popt-devel\n')
			f.write('gnome-python2-desktop\n')
			f.write('libdrm-devel\n')
			f.write('libXrandr-devel\n')
			f.write('libxslt-devel\n')
			f.write('libglade2-devel\n')
			f.write('gnutls-devel\n')
			f.write('desktop-file-utils\n')
			f.write('ant\n')
			f.write('rpmdevtools\n')
			f.write('gcc-java\n')
			f.write('jpackage-utils\n')
			f.write('rpmlint\n')
			f.write('krb5-auth-dialog\n')
			f.write('seahorse-plugins\n')
			f.write('vim-X11\n')
			f.write('system-config-lvm\n')
			f.write('audit-viewer\n')
			f.write('openmotif\n')
			f.write('libXmu\n')
			f.write('libXp\n')
			f.write('openmotif22\n')
			f.write('-samba-winbind\n')
			f.write('-certmonger\n')
			f.write('-gnome-applets\n')
			f.write('-vino\n')
			f.write('-ypbind\n')
			f.write('-cheese\n')
			f.write('-gnome-backgrounds\n')
			f.write('-compiz-gnome\n')
			f.write('-gnome-bluetooth\n')
			f.write('-gnome-user-share\n')
			f.write('-sound-juicer\n')
			f.write('-rhythmbox\n')
			f.write('-brasero\n')
			f.write('-brasero-nautilus\n')
			f.write('-brasero-libs\n')
			f.write('-NetworkManager\n')
			f.write('-NetworkManager-gnome\n')
			f.write('-evolution-data-server\n')
			f.write('-evolution-data-server-devel\n')
			f.write('-NetworkManager-glib\n')
			f.write('-m17n-contrib-bengali\n')
			f.write('-m17n-contrib-punjabi\n')
			f.write('-ibus-sayura\n')
			f.write('-m17n-contrib-assamese\n')
			f.write('-m17n-contrib-oriya\n')
			f.write('-m17n-contrib-kannada\n')
			f.write('-m17n-contrib-telugu\n')
			f.write('-m17n-contrib-hindi\n')
			f.write('-m17n-contrib-maithili\n')
			f.write('-m17n-db-sinhala\n')
			f.write('-m17n-contrib-marathi\n')
			f.write('-m17n-db-thai\n')
			f.write('-ibus-pinyin\n')
			f.write('-m17n-contrib-urdu\n')
			f.write('-m17n-contrib-tamil\n')
			f.write('-ibus-chewing\n')
			f.write('-ibus-hangul\n')
			f.write('-ibus-anthy\n')
			f.write('-m17n-contrib-malayalam\n')
			f.write('-m17n-contrib-gujarati\n')
			#  Additional TACSIM I&T Package Selection
                        f.write('-brasero\n')
			f.write('-brasero-nautilus\n')
			f.write('-brasero-libs\n')
			f.write('@office-suite\n')
			f.write('@virtualization\n')
			f.write('@virtualization-client\n')
			f.write('@virtualization-platform\n')
			f.write('@virtualization-tools\n')
			f.write('perl-Sys-Virt\n')
			f.write('qemu-kvm-tools\n')
			f.write('fence-virtd-libvirt\n')
			f.write('virt-v2v\n')
			f.write('ebtables\n')
			f.write('libguestfs-tools\n')
			f.write('nfs-utils\n')
			f.write('nfs-utils-lib\n')
			f.write('mysql-server\n')
           	        f.close()


		################################################################################################################
		# IdM/IPA Authentication Server
		################################################################################################################
		if int(self.system_profile.get_active()) == 3:
			# Turn off FIPS 140-2 mode for Kernel
			self.fips_kernel.set_active(False)
			# Partitioning
			if self.disk_total < 8:
				self.MessageBox(self.window,"<b>Recommended minimum of 10Gb disk space for a IdM Authentication Server Install!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(5)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(15)
			self.root_partition.set_value(35)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --idm\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('ipa-server\n')
			f.write('ipa-server-selinux\n')
			f.write('ipa-admintools\n')
			f.write('ipa-client\n')
			f.write('nfs-utils\n')
			f.write('nfs-utils-lib\n')
			f.close()


		################################################################################################################
		# RHN Satellite 5.7 Install
		################################################################################################################
		if int(self.system_profile.get_active()) == 4:
			# Turn off FIPS 140-2 mode for Kernel
			self.fips_kernel.set_active(False)
			# Partitioning
			if self.disk_total < 120:
				self.MessageBox(self.window,"<b>Recommended minimum of 120Gb disk space for a RHN Satelite Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(20)
			self.www_partition.set_value(3)
			self.swap_partition.set_value(1)
			self.tmp_partition.set_value(2)
			self.var_partition.set_value(60)
			self.log_partition.set_value(3)
			self.audit_partition.set_value(3)
			self.home_partition.set_value(3)
			self.root_partition.set_value(5)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# RHN Satellite requires umask of 022 for installation only for root
			f.write('cat "umask 022" >> /root/.bashrc\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --https\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('')
			f.close()


		################################################################################################################
		# RHN Satellite 6.x Install
		################################################################################################################
		if int(self.system_profile.get_active()) == 5:
			# Turn off FIPS 140-2 mode for Kernel
			self.fips_kernel.set_active(False)
			# Partitioning
			if self.disk_total < 120:
				self.MessageBox(self.window,"<b>Recommended minimum of 120Gb disk space for a RHN Satelite Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(20)
			self.www_partition.set_value(3)
			self.swap_partition.set_value(1)
			self.tmp_partition.set_value(2)
			self.var_partition.set_value(60)
			self.log_partition.set_value(3)
			self.audit_partition.set_value(3)
			self.home_partition.set_value(3)
			self.root_partition.set_value(5)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# RHN Satellite requires umask of 022 for installation only for root
			f.write('cat "umask 022" >> /root/.bashrc\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('')
			f.close()
			
			
		################################################################################################################
		# Proprietary Database
		################################################################################################################
		if int(self.system_profile.get_active()) == 6:
			# Partitioning
			if self.disk_total < 60:
				self.MessageBox(self.window,"<b>Recommended minimum of 60Gb disk space for a Proprietary Database Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.www_partition.set_value(0)
			self.home_partition.set_value(5)
			self.swap_partition.set_value(5)
			self.var_partition.set_value(7)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.tmp_partition.set_value(15)
			self.opt_partition.set_value(30)
			self.root_partition.set_value(18)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('cp /mnt/source/hardening/classification-banner.py /mnt/sysimage/usr/local/bin/\n')
			f.write('chmod a+rx /mnt/sysimage/usr/local/bin/classification-banner.py\n')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('xorg-x11-server-Xorg\n')
			f.write('xorg-x11-xinit\n')
			f.write('xterm\n')
			f.write('twm\n')
			f.write('liberation-*\n')
			f.write('dejavu-*\n')
			f.write('openmotif\n')
			f.write('libXmu\n')
			f.write('libXp\n')
			f.write('openmotif22\n')
			f.write('kernel-devel\n')
			f.write('kernel-headers\n')
			f.write('gcc\n')
			f.write('gcc-c++\n')
			f.write('libgcc\n')
			f.write('autoconf\n')
			f.write('make\n')
			f.write('libstdc++\n')
			f.write('compat-libstdc++-33\n')
			f.write('libaio\n')
			f.write('libaio-devel\n')
			f.write('unixODBC\n')
			f.write('unixODBC-devel\n')
			f.write('sysstat\n')
			f.write('ksh\n')
			f.close()
			
		################################################################################################################
		# RHEV-Attached KVM Server
		################################################################################################################
		if int(self.system_profile.get_active()) == 7:
			# WARNING - HARDENDING SCRIPT NOT RUN!
 			self.MessageBox(self.window,"<b>Warning:</b> Please run the following script before adding system RHEV-M:\n\n   # /root/rhevm-preinstall.sh\n\nAfter adding the system to RHEV-M, run the following:\n\n   # /root/rhevm-postinstall.sh",gtk.MESSAGE_WARNING)
			# Partitioning
			if self.disk_total < 60:
				self.MessageBox(self.window,"<b>Recommended minimum of 60Gb disk space for a RHEV-Attached KVM Server Install!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# RHEV Scripts for Pre-Install/Post-Install
			f.write('cp /root/hardening/rhevm*.sh /root/\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --kvm\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('ebtables')
			f.close()


		################################################################################################################
		# Standalone KVM Installation
		################################################################################################################
		if int(self.system_profile.get_active()) == 8:
			# Partitioning
			if self.disk_total < 60:
				self.MessageBox(self.window,"<b>Recommended minimum 60Gb disk space for a RHEL/KVM Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(2)
			self.tmp_partition.set_value(3)
			self.var_partition.set_value(65)
			self.log_partition.set_value(5)
			self.audit_partition.set_value(5)
			self.home_partition.set_value(5)
			self.root_partition.set_value(15)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --kvm\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('@storage-client-iscsi\n')
			f.write('@virtualization\n')
			f.write('@virtualization-client\n')
			f.write('@virtualization-platform\n')
			f.write('@virtualization-tools\n')
			f.write('perl-Sys-Virt\n')
			f.write('qemu-kvm-tools\n')
			f.write('fence-virtd-libvirt\n')
			f.write('virt-v2v\n')
			f.write('ebtables\n')
			f.write('libguestfs-tools\n')
			f.close()


		################################################################################################################
		# Apache HTTPD (Web Server)
		################################################################################################################
		if int(self.system_profile.get_active()) == 9:
			# Partitioning
			if self.disk_total < 10:
				self.MessageBox(self.window,"<b>Recommended minimum of 10Gb disk space for a Web Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --https\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('httpd\n')
			f.close()


		################################################################################################################
		# Apache HTTPD/Tomcat
		################################################################################################################
		if int(self.system_profile.get_active()) == 10:
			# Partitioning
			if self.disk_total < 10:
				self.MessageBox(self.window,"<b>Recommended minimum of 10Gb disk space for an Apache Tomcat Web Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('tomcat6\n')
			f.write('httpd\n')
			f.close()


		################################################################################################################
		# PostgreSQL Database
		################################################################################################################
		if int(self.system_profile.get_active()) == 11:
			# Partitioning
			if self.disk_total < 16:
				self.MessageBox(self.window,"<b>Recommended minimum of 16Gb disk space for a PostgreSQL Database Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --postgresql\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('postgresql\n')
			f.close()


		################################################################################################################
		# MySQL Database
		################################################################################################################
		if int(self.system_profile.get_active()) == 12:
			# Partitioning
			if self.disk_total < 16:
				self.MessageBox(self.window,"<b>Recommended minimum of 16Gb disk space for a MariaDB Database Server!</b>\n\n You have "+str(self.disk_total)+"Gb available.",gtk.MESSAGE_WARNING)
			self.opt_partition.set_value(0)
			self.www_partition.set_value(0)
			self.swap_partition.set_value(5)
			self.tmp_partition.set_value(10)
			self.var_partition.set_value(10)
			self.log_partition.set_value(10)
			self.audit_partition.set_value(10)
			self.home_partition.set_value(25)
			self.root_partition.set_value(30)
			# Post Configuration (nochroot)
			f = open('/tmp/hardening-post-nochroot','w')
			f.write('')
			f.close()
			# Post Configuration
			f = open('/tmp/hardening-post','w')
			# Run Hardening Script
			f.write('/usr/bin/oscap xccdf eval --profile '+str(self.profile)+' --remediate --results /root/`hostname`-ssg-results.xml  --cpe /usr/share/xml/scap/ssg/content/ssg-rhel6-cpe-dictionary.xml /usr/share/xml/scap/ssg/content/ssg-rhel6-xccdf.xml\n')
			# Firewall Configuration
			f.write('cp /root/hardening/iptables.sh /root/\n')
			f.write('/root/iptables.sh --mysql\n')
			f.close()
			# Package Selection
			f = open('/tmp/hardening-packages','w')
			f.write('mysql-server\n')
			f.close()


	# Check LVM Partitioning
	def lvm_check(self,args):
		self.lvm = self.root_partition.get_value_as_int()+self.home_partition.get_value_as_int()+self.tmp_partition.get_value_as_int()+self.var_partition.get_value_as_int()+self.log_partition.get_value_as_int()+self.audit_partition.get_value_as_int()+self.swap_partition.get_value_as_int()+self.www_partition.get_value_as_int()+self.opt_partition.get_value_as_int()
		self.partition_used.set_label(str(self.lvm)+'%')
		if int(self.lvm) > 100:
			self.MessageBox(self.window,"<b>Verify that LVM configuration is not over 100%!</b>",gtk.MESSAGE_ERROR)
			return False
		else:
			return True


	# Display Message Box (e.g. Help Screen, Warning Screen, etc.)
	def MessageBox(self,parent,text,type=gtk.MESSAGE_INFO):
                message = gtk.MessageDialog(parent,0,type,gtk.BUTTONS_OK)
		message.set_markup(text)	
		response = message.run()
		if response == gtk.RESPONSE_OK:
			message.destroy()

		
	# Get Password Dialog
	def get_password(self,parent):
		dialog = gtk.Dialog("Configure System Password",parent,gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT,gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))
		self.pass1 = gtk.HBox()
                self.label1 = gtk.Label("           Passsword: ")
                self.pass1.pack_start(self.label1,False,True,0)
		self.password1 = gtk.Entry()
		self.password1.set_visibility(False)
		self.pass1.pack_start(self.password1,False,True,0)
		dialog.vbox.add(self.pass1)
		self.pass2 = gtk.HBox()
                self.label2 = gtk.Label("  Verify Password: ")
                self.pass2.pack_start(self.label2,False,True,0)
		self.password2 = gtk.Entry()
		self.password2.set_visibility(False)
		self.pass2.pack_start(self.password2,False,True,0)
		dialog.vbox.add(self.pass2)
		dialog.show_all()
		response = dialog.run()
		if response == gtk.RESPONSE_ACCEPT:
			self.a = self.password1.get_text()
			self.b = self.password2.get_text()
			dialog.destroy()
		else:
			self.a = ''
			self.b = ''
			dialog.destroy()

	# Configure Network Dialog
	def configure_network(self,parent,window):
		self.network_dialog = gtk.Dialog("Configure Network",window,gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))

                # List Network Ports
                self.network = gtk.HBox()
		self.label = gtk.Label(" Network Device(s): ")
		self.network.pack_start(self.label, False, True, 0)
		self.network_devices = gtk.combo_box_new_text()
                self.output = os.popen("ip link show | grep UP | awk -F ': ' '{ print $2 }'")
                for self.line in self.output:
                        self.line = self.line.strip()
			if not ('lo' in self.line):
               			self.network_devices.append_text(self.line)
		self.network.pack_start(self.network_devices,False,True,0)
		self.network_dialog.vbox.add(self.network)
		self.network = gtk.HBox()
		self.dhcp = gtk.CheckButton('DHCP')
		self.network.pack_start(self.dhcp,False,True,0)
		self.network_dialog.vbox.add(self.network)
		self.network = gtk.HBox()
                self.label = gtk.Label("           IP Address: ")
                self.network.pack_start(self.label,False,True,0)
		self.ip = gtk.Entry()
		self.network.pack_start(self.ip,False,True,0)
		self.network_dialog.vbox.add(self.network)
		self.network = gtk.HBox()
                self.label = gtk.Label("              Netmask: ")
                self.network.pack_start(self.label,False,True,0)
		self.netmask = gtk.Entry()
		self.network.pack_start(self.netmask,False,True,0)
		self.network_dialog.vbox.add(self.network)
		self.network = gtk.HBox()
                self.label = gtk.Label("              Gateway: ")
                self.network.pack_start(self.label,False,True,0)
		self.gateway = gtk.Entry()
		self.network.pack_start(self.gateway,False,True,0)
		self.network_dialog.vbox.add(self.network)
		self.network = gtk.HBox()
                self.label = gtk.Label("                   DNS1: ")
                self.network.pack_start(self.label,False,True,0)
		self.dns1 = gtk.Entry()
		self.network.pack_start(self.dns1,False,True,0)
		self.network_dialog.vbox.add(self.network)
		self.network = gtk.HBox()
                self.label = gtk.Label("                   DNS2: ")
                self.network.pack_start(self.label,False,True,0)
		self.dns2 = gtk.Entry()
		self.network.pack_start(self.dns2,False,True,0)
		self.network_dialog.vbox.add(self.network)

		self.dhcp.set_active(self.network_dhcp)
		self.ip.set_text(self.network_ip)
		self.netmask.set_text(self.network_netmask)
		self.gateway.set_text(self.network_gateway)
		self.dns1.set_text(self.network_dns1)
		self.dns2.set_text(self.network_dns2)
		self.network_devices.set_active(self.network_device)

		if self.dhcp.get_active() == True:
			self.dhcp.set_label("DHCP")
			self.ip.set_sensitive(False)
			self.netmask.set_sensitive(False)
			self.gateway.set_sensitive(False)
			self.dns1.set_sensitive(False)
			self.dns2.set_sensitive(False)
		else:
			self.dhcp.set_label("Static IP")
			self.ip.set_sensitive(True)
			self.netmask.set_sensitive(True)
			self.gateway.set_sensitive(True)
			self.dns1.set_sensitive(True)
			self.dns2.set_sensitive(True)

		self.dhcp.connect("toggled", self.check_network)
		self.ip.connect("grab-focus", self.check_network)
		self.netmask.connect("grab-focus", self.check_network)
		self.gateway.connect("grab-focus", self.check_network)
		self.dns1.connect("grab-focus", self.check_network)
		self.dns2.connect("grab-focus", self.check_network)
		self.network_dialog.connect("move-focus", self.check_network)

		self.network_dialog.show_all()
		response = self.network_dialog.run()
		if response == gtk.RESPONSE_ACCEPT:
			self.network_device = self.network_devices.get_active()
			self.network_name = self.network_devices.get_active_text()
			self.network_dhcp = self.dhcp.get_active()
			self.network_ip = self.ip.get_text()
			self.network_netmask = self.netmask.get_text()
			self.network_gateway = self.gateway.get_text()
			self.network_dns1 = self.dns1.get_text()
			self.network_dns2 = self.dns2.get_text()
			
			# Write Network Configuration File
			if self.dhcp.get_active() == True:			
				f = open('/tmp/networking','w')
				f.write('network --bootproto=dhcp --device='+str(self.network_name)+' --noipv6 --activate\n')
				f.close()
			else:
				f = open('/tmp/networking','w')
				f.write('network --bootproto=static --ip='+str(self.network_ip)+' --netmask='+str(self.network_netmask)+' --gateway='+str(self.network_gateway)+' --nameserver '+str(self.network_dns1)+','+str(self.network_dns2)+' --device='+str(self.network_name)+' --noipv6 --activate\n')
				f.close()

			self.network_dialog.destroy()
				

	# DHCP Button Toggle
	def check_network(self,widget,event=None):

		self.network_error = 0

		if self.dhcp.get_active() == True:
			self.dhcp.set_label("DHCP")
			self.ip.set_sensitive(False)
			self.netmask.set_sensitive(False)
			self.gateway.set_sensitive(False)
			self.dns1.set_sensitive(False)
			self.dns2.set_sensitive(False)
		else:
			self.dhcp.set_label("Static IP")
			self.ip.set_sensitive(True)
			self.netmask.set_sensitive(True)
			self.gateway.set_sensitive(True)
			self.dns1.set_sensitive(True)
			self.dns2.set_sensitive(True)

			if self.verify.check_ip(self.ip.get_text()) == False:
				self.MessageBox(self.window,"<b>Invalid IP Address!</b>",gtk.MESSAGE_ERROR)
				self.network_error = 1
		    	if self.verify.check_ip(self.netmask.get_text()) == False:
				self.MessageBox(self.window,"<b>Invalid Netmask!</b>",gtk.MESSAGE_ERROR)
				self.network_error = 1
			if self.verify.check_ip(self.gateway.get_text()) == False:
				self.MessageBox(self.window,"<b>Invalid Gateway!</b>",gtk.MESSAGE_ERROR)
				self.network_error = 1
			if self.verify.check_ip(self.dns1.get_text()) == False:
				self.MessageBox(self.window,"<b>Invalid DNS1 Address!</b>",gtk.MESSAGE_ERROR)
				self.network_error = 1
			if self.verify.check_ip(self.dns2.get_text()) == False:
				self.MessageBox(self.window,"<b>Invalid DNS2 Address!</b>",gtk.MESSAGE_ERROR)
				self.network_error = 1

		if self.network_error == 1:
			self.network_dialog.set_response_sensitive(gtk.RESPONSE_ACCEPT,False)
			return False	
		else:
			self.network_dialog.set_response_sensitive(gtk.RESPONSE_ACCEPT,True)
			return True


        # Appply Configurations to Kickstart File
        def apply_configuration(self,args):

		# FIPS 140-2 Configuration
		if self.fips_kernel.get_active() == True:			
			f = open('/tmp/hardening-post','a')
			# Enable FIPS 140-2 mode in Kernel
			f.write('\n/root/hardening/fips-kernel-mode.sh\n')
			f.close()
                else:
			f = open('/tmp/hardening-post','a')
			# Disable FIPS 140-2 mode in Kernel
			f.write('\ngrubby --update-kernel=ALL --remove-args="fips=1"\n')
			f.write('\n/usr/bin/sed -i "s/ fips=1//" /etc/default/grub\n')
			f.close()

		# Disable USB (nousb kernel option)
		if self.nousb_kernel.get_active() == True:
			f = open('/tmp/hardening-post','a')
			# Enable nousb mode in Kernel
			f.write('\ngrubby --update-kernel=ALL --args="nousb"\n')
			f.write('\n/usr/bin/sed -i "s/ quiet/quiet nousb/" /etc/default/grub\n')
			f.close()
		else:
			f = open('/tmp/hardening-post','a')
			# Disable nousb mode in Kernel
			f.write('\ngrubby --update-kernel=ALL --remove-args="nousb"\n')
			f.write('\n/usr/bin/sed -i "s/ nousb//" /etc/default/grub\n')
			f.close()

		# Set system password
		while True:
			self.get_password(self.window)
			if self.a == self.b:
				if len(self.a) == 0:
					return
				elif len(self.a) >= 14:
					self.passwd = self.a
					break
				else:
					self.MessageBox(self.window,"<b>Password too short! 14 Characters Required.</b>",gtk.MESSAGE_ERROR)
			else:
				self.MessageBox(self.window,"<b>Passwords Don't Match!</b>",gtk.MESSAGE_ERROR)
			
                self.error = 0

		if self.verify.check_hostname(self.hostname.get_text()) == False:
			self.MessageBox(self.window,"<b>Invalid Hostname!</b>",gtk.MESSAGE_ERROR)
			self.error = 1

		# Check Install Disks	
		self.install_disks = ""
		self.ignore_disks = ""
		for i in range(len(self.disk_info)):
			if eval("self.disk%d.get_active()"%(i)) == True:
				self.install_disks += self.disk_info[i][0]+","
			else:
				self.ignore_disks += self.disk_info[i][0]+","
		self.data["INSTALL_DRIVES"] = self.install_disks[:-1]
		self.data["IGNORE_DRIVES"] = self.ignore_disks[:-1]
		if self.install_disks == "":
			self.MessageBox(self.window,"<b>Please select at least one install disk!</b>",gtk.MESSAGE_ERROR)
			self.error = 1

		# Check LVM Partitioning
		if self.lvm_check(args) == False:
			self.error = 1

		# Write Kickstart File
		if self.error == 0:

			# Generate Salt
			self.salt = ''
			self.alphabet = '.abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
			for self.i in range(16):
    				self.index = random.randrange(len(self.alphabet))
    				self.salt = self.salt+self.alphabet[self.index]

			# Encrypt Password
			self.salt = '$6$'+self.salt
			self.password = crypt.crypt(self.passwd,self.salt)

			# Write Classification Banner Settings
			f = open('/tmp/classification-banner','w')
			f.write('message = "'+str(self.system_classification.get_active_text())+'"\n')
			if int(self.system_classification.get_active()) == 0 or int(self.system_classification.get_active()) == 1:
				f.write('fgcolor = "#FFFFFF"\n')
				f.write('bgcolor = "#007A33"\n')
			elif int(self.system_classification.get_active()) == 2:
				f.write('fgcolor = "#FFFFFF"\n')
				f.write('bgcolor = "#0033A0"\n')
			elif int(self.system_classification.get_active()) == 3:
				f.write('fgcolor = "#FFFFFF"\n')
				f.write('bgcolor = "#C8102E"\n')
			elif int(self.system_classification.get_active()) == 4:
				f.write('fgcolor = "#FFFFFF"\n')
				f.write('bgcolor = "#FF671F"\n')
			elif int(self.system_classification.get_active()) == 5:
				f.write('fgcolor = "#FFFFF"\n')
				f.write('bgcolor = "#F7EA48"\n')
			elif int(self.system_classification.get_active()) == 6:
				f.write('fgcolor = "#000000"\n')
				f.write('bgcolor = "#F7EA48"\n')
			else:
				f.write('fgcolor = "#FFFFFF"\n')
				f.write('bgcolor = "#007A33"\n')
			f.close()

			# Write Kickstart Configuration
			f = open('/tmp/hardening','w')
			f.write('network --device eth0 --bootproto dhcp --noipv6 --hostname '+self.hostname.get_text()+'\n')
			f.write('rootpw --iscrypted '+str(self.password)+'\n')
			f.write('bootloader --location=mbr --driveorder='+str(self.data["INSTALL_DRIVES"])+' --append="crashkernel=auto rhgb quiet audit=1" --password='+str(self.a)+'\n')
			f.close()
			f = open('/tmp/partitioning','w')
			if self.data["IGNORE_DRIVES"] != "":
				f.write('ignoredisk --drives='+str(self.data["IGNORE_DRIVES"])+'\n')
			f.write('zerombr\n')
			f.write('clearpart --all --drives='+str(self.data["INSTALL_DRIVES"])+'\n')
			if self.encrypt_disk.get_active() == True:
				f.write('part pv.01 --grow --size=200 --encrypted --cipher=\'aes-xts-plain64\' --passphrase='+str(self.passwd)+'\n')
			else:
				f.write('part pv.01 --grow --size=200\n')
			f.write('part /boot --fstype=ext4 --size=1024\n')
			if os.path.isdir('/sys/firmware/efi'):
				f.write('part /boot/efi --fstype=efi --size=200\n')
			f.write('volgroup vg1 --pesize=4096 pv.01\n')
			f.write('logvol / --fstype=ext4 --name=lv_root --vgname=vg1 --size=2048 --grow --percent='+str(self.root_partition.get_value_as_int())+'\n')
			f.write('logvol /home --fstype=ext4 --name=lv_home --vgname=vg1 --size=1024 --grow --percent='+str(self.home_partition.get_value_as_int())+'\n')
			f.write('logvol /tmp --fstype=ext4 --name=lv_tmp --vgname=vg1 --size=512 --grow --percent='+str(self.tmp_partition.get_value_as_int())+'\n')
			f.write('logvol /var --fstype=ext4 --name=lv_var --vgname=vg1 --size=512 --grow --percent='+str(self.var_partition.get_value_as_int())+'\n')
			f.write('logvol /var/log --fstype=ext4 --name=lv_log --vgname=vg1 --size=512 --grow --percent='+str(self.log_partition.get_value_as_int())+'\n')
			f.write('logvol /var/log/audit --fstype=ext4 --name=lv_audit --vgname=vg1 --size=512 --grow --percent='+str(self.audit_partition.get_value_as_int())+'\n')
			f.write('logvol swap --fstype=swap --name=lv_swap --vgname=vg1 --size=256 --maxsize=4096 --grow --percent='+str(self.swap_partition.get_value_as_int())+'\n')
			if self.opt_partition.get_value_as_int() >= 1:
				f.write('logvol /opt --fstype=ext4 --name=lv_opt --vgname=vg1 --size=512 --grow --percent='+str(self.opt_partition.get_value_as_int())+'\n')
			if self.www_partition.get_value_as_int() >= 1:
				f.write('logvol /var/www --fstype=ext4 --name=lv_www --vgname=vg1 --size=512 --grow --percent='+str(self.www_partition.get_value_as_int())+'\n')
			f.close()
			gtk.main_quit()


# Executes Window Display
if __name__ == "__main__":
	window = Display_Menu()
        gtk.main()
