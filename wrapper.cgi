#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;

use lib '/var/www/mythexport';
require includes;

my $podcast_name = param("podcastName");

my $template = HTML::Template->new(filename => 'template/wrapper.tmpl');

my $content = "<object style=\"overflow:auto;height:90%;100%;\" data=\"mythexportRSS.cgi?podcastName=$podcast_name\" type=\"text/html\"></object>";

$template->param(CONTENT => $content);

print generateContentType(), $template->output;
exit(0);
