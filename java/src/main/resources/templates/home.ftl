
<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
	<h1>Partner API Demo Site</h1>
	<h2>Welcome to the Climate Partner Demo App.</h2>
	<p> 
	  Welcome - ${tokenResponse.user.firstname} ${tokenResponse.user.lastname} 
	</p>
	<p> 
	  Email - ${tokenResponse.user.email}<br>
	  Country - ${tokenResponse.user.country}
	</p>
	<p> 
	  Access Token  - ${tokenResponse.accessToken}<br>
	  Refresh Token - ${tokenResponse.refreshToken}<br>
	  Scopes - ${tokenResponse.scopes}
	</p>
</@standardPage>