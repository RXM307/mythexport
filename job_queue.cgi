#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use MythTV;

use lib '/var/www/mythexport';
require includes;

my $connect = undef;

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};

my $template = HTML::Template->new(filename => 'template/template.tmpl');

my $script = "<script type=\"text/javascript\" src=\"includes/ajax.js\"></script>
<script type=\"text/javascript\">//<![CDATA[
function confirmDeleteJob(id){
var answer = confirm(\"Are you sure you want to delete this job?\");
if (answer){
	deleteJob(id);
	return true;
}
else
	return false;
}//]]>
</script>";

# find the old recordings
my $query = "SELECT id, type, description FROM mythexport_job_queue order by id";
my $query_handle = $connect->prepare($query);
$query_handle->execute()  || die "Unable to query mythexport_job_queue table";

my $content = "<p>Job Queue<br /><br /><table border=\"1\"><th>Job</th><th>Description</th>";

while ( my ($id,$type, $description) = $query_handle->fetchrow_array() ) {
	$content .= "<tr><td>$type</td><td>$description</td>
	<td><a href=\"#\" onclick=\"javascript:return confirmDeleteJob($id);\">Delete</a></td>
	</tr>";
	#if($type eq "delete"){
	#    my $sub_query = "SELECT type FROM mythexport_job_queue order by id";
    #    my $sub_query_handle = $connect->prepare($sub_query);
    #    $query_handle->execute()  || die "Unable to query mythexport_job_queue table";
	#}
}

$content .= "</p></table>";

$template->param(SCRIPT => $script);
$template->param(CONTENT => $content);
$template->param(LOCATION => "file");

print generateContentType(), $template->output;
exit(0);
