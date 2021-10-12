#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use HTML::Template;
use Config::Simple; 

require includes;

my $delete = param("delete");
my $title = param("title");
my $content = "";
my $file = "/etc/mythtv/mythexport/mythexport.cfg";
my $cfg = new Config::Simple();

if(-e $file){
    if(-s $file < 6){
        unlink($file);
    }
    else{
        $cfg->read($file); 
    }
}

my $template = HTML::Template->new(filename => 'template/template.tmpl');

my $location = param("location"); 

$cfg->param("dir", $location);
$cfg->write($file) || die $cfg->error();
#$cfg->save($file) || die $cfg->error();

$content = "<p>Configuration has been sucessfully saved.<br /><br />
You may need to execute the following commands:<br />
sudo mkdir -p $location && sudo chmod 775 $location && sudo chown mythtv:mythtv $location && sudo ln -s -f $location /var/www/mythexport/video<br /><br />
You will also need to move any exported recordings that occured using a different directory.
</p>";

$template->param(CONTENT => $content);
$template->param(LOCATION => "setup");

print generateContentType(), $template->output;
exit(0);
