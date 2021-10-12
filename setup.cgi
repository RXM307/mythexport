#!/usr/bin/perl

use strict;
use lib '/usr/share/mythexport/configs';
use lib '/usr/share/mythexport';
use CGI qw(:standard);
use HTML::Template;
use MythTV;

require includes;

my $myth = new MythTV();
my $connect = undef;
# connect to database
$connect = $myth->{'dbh'};

my $dir = '/usr/share/mythexport/configs';

my $template = HTML::Template->new(filename => 'template/template.tmpl');

# find the user jobs
my $query = "SELECT data from settings where value like ?";
my $query_handle = $connect->prepare($query);
$query_handle->execute("UserJobDesc%")  || die "Unable to query mythexport_job_queue table";

opendir(my $dh, $dir) || die "can't opendir $dir: $!";
my @modules = grep { /\.pm/ && -f "$dir/$_" } readdir($dh);

my $content = "<form action=\"setupsave.cgi\" method=\"post\"><p>
    Choose a Configuration:<br /><table border=\"1\">
    <tr><th>&nbsp;</th><th>Name</th><th>Version</th><th>Description</th><th>Devices</th><th>Notes</th></tr>";


foreach my $config (@modules) {
    next if $config eq "ExportBase.pm";
    (my $class = $config) =~ s/.pm//;
    require $config;

    my $object = new $class();
    my $description = $object->Description();
    my $devices = $object->Devices();
    my $notes = $object->Notes();
    my $version = $object->Version();
    
    $content .= "<tr><td><input type=\"radio\" name=\"config\" id=\"$class\" value=\"$class\" /></td>
        <td>$class</td><td>$version</td><td>$description</td><td>$devices</td><td>$notes</td></tr>";
}

$content .= "</table><br />Don't see a usable config? <a href=\"http://www.baablogic.net/mythexport/\">Check here for new configuration releases and updates</a><br /><br />";

$content .= "Select a User Jobs:<br />";
my $i = 1;
while(my ($description) = $query_handle->fetchrow_array()) {
    $content .= "<input type=\"radio\" id=\"radio$i\" name=\"userjob\" value=\"$i\" />$description<br />";
    $i++;
}

$content .= "Description: <input type=\"text\" id=\"description\" name=\"description\" value=\"\" /><br />
<span style=\"color:red;\">*WARNING: Proceeding will overwrite any data for this User Job</span><br /><br />
Delete Period: <input type=\"text\" id=\"deletePeriod\" name=\"deletePeriod\" value=\"\" />&nbsp;(number of days to keep exported files, empty will never delete)<br />
Podcast Name: <input type=\"text\" id=\"podcastName\" name=\"podcastName\" value=\"\" />&nbsp;(optional)<br /><br />
<input type=\"submit\" id=\"submit\" name=\"submit\" value=\"Submit\" />
</p></form>";

$template->param(CONTENT => $content);
$template->param(LOCATION => "setup");

print generateContentType(), $template->output;
exit(0);
