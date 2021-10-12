/*#################################################
# copyright 2008
# insert gpl license
#################################################*/

// ajax.js
// Created by: John Baab
// E-mail: john.baab@gmail.com

var req;
var dowhatnow;

function retrieveURL(url) 
{
	if (window.XMLHttpRequest) 
	{ // Non-IE browsers
		req = new XMLHttpRequest();
  		req.onreadystatechange = processStateChange;
		try 
		{
 			req.open("GET", url, true);
		} 
		catch (e) 
		{
      			alert(e);
		}
		req.send(null);
    	} 
	else if (window.ActiveXObject) 
	{ // IE
      		req = new ActiveXObject("Microsoft.XMLHTTP");
      		if (req) 
		{
        		req.onreadystatechange = processStateChange;
        		req.open("GET", url, true);
        		req.send();
      		}
    	}
}

function processStateChange() 
{
	if (req.readyState == 4) 
	{ // Complete
		if (req.status == 200) 
		{ // OK response
			//alert("done");
			//alert(req.responseText);
			//alert(req.responseText);
			if (dowhatnow == "rss")
				document.getElementById("feed").innerHTML = req.responseText;
			else if(dowhatnow == "deleteFile"){
				alert("File Delete Job has been added to the queue.");
				//location.reload()
			}
			else if(dowhatnow == "deleteJob"){
				alert("Job has been removed from the queue.");
				location.reload()
			}
			//var newtext = document.createTextNode(req.responseText);
			//document.getElementById("feed").appendChild(newtext);
			//transformData(req.responseText);
		} 
		else 
		{
			alert("Problem: " + req.statusText);
		}
	}
}

function openRSS()
{
	//document.getElementById("feed").innerHTML = "SOMETHING!!!";
	//alert("test");
	//alert("mythexportRSS.cgi?podcastName=" + document.getElementById("podcast").value);
	//retrieveURL("mythexportRSS.cgi?podcastName=" + document.getElementById("podcast").value);
	dowhatnow = "rss";
	retrieveURL("wrapper.cgi?podcastName=" + document.getElementById("podcast").value);
	document.getElementById("link").href = "mythexportRSS.cgi?podcastName=" + document.getElementById("podcast").value;
	//retrieveURL("rss.cgi");
	
	//document.getElementById("test").innerHTML="image.cgi?image=" + image;
}

function deleteFile(id)
{
	//alert("test2");
	dowhatnow = "deleteFile";
	retrieveURL("deleteFile.cgi?id=" + id);
	return true;
}

function deleteJob(id)
{
	//alert("test2");
	dowhatnow = "deleteJob";
	retrieveURL("deleteJob.cgi?id=" + id);
	return true;
}


