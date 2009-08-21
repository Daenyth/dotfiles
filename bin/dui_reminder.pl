#!/usr/bin/perl
use strict;
use warnings;

my @repeat_delays = ( .5, 1, 2.5, 5, 10, 10, .5, .5, .5 ); # Sleep N minutes between alerts

my $pid = fork;

die "Unable to fork" unless (defined $pid);
repeat_unemployment_alert() if ($pid == 0) # Child
exit;

sub repeat_unemployment_alert {
	my $sleep_length;
	while ($sleep_length = shift @repeat_delays) {
		unemployment_alert();
		sleep $sleep_length * 60;
	}
}

sub unemployment_alert {
	system('espeak -s 125 "File unemployment claim!"');
}
