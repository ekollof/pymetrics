=== Synopsis ===
	getmetrics.py <host> <metric type> <parameter> <treshold>

=== Dependancies ===
	paramiko (voor SSH)
	SSH private key voor remote host (voor passwordless ssh naar andere hosts) als bestandsnaam 'key' in script root

=== Uitvoer ===
	Als waarde beneden treshold, TRUE, anders FALSE

=== Metric types ===

* load - load average <0 current, 1 5 min avg, 2 15 min avg)
* diskfree - % ruimte vrij op disk op <parameter>
* inodefree - % inodes vrij op disk <parameter>
* swapinuse - % swap in use (0 as parameter)
* iops - IOPS on disk param
* netload - mb/sec on nic <parameter>
* test - maakt verbinding met host en geeft altijd TRUE (en de parameter) als een commando kan worden uitgevoerd op de host. Dit is om te testen of de host kan worden bereikt en dat de ssh key e.a. werkt
