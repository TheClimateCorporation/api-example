<#if logout_link?has_content>
    <a href=${logout_link}>	Logout</a>
</#if>

<#if refreshLink?has_content>


</#if>

<#if tokenResponse?has_content>
	    <a href=${"logout"}>	Logout</a>
	    &nbsp;|
	    <a href=${"/"}>	Home</a>
		&nbsp;|
		<a href=${"refresh-token?refresh_token="}${tokenResponse.refreshToken}>Refresh Token</a>		

	<#if tokenResponse.scopes?has_content>
		
			<#if tokenResponse.scopes?contains("asPlanted:read")>
				&nbsp;|
				<a href=${"agronomic?data=asPlanted"}> asPlanted</a>
			</#if>
			<#if tokenResponse.scopes?contains("asPlanted:read")>
				&nbsp;|
				<a href=${"agronomic?data=asApplied"}> asApplied</a>
			</#if>
			<#if tokenResponse.scopes?contains("asHarvested:read")>
				&nbsp;|
				<a href=${"agronomic?data=asHarvested"}> asHarvested</a>
			</#if>								
	</#if>
</#if>
