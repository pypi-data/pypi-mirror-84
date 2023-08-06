# domain_stats2

## Introduction
Domain_stats is a log enhancment utility that is intended help you find threats in your environment. It will identify the following possible threats in your environment.
 - Domains that were recently registered
 - Domains that no one in your organization has ever visited before
 - Domains with hostnames that appear to be random characters
 - Domains that the security community has identified as new (**Pending ISC Integration)
 - Domains that SANS ISC issues warning for (**Pending ISC Integration)

## The Old Domain_stats support
This version of domains_stats provides a number of benefits over the old version including performance, scalability, alerting, and isc integration. It does focus on born-on information which was the primary use of the tool and achieves its increaces performance by not processing the entire whois record. If you are looking for a copy of the old domain_stats which rendered ALL of the whois record rather than just the born-on information please let me make two suggestions.  First, that functionality has been moved to a new tool called "APIify" which can render any standard linux command in a json response for consumption. It also has improved caching and scalability over the old domain_stats. You can download [APIify HERE](https://github.com/markbaggett/apiify). You can also find the old version of domain_stats [in the releases section](https://github.com/MarkBaggett/domain_stats/releases/tag/1.0).

## Special Thanks
Thanks to the following individuals for their support, suggestions and inspirations without whom this version of domain_stats would not be possible.  
 - Justin Henderson [@securitymapper](https://twitter.com/securitymapper)
 - Don Williams [@bashwrapper](https://twitter.com/bashwrapper)
 - Dustin "cuz" Lee [@_dustinlee](https://twitter.com/_dustinlee)
 - Luke Flinders [@The1WhoPrtNocks](https://twitter.com/The1WhoPrtNocks)

## Ubuntu system preparation:
On Ubuntu you usually have to install Python PIP first. At a bash prompt run the following:
```
$ apt-get install python3-pip
```

## Install published package via PIP
```
$ python3 -m pip install domain-stats
```

## Install from latest source via PIP
Alternatively download the latest build from this github repo and install it as follows. Use PIP to install domain_stats rather than running setup.py.
```
$ git clone https://github.com/markbaggett/domain_stats
$ cd domain_stats
$ python3 -m pip install .
```

## Configure and Start

One the package is installed, make a directory that will be used to for storage of data and configuration files. Then run 'domain-stats-settings' and followd by 'domain-stats'. Both of those programs require you pass it the path to your data directory. The first command 'domain-stats-settings' creates or edits the required settings files. If you are not sure how to answer the questions just press enter and allow it to create the configuration files. The second command 'domain-stats' will run the server.

```
$ mkdir /mydata
$ domain-stats-settings /mydata
$ domain_stats /mydata
```

Here is what that looks like installed from source.

![alt text](./domain_stats.gif "Installation and use")

## Install as a container

To get a container up and running with domain_stats `docker build` passing the git file as a url. The `docker run` command must mount a directory into the container as the folder "host_mounted_dir" and to TCP port 8000 so you can access the server. In the example below port 10000 on the docker server is forwarded to the domain_stats server running inside the container on port 8000. Run docker run once with the -it option so you can go through the setup questions. If you do not know a better answer then the default just press ENTER. When it is finished run the container again with the -d and --name options as shown below. After that you can `docker stop domain_stats` and `docker start domain_stats` as needed.
 
```
$ docker build --tag domain_stats_image http://github.com/markbaggett/domain_stats.git
$ mkdir ~/dstat_data
$ docker run -it --rm -v ~/dstat_data:/host_mounted_dir -p 8000:10000 domain_stats_image
Set value for ip_address. Default=0.0.0.0 Current=0.0.0.0 (Enter to keep Current): 
Set value for local_port. Default=5730 Current=5730 (Enter to keep Current): 
Set value for workers. Default=3 Current=3 (Enter to keep Current): 
Set value for threads_per_worker. Default=3 Current=3 (Enter to keep Current): 
Set value for timezone_offset. Default=0 Current=0 (Enter to keep Current): 
Set value for established_days_age. Default=730 Current=730 (Enter to keep Current): 
Set value for mode. Default=rdap Current=rdap (Enter to keep Current): 
Set value for freq_table. Default=freqtable2018.freq Current=freqtable2018.freq (Enter to keep Current): 
Set value for enable_freq_scores. Default=True Current=True (Enter to keep Current):
Set value for freq_avg_alert. Default=5.0 Current=5.0 (Enter to keep Current): 
Set value for freq_word_alert. Default=4.0 Current=4.0 (Enter to keep Current): 
Set value for log_detail. Default=0 Current=0 (Enter to keep Current): 
Commit Changes to disk?y

$ docker run -d --name domain_stats -v ~/dstat_data:/host_mounted_dir -p 8000:8000 domain_stats_image
```

## To Run domain_stats as a service
If you are not going to use a docker you may want to run domain_stats as a server. After installing domain_stats as described above you can set it to run as a service on your system using the provided .service file in the data folder. It will be necessary to edit the domain_stats.service file and change the "WorkingDirectory" entry so that it points to the location you are storing your data. After editing the file add the ["domain_stats.service"](./domain_stats/data/domain_stats.service) file to your `/etc/systemd/system` folder.  Then use `systemctl enable domain_stats` to set it to start automatically. 

## SEIM Integration:
This varies depending upon the SEIM. The web interface is designed for your SEIM to make API calls to it.  It will respond back with a JSON responce for you it to consume.  Since many SEIM products are already configured to consume ZEEK logs another easy option is to add the ["domain_stats.zeek"](./domain_stats/data/domain_stats.zeek) module to your zeek configuration. Check the zeek domainstats.log for "NEW" domains and check for alerts such as "YOUR-FIRST-CONTACT".

### Example Zeek Configuration:

Assuming that zeek is installed in `/opt/zeek` and you don't already have custom scripts configured you can do this:

 - Place domain_stats.zeek in a new directory called `/opt/zeek/share/zeek/policy/custom-script`
 - Add `@load ./domain_stats` to a new file called `/opt/zeek/share/zeek/policy/custom-script/__load__.zeek`  
 - Add `@load custom-scripts` to `/opt/zeek/share/zeek/site/local.zeek`
 - Make sure curl is installed. This is a dependency of zeeks ActiveHTTP module. (try `apt install curl`)
 - If you are running zeek in a VM you need uncomment `redef ignore_checksums = T;` in domain_stats.zeek
 - Start domain_stats server
 - In zeekctl `deploy`
 - Confirm domain_stats appears in loaded_scripts.log


## Using domain_stats

This is a complete rewrite and new approach to managing baby domains in your organization.  Based on feedback from the community Domain_stats was really only used for baby domain information.  This new iteration focuses on that data and how to make it useful.  In this process it now tracks "FIRST CONTACT" so you know when your organization and/or the ISC has seen that domain before.

The domain stats client is focused on quickly giving you 5 pieces of data for every domain name you ask it for.  That is when the domain was first seen by you, when it was first seen by the security community and when it was first seen by the web.

SEEN_BY_YOU - Values: Date First Seen by you

SEEN_BY_ISC  - Values: NA or Date First seen by ISC  (NA indicates that it was resolved by the local database no ISC is required.)

SEEN_BY_WEB - Values: CreationDate

CATEGORY    - NEW or ESTABLISHED  (indicating whether it is less than 2 years old since the SEEN_BY_WEB date)

ALERT      -  List of alerts regarding this domain.   Including:
              YOUR-FIRST-CONTACT  - This request is first time you have ever seen this domain on your network
              ISC-FIRST-CONTACT  - This is the first time any domain_stats user has seen this domain on their network
              <other>  - The ISC may add other alert for a domain 


Here are some examples of how these are useful.
If your SIEM sees a request for google.com that is not a new domain and has been established for may years. Your response may look like this:

```
student@573:~/Documents/domain_stats2$ wget -q -O- http://127.0.0.1:8000/google.com
{"seen_by_web": "1998-10-08 07:30:02", "seen_by_isc": "NA", "seen_by_you": "2019-12-24 15:30:02", "category": "ESTABLISHED", "alerts": ['YOUR-FIRST-CONTACT']}
```
When the domain has been around for more than two years domain stats responds and tells you that is an "ESTABLISHED" domain. Notice that ALERTS is set to "YOUR-FIRST-CONTACT". Since this is a brand new domain stats installation this is the first time my organization has ever queried google. You will only see "YOUR-FIRST-CONTACT" once for each domain. Also "SEEN_BY_ISC" is set to NA indicating that this query was resolved locally by your domain client and it didn't need to talk to the ISC. That means that this is a well known established domain that has been around for a long time and your local client has it in its database. Generally speaking you can most likely ignore the NA SEEN_BY_ISC domains.
 
Lets look at another domain.  Look at markbaggett.com.

```
student@573:~/Documents/domain_stats2$ wget -q -O- http://127.0.0.1:8000/markbaggett.com
{"seen_by_web": "2015-12-12 19:34:59", "seen_by_isc": "2019-06-08 10:03:17", "seen_by_you":"2019-06-08 10:03:17", "category": "ESTABLISHED", "alerts": ['YOUR-FIRST-CONTACT'] 
```
The domain markbaggett.com wasn't in the local database on my server so it had to go off and ask the SANS Internet Storm Center server for that information. It got back a "seen_by_web" date of 12-12-2015. This is the domains registration date. The category indicates that this is an "ESTABLISHED" domain. It will added to the client database for all future queries unless any additional alerts were set by the ISC. Domains that have an alert associated with them will be cached for 24 hours. Then another query will be sent to the ISC.  This process is repeated until the isc alert for that domain is cleared. Notice there is a date for "seen_by_isc". That is the first time ANYONE using domain_stats queried the central server for that domain. Someone using domain stats ask about that domain that back on July 8th. That is a few months ago so it isn't brand new to the community. If no one using domain stats had ever asked about that domain there would have been an additional alert that says "ISC-FIRST-CONTACT". Last we can see it is again the YOUR-FIRST-CONTACT alert for our organization.   

A domain with a very recent "seen_by_web", "seen_by_isc" and "seen_by_you" date should be investigated. The vast majority of domains have been around for a few years before they are stable and gain popularity.  Domains used by attackers are usually established shortly before they are used. 

Anytime you see a "???-FIRST-CONTACT" on a domain that has been running for some period of time it is at the least a good thing to be aware of.  If it is the FIRST CONTACT for both you and the community then that is even more interesting. (Unless of course you are of the few beta testers where the community is very small and not much different that seen_by_you.)


![Overview](overview.jpg)


The goal is to push as much of the "ESTABLISHED" data to the client local lan as possible. This minimizes network traffic keeps as much data as possible on the client network. When contacting the central server it will periodically inform the client to pull list of new domains and add them to the client established database.

The domain_stats.yaml file has many useful configurations includeing the "mode".  For now it is in "rdap" mode by default.  Which means instead of going to the ISC for domains it will do RDAP queries.  This is a useful stop gap measure but lacks the additional alerting providing by the ISC.

More data to come later as features and functions are more firmly established.

You can check the efficiency of your domain_stats server cache with the following request.

$ wget -q -O- http://127.0.0.1:8000/stats
Will show statistics on the efficiency of the memory cache and the database hit rate.

$ wget -q -O- http://127.0.0.1:8000/showcache
Will dump the cache

# Configuration

domain_stats behavior can be changed my modifying domain_stats.yaml that is in its setup directory.  In that file you will find the following useful items.

- You can adjust the maximum number of items domain stats will keep in memory cache with cached_max_items. Each record consumes 32 bytes so 65536 assumes you can spare about 2MB of memory for the cache. For performance reasons this number should be a power of 2.
```
cached_max_items: 65536
```
- You can specify the name of the database with database_file.
```
database_file: domain_stats.db
```
- What IP address do you want domain stats to listen on? 0.0.0.0 means all public and private IP addresses. You should change this to 127.0.0.1 if you run domain_stats on the same server that is doing the request to the API.
```
local_address: 0.0.0.0
```
- Set which TCP port do you want the server to listen on with local_port
```
local_port: 8000
```
- The name of the file where you want to store the memory cache on disk when the tool exists. Keep this in a SECURE location.
```
memory_cache: domain_stats.cache
```
- The prohibited_tlds is a section that lists top level domains that will not be sent to the central server for resolution. List each domain beneith the word "prohibited_tlds" (Yes i know they are not TLDS) with a **dash space** in front of them.
```
prohibited_tlds:
- yourdomainhere.local
```
- server_name is the hostname of the central domain stats server use to lookup host that are not in the database when in isc mode
```
server_name: domain_stats.isc.sans.edu
```
- This is the tcp port the central isc domain stats server
```
server_port: 4100
```
- Where to get new domain expiration data from when domain_stats_db_admin -u is run
```
target_updates: https://raw.githubusercontent.com/MarkBaggett/domain_stats/master/data
```
- ALL timestamps are UTC if you want "seen_my_you" to be in your local timezone make that adjustment here. Example EST=-5 EDT=-4, etc.  The server does not change this value automatically during daylight savings time.
```
timezone_offset: 0
```
- Control the amount of data logged with log_detail.  0=off, 1=on, 2=debug
```
log_detail: 0
```
- Mode can be isc or rdap. rdap is local resolution with no community data. isc has the good stuff.
```
mode: rdap
```

# RDAP vs ISC Support
They each have their own advantages.  We will discuss them here.

- RDAP works today! The ISC support engine is still in the works.
- If you trust your ISP, and commercial and government entities that support DNS infrastructure with your DNS queries but not the ISC then RDAP will let you live in your bubble.
- As of August 2019 RDAP ICANN requires providers support for gTLDs (Top Level: .com, .gov, etc) and not ccTLDs (country code :google.com.au, .ga.us, etc) or eTLDs (Effective TLDs: Where we register domains). You basically can't resolve those domains until ISC support is enabled.  More info on RDAP Support timelines are [HERE]('https://www.icann.org/resources/pages/rdap-background-2018-08-31-en')
 - ISC support will support all domains and not be limited by RDAP support. 
 - ISC will provide additional alerting on domains

# ISC API Specification 
API requests look like this
```
{"command":  <command string>,  additional arguments depending upon command}
```
Valid COMMANDS include "CONFIG", "STATUS", and "QUERY"



### **CONFIG command requests configuration options the ISC would like to enforce on the client**
request:
```
{"command": "config"}
```
response:
```
{"min_software_version": "major.minor string",  "min_database_version", "major.minor string", prohitited_tlds:["string1","string2"]}
```
- clients will not query ISC for Domains listed in prohibited_tlds.   Examples may be ['.local', '.arpa']
- If min_software_version is higher than the client software version it causes the software to abort
- if min_database_version is higher than database version it forces the client to download new domains from github.com/markbaggett and add it to its local database



### **STATUS command allows the clients to tell the ISC how they are doing and see if they can continue.  This can be used to tune client efficiency and reduce ISC requests.**
Request:
```
{"command":"status", "client_version":client_version, "database_version":database_version, "cache_efficiency":[cache.hits, cache.miss, cache.expire], "database_efficiency":[database_stats.hits, database_stats.miss]}
```
Response:
```
{"interval": "integer number of minutes ISC wishes to wait until next status update", "deny_client": "client message string"}
```
- interval: The interval tells the client how many minutes to wait before sending another status updates
- deny_client: If set aborts the client with the specified message



### **QUERY command allows clients to query a domain record.**
Requests:
```
{"command": "query", "domain": "example.tld"}
```
RESPONSES (two possible):
##### A success response looks like this:

```
{"seen_by_web": '%Y-%m-%d %H:%M:%S', "expires": '%Y-%m-%d %H:%M:%S', "seen_by_isc":'%Y-%m-%d %H:%M:%S', "alerts":['list','of','alerts]}
```
   - seen_by_web is the domains creation date from the whois record. The time stamp must be in '%Y-%m-%d %H:%M:%S' format
   - expires is the date that the domains registration expires from the whois record. The timestamp must be in '%Y-%m-%d %H:%M:%S' format
   - seen_by_isc is the date that the first domain_stats client requested this domain from the isc. If this was the first request it will have the current date and time and 'ISC-FIRST-CONTACT' will be added to the alerts. The timestamp must be in '%Y-%m-%d %H:%M:%S' format.
   - Alerts must include "ISC-FIRST-CONTACT" if this is the first time anyone has ever queried ISC for this domain
   - Setting any additional alerts limits will cause the client record to not be commited to the database. Instead it is cached for 24 hours on the client.  After 24 hours the client will query the isc again.
##### An error response looks like this:

```
{"seen_by_web":"ERROR", "expires":"ERROR", "seen_by_isc":<integer specifying cache time to live>, "alerts":['alerts','for','that','domain']}
```
   - seen_by_web and expires must be set to "ERROR" when an error has occured.
   - Error time to live tell the client how long to cache and reuse the error for that domain.
   - Integer > 0 - will cache the error for that many hours
   - 0 - will not cache the error at all
   - -1 - will cache it such that it does not expire, but the domain can still drop out of cache based on LRU algorithm
   - -2 - PERMANENT cache entry.  Will never expire.  DANGEROUS. Use with caution.
    
