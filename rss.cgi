#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use MythTV;

use lib '/var/www/mythexport';
require includes;

my $connect = undef;
my $podcast_name = param("podcastName");

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

my $template = HTML::Template->new(filename => 'template/template.tmpl');

#my $script = "<script type=\"text/javascript\">//<![CDATA[
#function changeRSS(){
#var url = \"rss.cgi?podcastName=\" + document.getElementById(\"podcast\").value;
#window.location = url;
#}//]]>
#</script>";

my $bodyLoad = " onload=\"javascript:openRSS();\"";

my $script = "<script type=\"text/javascript\" src=\"includes/ajax.js\"></script>";

# find all podcast names
my $query = "SELECT distinct(podcastName) FROM mythexport";
my $query_handle = $connect->prepare($query);
$query_handle->execute()  || die "Unable to query mythexport table";

my $content = "<p><a id=\"link\" href=\"mythexportRSS.cgi?podcastName=$podcast_name\">Link to this feed</a>
&nbsp;Filter by Podcast Name:&nbsp;
<select id=\"podcast\" name=\"podcast\" onchange=\"javascript:openRSS();\">
<option value=\"\">All</option>";

while ( my $podcastName = $query_handle->fetchrow_array() ) {
	$content .= "<option value=\"$podcastName\"";
	if ($podcast_name eq $podcastName){
		$content .= " selected=\"selected\"";
	}
	$content .= ">$podcastName</option>";
}
$content .= "</select></p>
<div id=\"feed\" name=\"feed\">&nbsp;</div>";

#<object id=\"feed\" name=\"feed\" style=\"overflow:hidden;height:90%;100%;\" data=\"\" type=\"text/html\"></object>

$template->param(SCRIPT => $script);
$template->param(BODY_VARS => $bodyLoad);
$template->param(CONTENT => $content);
$template->param(LOCATION => "rss");

print generateContentType(), $template->output;
#print "Content-Type: text/html\n\n", $template->output;
exit(0);
