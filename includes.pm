#!/usr/bin/perl

use strict;
use CGI qw(:standard);

sub generateContentType{
    if ($ENV{HTTP_ACCEPT} =~ /(^|,)(\s)*application\/xhtml\+xml(\s)*(,|$)/ || $ENV{HTTP_USER_AGENT} =~ /W3C_Validator/){
        #return "Content-Type: application/xhtml+xml\n\n";
        return "Content-Type: text/html\n\n";
    }
    else{
        return "Content-Type: text/html\n\n";
    }
}

1;
