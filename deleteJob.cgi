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

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

my $template = HTML::Template->new(filename => 'template/template.tmpl');

# add delete job
my $query = "delete from mythexport_job_queue where id=?";
my $query_handle = $connect->prepare($query);
$query_handle->execute($id) || die "Unable to query mythexport table";

my $content = "DONE";

$template->param(CONTENT => $content);
$template->param(LOCATION => "file");

print generateContentType(), $template->output;
exit(0);
