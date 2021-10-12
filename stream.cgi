#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use Config::Simple;
use MythTV;

use lib '/var/www/mythexport';
require includes;

my $connect = undef;
my $file = "/etc/mythtv/mythexport/mythexport.cfg";
my ($script,$content) = "";
my $template = HTML::Template->new(filename => 'template/template.tmpl');

# if we have a valid config
if(-e $file && -s $file > 5){
    my $cfg = new Config::Simple();
    $cfg->read($file) || die $cfg->error();

    my $myth = new MythTV();
    # connect to database
    $connect = $myth->{'dbh'};

    # find the exported recordings
    my $query = "SELECT title, subtitle, airDate, podcastName, id, file FROM mythexport order by pubDate desc";
    my $query_handle = $connect->prepare($query);
    $query_handle->execute()  || die "Unable to query mythexport table";

    $content = "<p>Exported Files<br /><table border=\"1\"><th>Recording</th>";

    while ( my ($title,$subtitle,$airDate,$podcastName,$id,$file) = $query_handle->fetchrow_array() ) {
	    $content .= "<tr><td><a href=\"player.cgi?id=$id\">$title";
	    if ($subtitle)
	    {
		    $content .= ": $subtitle";
	    }
	    else{
		    $content .= ": $airDate";
	    }
	    $content .= "</a></td></tr>";
    }

    $content .= "</p></table>";
}
else{
    $content = "<p>Missing or Invalid configuration file, please create one.</p>";
}

$template->param(CONTENT => $content);
$template->param(LOCATION => "file");

print generateContentType(), $template->output;
exit(0);
