#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use Config::Simple;
use MythTV;

use lib '/var/www/mythexport';
require includes;

my $connect = undef;
my $location = param("location");
my $type = param("type");
my $config = param("config");
my @recordings = param("recordings");

my ($chanid,$starttime) = "";
my $counter = 0;

foreach (@recordings){
	if($_ =~ m/(.*)\|(.*)/){
		$chanid .= "$1|";
		$starttime .= "$2|";
	}
	$counter++;
}

$chanid =~ s/\|$//;
$starttime =~ s/\|$//;

my $param = "chanid=$chanid&starttime=$starttime&config=$config&exportdir=$location";
my $otgVersion = "";

if($type eq "otgFull"){
	$otgVersion = "otg-full";
}
elsif($type eq "otgLight"){
	$otgVersion = "otg-lightweight";
}

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

my $template = HTML::Template->new(filename => 'template/template.tmpl');

# add OTG job
my $query = "insert into mythexport_job_queue(type,param,id,description) values (?,?,NULL,?)";
my $query_handle = $connect->prepare($query);
$query_handle->execute($otgVersion,$param,"Total Recordings: $counter") || die "Unable to add OTG job to queue table";

my $content = "OTG Job has been added to the Queue.";

$template->param(CONTENT => $content);
$template->param(LOCATION => "otg");

print generateContentType(), $template->output;
exit(0);
