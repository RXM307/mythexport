#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use MythTV;

use lib '/var/www/mythexport';
require includes;
my $connect = undef;
my $template = HTML::Template->new(filename => 'template/template.tmpl');
my ($script,$content) = "";

my $dir = '/usr/share/mythexport/configs';

opendir(my $dh, $dir) || die "can't opendir $dir: $!";
my @modules = grep { /\.pm/ && -f "$dir/$_" } readdir($dh);

$script = "<script type=\"text/javascript\">//<![CDATA[
function showConfigs(){
    document.getElementById(\"hidden\").style.display=\"block\";
}
function hideConfigs(){
    document.getElementById(\"hidden\").style.display=\"none\";
}//]]>
</script>";

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

# find all recordings
my $query = "SELECT title,subtitle,description,starttime,chanid
    FROM recorded order by title, subtitle, starttime";
my $query_handle = $connect->prepare($query);
$query_handle->execute()  || die "Unable to query mythexport table";

$content = "<form id=\"form\" action=\"otg_job.cgi\" method=\"post\">
<p>Choose a Location: <input type=\"text\" id=\"location\" name=\"location\" value=\"\" />&nbsp;<span class=\"red\">*</span><br />
<input type=\"radio\" id=\"otgFull\" name=\"type\" value=\"otgFull\" onclick=\"javascript:hideConfigs();\" checked=\"checked\" />Full Featured
<input type=\"radio\" id=\"otgLight\" name=\"type\" value=\"otgLight\" onclick=\"javascript:showConfigs();\" />Lightweight<br />
<span id=\"hidden\" style=\"display:none\">Choose an export profile: <select id=\"config\" name=\"config\" onchange=\"javascript:changeBlock();\">";

foreach my $config (@modules) {
    next if $config eq "ExportBase.pm";
    (my $class = $config) =~ s/.pm//;

    $content .= "<option value=\"$class\">$class</option>";
}

$content .= "</select><br /></span>Choose recordings to take on the go:
<table border=\"1\"><th></th><th>Title</th><th>Description</th><th>Start Time</th>";

while ( my ($title,$subtitle,$description,$starttime,$chanid) = $query_handle->fetchrow_array() ) {
    $content .= "<tr><td><input type=\"checkbox\" name=\"recordings\" value=\"$chanid|$starttime\" /></td>
    <td>$title";
    if ($subtitle)
    {
	    $content .= ": $subtitle";
    }
    $content .= "<td>$description</td><td>$starttime</td></tr>";
}

$content .= "</table><br /><span class=\"red\">* Are required</span>
<br /><input type=\"submit\" id=\"submitButton\" name=\"submitButton\" value=\"Submit\" />
</p></form>";

$template->param(SCRIPT => $script);
$template->param(CONTENT => $content);
$template->param(LOCATION => "otg");

print generateContentType(), $template->output;
exit(0);
