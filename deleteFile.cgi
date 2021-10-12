#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use Config::Simple;
use MythTV;

use lib '/var/www/mythexport';
require includes;

my $connect = undef;
my $id = param("id");
my $file = "/etc/mythtv/mythexport/mythexport.cfg";

my $cfg = new Config::Simple();
$cfg->read($file) || die $cfg->error();

my $dir = $cfg->param("dir");
$dir =~ s/\/$//;

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

my $template = HTML::Template->new(filename => 'template/template.tmpl');

my $query = "SELECT file FROM mythexport where id=?";
my $query_handle = $connect->prepare($query);
$query_handle->execute($id) || die "Unable to query mythexport table";

my $file = $query_handle->fetchrow_array();

# add delete job
$query = "insert into mythexport_job_queue(type,param,id,description) values ('delete',?,NULL,?)";
$query_handle = $connect->prepare($query);
$query_handle->execute($id,$file) || die "Unable to query mythexport table";

my $content = "DONE";

$template->param(CONTENT => $content);
$template->param(LOCATION => "file");

print generateContentType(), $template->output;
exit(0);
