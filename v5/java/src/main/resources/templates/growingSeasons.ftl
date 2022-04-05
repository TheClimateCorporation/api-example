<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
    <h1>Partner API Demo Site</h1>
    <h2>Welcome to the Climate Partner Demo App.</h2>
    <#if growingSeasons?has_content>
        <p>Growing Seasons Content Id: <a href=${"growingSeasonsContents/${growingSeasons.contentId}"}>${growingSeasons.contentId}</p>
    <#else>
        <form method=post>
            <p>Field Id: <input type=text name=fieldId /></p>
            <p><input type=submit value=Submit /></p>
        </form>
    </#if>
</@standardPage>