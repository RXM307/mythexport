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

    $script = "<script type=\"text/javascript\" src=\"includes/ajax.js\"></script>
    <script type=\"text/javascript\">//<![CDATA[
    function confirmDelete(id){
    var answer = confirm(\"Are you sure you want to delete this file?\");
    if (answer){
	    deleteFile(id);
	    return true;
    }
    else
	    return false;
    }//]]>
    </script>";

    # find the old recordings
    my $query = "SELECT file, title, subtitle, airDate, podcastName, id, file FROM mythexport order by pubDate desc";
    my $query_handle = $connect->prepare($query);
    $query_handle->execute()  || die "Unable to query mythexport table";

    $content = "<p>Exported Files<br /><table border=\"1\"><th>Recording</th><th>Podcast</th><th>Delete?</th>";

    while ( my ($file,$title,$subtitle,$airDate,$podcastName,$id,$file) = $query_handle->fetchrow_array() ) {
	    $content .= "<tr><td><a href=\"video/$file\">$title";
	    if ($subtitle)
	    {
		    $content .= ": $subtitle";
	    }
	    else{
		    $content .= ": $airDate";
	    }
	    $content .= "</a></td><td>$podcastName</td><td><a href=\"#\" onclick=\"javascript:return confirmDelete($id);\">Delete</a></td></tr>";
    }

    $content .= "</p></table>";
}
else{
    $content = "<p>Missing or Invalid configuration file, please create one.</p>";
}

$template->param(SCRIPT => $script);
$template->param(CONTENT => $content);
$template->param(LOCATION => "file");

print generateContentType(), $template->output;
exit(0);
