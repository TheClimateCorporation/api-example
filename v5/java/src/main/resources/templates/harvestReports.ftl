<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
    <h1>Partner API Demo Site</h1>
    <h2>Welcome to the Climate Partner Demo App.</h2>
    <#if harvestReports?has_content>
        <p>Harvest Reports Id: <a href=${"harvestReportsContents/${harvestReports.id}"}>${harvestReports.id}</p>
    <#else>
        <form method=post>
            <p>Field Id: <input type=text name=fieldId /></p>
            <p>Growing Seasons Ids: (Comma delimited)<textarea name=growingSeasons rows="4" cols="50"></textarea></p>
            <p><input type=submit value=Submit /></p>
        </form>
    </#if>
</@standardPage>