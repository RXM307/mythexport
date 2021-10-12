#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use Config::Simple; 

use lib '/var/www/mythexport';
require includes;

my $file = "/etc/mythtv/mythexport/mythexport.cfg";
my $template = HTML::Template->new(filename => 'template/template.tmpl');
my $location = "";

# if we have a valid config
if(-e $file && -s $file > 5){
    my $cfg = new Config::Simple();
    $cfg->read($file) || die $cfg->error();; 

    $location = $cfg->param("dir");
}

my $content = "<form id=\"form\" action=\"save_system_setup.cgi\" method=\"post\"><p>Update the location where you would like MythExport to store exported recordings:<br />";

$content .= "<input type=\"text\" id=\"location\" name=\"location\" value=\"$location\" />&nbsp;<span class=\"red\">*</span><br /><br />
<span class=\"red\">* Are required</span>
<br /><input type=\"submit\" id=\"submitButton\" name=\"submitButton\" value=\"Submit\" /></p></form></table>";

$template->param(CONTENT => $content);
$template->param(LOCATION => "file");

print generateContentType(), $template->output;
exit(0);
