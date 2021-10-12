#!/usr/bin/perl
use DBI;
use DBD::mysql;
use MythTV;
use XML::RSS;
use CGI qw(:standard);
use HTTP::Date;
use strict;

# create an RSS 2.0 file
my $rss = new XML::RSS (version => '2.0');
my $connect = undef;

my $myth = new MythTV();
# connect to database
$connect = $myth->{'dbh'};
my $ip = $ENV{'HTTP_HOST'};
my $http = "http://";
# Fixes bug LP:288186
if($ENV{'HTTP_X_FORWARDED_HOST'} ne ""){ 
    $ip = $ENV{'HTTP_X_FORWARDED_HOST'};
}
if($ENV{'HTTPS'} eq "on"){
    $http = "https://";
}

my $podcast_name = param("podcastName");
my $title = "MythCast";
my $currentDate = time2str(time());
my ($query, $query_handle);
if($podcast_name ne ""){
    $title .= " [$podcast_name]";
	$query = "select file, title, subtitle, description, pubDate, airDate from mythexport where podcastName like ? order by pubDate desc";
	$query_handle = $connect->prepare($query);
	$query_handle->execute($podcast_name) || die "Unable to get exported recordings from database.";
}
else{
	$query = "select file, title, subtitle, description, pubDate, airDate from mythexport order by pubDate desc";
	$query_handle = $connect->prepare($query);
	$query_handle->execute() || die "Unable to get exported recordings from database.";
}

$rss->channel(title          => "$title",
               link           => "$http$ip/mythexport/video/",
               language       => 'en',
               description    => 'Exported MythTV Recordings',
               rating         => '(PICS-1.1 "http://www.classify.org/safesurf/" 1 r (SS~~000 1))',
               pubDate        => $currentDate,
               lastBuildDate  => $currentDate
               );

while (my @data = $query_handle->fetchrow_array()) {
	#print "LOOP!";
	my $rss_file=$data[0];
	my $rss_title=$data[1];
	my $rss_subtitle=$data[2];
	my $rss_desc=$data[3];
	my $rss_pubDate = $data[4];
    my $rss_airDate = $data[5];
	my $title = "$rss_title - $rss_subtitle";
	my $file_len = -s "/var/www/mythexport/video/$rss_file";
	if ($rss_subtitle eq ""){
        my $temp_date = $rss_airDate;
        $temp_date =~ s/\-/\//g;
        $temp_date =~ s/\s00\:00\:00//;
        $title .= $temp_date;
    }
    my $temp_pubDate = str2time($rss_pubDate);
    $temp_pubDate = time2str($temp_pubDate);
	$rss->add_item(title => "$title",
        # creates a guid field with permaLink=true
        # alternately creates a guid field with permaLink=false
        # guid     => "gtkeyboard-0.85"
        enclosure   => { url=>"$http$ip/mythexport/video/$rss_file", type=>"video/mpeg", length=>"$file_len"},
        description => "$rss_desc",
		pubDate 	=> "$temp_pubDate",
		guid        => "$rss_file",
		);
}


print "Content-Type: application/rss+xml\n\n", $rss->as_string;
exit(0);
