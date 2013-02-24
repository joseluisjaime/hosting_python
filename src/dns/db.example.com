$TTL	86400
example.com.	IN	SOA	hosting.example.com. hosting.example.com. (
			1		; Serial
			604800		; Refresh
			86400		; Retry
			2419200		; Expire
			86400 )		; Negative Cache TTL
;
			IN	NS	hosting.example.com.
$ORIGIN example.com.
hosting		A	192.168.1.16
