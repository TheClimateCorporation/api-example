<#if logout_link?has_content>
    <a href=${logout_link}>Logout</a>
</#if>
<#if tokenResponse?has_content>
    <a href=${"logout"}>Logout</a>
        &nbsp;|
    <a href=${"/"}>Home</a>
        &nbsp;|
    <a href=${"refresh-token?refresh_token="}${tokenResponse.refreshToken}>Refresh Token</a>
    <#if tokenResponse.scopes?has_content>
        <#if tokenResponse.scopes?contains("user")>
            &nbsp;|
            <a href=${"growingSeasons"}>Growing Seasons</a>
        </#if>
        <#if tokenResponse.scopes?contains("queries:read") && tokenResponse.scopes?contains("queries:write")>
            &nbsp;|
            <a href=${"harvestReports"}> Harvest Reports</a>
        </#if>
     </#if>
</#if>
