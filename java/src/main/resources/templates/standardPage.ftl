<#macro standardPage title="">
<!DOCTYPE html>
<html lang="en">
<head>
    <title>${title}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<link rel="icon" href="/favicon.png">
	<style>
	table {
  		font-family: arial, sans-serif;
  		border-collapse: collapse;
  		width: 100%;
		}

		td, th {
 		 border: 1px solid #dddddd;
		  text-align: left;
		  padding: 8px;
		}

		tr:nth-child(even) {
		  background-color: #dddddd;
		}
	</style>
</head>
<body>
  

    <#nested/>

    <#include "footer.ftl">    
</body>
</html>
</#macro>