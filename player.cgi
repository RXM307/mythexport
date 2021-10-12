#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use Config::Simple;
use MythTV;

require includes;

my $connect = undef;
my $file = "/etc/mythtv/mythexport/mythexport.cfg";
my ($script,$content) = "";
my $template = HTML::Template->new(filename => 'template/html5.tmpl');

# if we have a valid config
if(-e $file && -s $file > 5){
    my $cfg = new Config::Simple();
    $cfg->read($file) || die $cfg->error();

    my $myth = new MythTV();
    # connect to database
    $connect = $myth->{'dbh'};

    my $id = param("id");

    # find the exported recordings
    my $query = "SELECT file FROM mythexport where id=?";
    my $query_handle = $connect->prepare($query);
    $query_handle->execute($id)  || die "Unable to query mythexport table";

    $content = "<p>This page is a work in progress, it may work for your Anroid device or iPhone.<br />";

    while ( my $file = $query_handle->fetchrow_array() ) {
	    $content .= "<video width=\"480\" height=\"320\" autobuffer controls onClick=\"this.play();\">
        <source  src=\"/mythexport/video/$file\" /></video>";
    }

    $content .= "</p>";
}
else{
    $content = "<p>Missing or Invalid configuration file, please create one.</p>";
}

$template->param(CONTENT => $content);

print generateContentType(), $template->output;
exit(0);
