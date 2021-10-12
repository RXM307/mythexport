#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use MythTV;

require includes;

my $description = param("description");
my $userjob = param("userjob");
my $config = param("config");
my $deletePeriod = param("deletePeriod");
my $podcastName = param("podcastName");
my $hostname = `hostname`;

$hostname =~ s/\s//g;

my $connect = undef;

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

my $template = HTML::Template->new(filename => 'template/template.tmpl');

my $query = "update settings set data=? where value=?";
my $query_handle = $connect->prepare($query);
$query_handle->execute($description,"UserJobDesc$userjob") || die "Unable to update user job description";

my $command = "mythexport_addjob starttime=%STARTTIME% chanid=%CHANID% config=$config deleteperiod=$deletePeriod podcastname=$podcastName";

$query = "update settings set data=? where value=?";
$query_handle = $connect->prepare($query);
$query_handle->execute($command,"UserJob$userjob") || die "Unable to update user job command";

$query = "update settings set data='1' where value=? and hostname=?";
$query_handle = $connect->prepare($query);
$query_handle->execute("JobAllowUserJob$userjob",$hostname) || die "Unable activate user job";

my $content = "<p>User Job has been sucessfully saved.</p>";

$template->param(CONTENT => $content);
$template->param(LOCATION => "setup");

print generateContentType(), $template->output;
exit(0);
