import change_names

ip_address = change_names.ip_address
domainname = change_names.domainname
sub_domain = change_names.sub_domain
smtp_username = change_names.smtp_username
smtp_password = change_names.smtp_password

pmta_config = f"""
http-access 0/0 monitor
http-access 0/0 monitor
http-access {ip_address} admin
http-access {ip_address} admin
postmaster admin@{domainname}
<domain {domainname}>
deliver-local-dsn yes
</domain>
#########################################################
# Settings for Backoff codes in SMTP reply
<smtp-pattern-list SMTPRESPONS>
        reply /421 PR(ct1)/ mode=backoff
        reply /^550 SC-001/ mode=backoff
        reply /420 Resources unavailable temporarily/ mode=backoff
        reply /^Resources unavailable temporarily/ mode=backoff
        reply /^421/ mode=backoff
        reply /^450/ mode=backoff
        reply /^try later/ mode=backoff
        reply /^553/ mode=backoff
        reply /^421/ mode=backoff
        reply /^550/ mode=backoff
        reply /^553/ mode=backoff
        reply /^550 SC-001/ mode=backoff
        reply /^421 4.7.0/ mode=backoff
        reply /^busy/ mode=backoff
        reply /^WSAECONNREFUSED/ mode=backoff
        reply /^WSAECONNRESET/ mode=backoff
        reply /^Connection attempt failed/ mode=backoff
</smtp-pattern-list>
#########################################################

############################################################################
# BEGIN: BACKOFF RULES
############################################################################

<smtp-pattern-list common-errors> 
        reply /generating high volumes of.* complaints from AOL/    mode=backoff 
        reply /Excessive unknown recipients - possible Open Relay/  mode=backoff 
        reply /^421 .* too many errors/                             mode=backoff 
        reply /blocked.*spamhaus/                                   mode=backoff 
        reply /451 Rejected/                                        mode=backoff 
</smtp-pattern-list>

<smtp-pattern-list blocking-errors>
        #
        # A QUEUE IN BACKOFF MODE WILL SEND MORE SLOWLY
        # To place a queue back into normal mode, a command similar
        # to one of the following will need to be run:
        # pmta set queue --mode=normal yahoo.com
        # or
        # pmta set queue --mode=normal yahoo.com/vmta1
        #
        # To use backoff mode, uncomment individual <domain> directives
        #
        #AOL Errors
        reply /421 .* SERVICE NOT AVAILABLE/ mode=backoff
        reply /generating high volumes of.* complaints from AOL/ mode=backoff
        reply /554 .*aol.com/ mode=backoff
        reply /421dynt1/ mode=backoff
        reply /HVU:B1/ mode=backoff
        reply /DNS:NR/ mode=backoff
        reply /RLY:NW/ mode=backoff
        reply /DYN:T1/ mode=backoff
        reply /RLY:BD/ mode=backoff
        reply /RLY:CH2/ mode=backoff
        #
        #Yahoo Errors
        reply /421 .* Please try again later/ mode=backoff
        reply /421 Message temporarily deferred/ mode=backoff
        reply /VS3-IP5 Excessive unknown recipients/ mode=backoff
        reply /VSS-IP Excessive unknown recipients/ mode=backoff
        #
        # The following 4 Yahoo errors may be very common
        # Using them may result in high use of backoff mode
        #
        reply /\[GL01\] Message from/ mode=backoff
        reply /\[TS01\] Messages from/ mode=backoff
        reply /\[TS02\] Messages from/ mode=backoff
        reply /\[TS03\] All messages from/ mode=backoff
        #
        #Hotmail Errors
        reply /exceeded the rate limit/ mode=backoff
        reply /exceeded the connection limit/ mode=backoff
        reply /Mail rejected by Windows Live Hotmail for policy reasons/ mode=backoff
        reply /mail.live.com\/mail\/troubleshooting.aspx/ mode=backoff
        #
        #Adelphia Errors
        reply /421 Message Rejected/ mode=backoff
        reply /Client host rejected/ mode=backoff
        reply /blocked using UCEProtect/ mode=backoff
        #
        #Road Runner Errors
        reply /Mail Refused/ mode=backoff
        reply /421 Exceeded allowable connection time/ mode=backoff
        reply /amIBlockedByRR/ mode=backoff
        reply /block-lookup/ mode=backoff
        reply /Too many concurrent connections from source IP/ mode=backoff
        #
        #General Errors
        reply /too many/ mode=backoff
        reply /Exceeded allowable connection time/ mode=backoff
        reply /Connection rate limit exceeded/ mode=backoff
        reply /refused your connection/ mode=backoff
        reply /try again later/ mode=backoff
        reply /try later/ mode=backoff
        reply /550 RBL/ mode=backoff
        reply /TDC internal RBL/ mode=backoff
        reply /connection refused/ mode=backoff
        reply /please see www.spamhaus.org/ mode=backoff
        reply /Message Rejected/ mode=backoff
        reply /Delivery report/ mode=backoff
        reply /refused by antispam/ mode=backoff
        reply /Service not available/ mode=backoff
        reply /currently blocked/ mode=backoff
        reply /locally blacklisted/ mode=backoff
        reply /not currently accepting mail from your ip/ mode=backoff
        reply /421.*closing connection/ mode=backoff
        reply /421.*Lost connection/ mode=backoff
        reply /476 connections from your host are denied/ mode=backoff
        reply /421 Connection cannot be established/ mode=backoff
        reply /421 temporary envelope failure/ mode=backoff
        reply /421 4.4.2 Timeout while waiting for command/ mode=backoff
        reply /450 Requested action aborted/ mode=backoff
        reply /550 Access denied/ mode=backoff
        reply /exceeded the rate limit/ mode=backoff
        reply /421rlynw/ mode=backoff
        reply /permanently deferred/ mode=backoff
        reply /\d+\.\d+\.\d+\.\d+ blocked/ mode=backoff
        reply /www\.spamcop\.net\/bl\.shtml/ mode=backoff
        reply /generating high volumes of.* complaints from AOL/    mode=backoff 
        reply /Excessive unknown recipients - possible Open Relay/  mode=backoff 
        reply /^421 .* too many errors/                             mode=backoff 
        reply /blocked.*spamhaus/                                   mode=backoff 
        reply /451 Rejected/                                        mode=backoff 
</smtp-pattern-list>

############################################################################
# END: BACKOFF RULES
############################################################################
#
# Settings per source IP address (for incoming SMTP connections)
#
<virtual-mta sharedserver.pool>

        #smtp-source-host {ip_address} {sub_domain}.{domainname}
</virtual-mta>

<virtual-mta server007.pool1> 
smtp-source-host {ip_address} {sub_domain}.{domainname}
</virtual-mta>
<virtual-mta-pool cloud1.pool1>
		virtual-mta server007.pool1
</virtual-mta-pool>

############################################################################
<smtp-user {smtp_username}>
  password {smtp_password}
  source {{server007}}
</smtp-user>
<source {{server007}}>
    default-virtual-mta  cloud1.pool1
</source>

############################################################################
<source 0/0>
	jobid-header Message-ID 
	process-x-job yes
	hide-message-source yes
	allow-unencrypted-plain-auth yes
	hide-message-source yes
	always-allow-relaying yes   # allow feeding
	add-received-header no
	process-x-virtual-mta yes   # allow selection of a virtual MTA
	max-message-size unlimited  # 0 implies no cap, in bytes
	smtp-service yes            # allow SMTP service
	require-auth true
	add-message-id-header yes
</source>   
############################################################################
smtp-listener {ip_address}:587
smtp-listener {ip_address}:587
############################################################################
# DKIM SELECTORS START 
domain-key cast,{domainname}, /etc/pmta/dkim/cast.{domainname}.pem 
# DKIM SELECTORS END 
############################################################################

			

#
# {{gmImprinter}} is a special queue used for imprinting Goodmail tokens.
#
<domain {{gmImprinter}}>
	max-events-recorded 150
	log-messages yes
	log-data no             # extremely verbose, for debugging only
	retry-after 15s
</domain>

<domain *>
	max-smtp-out    512       # max. connections *per domain*
	bounce-after    1d    # 4 days, 12 hours
	retry-after     2h      # 10 minutes
	max-msg-per-connection 500
	dk-sign yes
	dkim-sign yes
	#dkim-identity postmaster@{domainname}
	#dkim-identity-fallback @{domainname}
	log-commands    yes
	backoff-to-normal-after 10m
	backoff-to-normal-after-delivery true
	backoff-retry-after 30m
	backoff-max-msg-rate   500/m
	bounce-upon-no-mx yes
	smtp-pattern-list SMTPRESPONS
	use-starttls  yes
	require-starttls no
</domain>


#
# Port used for HTTP management interface
#
http-mgmt-port 1001

#
# IP addresses allowed to access the HTTP management interface, one
# per line
#


#
# Synchronize I/O to disk after receiving the message.  'false' yields
# higher performance, but the message may be lost if the system crashes
# before it can write the data to disk.
#
sync-msg-create false

#
# Synchronize I/O to disk after updating the message (e.g., to mark recipients
# handled).  'false' yields higher performance, but if the system crashes
# before it can write the data to disk, some recipients may receive multiple
# copies of a message.
#
run-as-root yes
sync-msg-update false

#
# Logging file
#
log-file /etc/pmta/log/pmta.log # logrotate is used for rotation
log-auto-rotation true
log-rotate 2                 # number of files; 0 disables rotation

#
# Accounting file(s)
#
<acct-file /etc/pmta/files/acct.csv>
#    move-to /opt/myapp/pmta-acct   # configure as fit for your application
record-fields delivery *,envId,jobId,bounceCat
move-interval 5m
delete-after 3d
max-size 50M
user-string from
</acct-file>

# transient errors (soft bounces)
<acct-file /etc/pmta/files/diag.csv>
move-interval 1d
delete-after 3d
records t
</acct-file>

#
# Spool directories
#
spool /var/spool/pmta

#<spool /var/spool/pmta>
#    deliver-only no
#</spool>
# EOF

host-name {domainname}
total-max-smtp-in 6000
"""
############################################################################ " > /etc/pmta/config

# Print the new file
# cat "check = vi /etc/pmta/config"
# print(config)


# config = """This is the contents of the large file."""

# Get the path to the directory where you want to store the file.
# file_path = "C:\\Users\\002GPU744\\Desktop\\code\\flask-tutorial\\go\\configv3.py"
# pmta_config_path = "/etc/pmta/config"

# Open a file object in the specified directory and write the contents of the string variable to the file.
with open("/etc/pmta/config", "w") as f:
  f.write(pmta_config)


##################################################################################################
########################################### BASHRC ###############################################
##################################################################################################

bash_rc = """
# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

alias deleteq='sh /etc/pmta/files/reports/deleteq.sh'
alias delvips='sh /etc/pmta/files/reports/delvips.sh'
alias delvipscnt='sh /etc/pmta/files/reports/delvipscnt.sh'
alias live='sh /etc/pmta/files/reports/live.sh'
alias livear='sh /etc/pmta/files/reports/livear.sh'
alias liveec='sh /etc/pmta/files/reports/liveec.sh'
alias mlogd='sh /etc/pmta/files/reports/mlogd.sh'
alias mlogr='sh /etc/pmta/files/reports/mlogr.sh'
alias passfromipt='sh /etc/pmta/files/reports/passfromipt.sh'
alias passfromipy='sh /etc/pmta/files/reports/passfromipy.sh'
alias test='sh /etc/pmta/files/reports/test.sh'
alias todall='sh /etc/pmta/files/reports/todall.sh'
alias todallip='sh /etc/pmta/files/reports/todallip.sh'
alias todcust='sh /etc/pmta/files/reports/todcust.sh'
alias todemailall='sh /etc/pmta/files/reports/todemailall.sh'
alias todemailcus='sh /etc/pmta/files/reports/todemailcus.sh'
alias todipcus='sh /etc/pmta/files/reports/todipcus.sh'
alias yesall='sh /etc/pmta/files/reports/yesall.sh'
alias yesallip='sh /etc/pmta/files/reports/yesallip.sh'
alias yescust='sh /etc/pmta/files/reports/yescust.sh'
alias yesemailall='sh /etc/pmta/files/reports/yesemailall.sh'
alias yesemailcus='sh /etc/pmta/files/reports/yesemailcus.sh'
alias yesipcus='sh /etc/pmta/files/reports/yesipcus.sh'
alias mlogec='sh /etc/pmta/files/reports/liveec.sh'
alias mlogar='sh /etc/pmta/files/reports/livear.sh'
alias mlog='sh /etc/pmta/files/reports/live.sh'
alias delallq='sh /etc/pmta/files/reports/delallq.sh'
alias ipcus='sh /etc/pmta/files/reports/ipcus.sh'




# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi
"""

bash_file_path = "/root/.bashrc"

with open(bash_file_path, "w") as f:
  f.write(bash_rc)