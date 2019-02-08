<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
    <h1>Partner API Demo Site</h1>
    <h2>Welcome to the Climate Partner Demo App.</h2>
    <table>
        <tr>
            <td>Id</td>
            <td>Start Date</td>
            <td>End Date </td>
            <td>Created At</td>
            <td>Updated At</td>
            <td>Length</td>
            <td>Field Ids</td>
        </tr>
        <#list activities as activity>
        <tr>
            <td>
                <a href=${"agronomic-contents?id="}${activity.id}&length=${activity.length}&data=${dataType}>${activity.id}</a>	
            </td>
            <td>${activity.startTime}</td>
            <td>${activity.endTime}</td>
            <td>${activity.createdAt}</td>
            <td>${activity.updatedAt}</td>
            <td>${activity.length}</td> 
            <td>[
                <#list activity.fieldIds as field>
                    ${field}&nbsp;
                </#list>]
            </td>
         </tr>	
         </#list>
    </table>
</@standardPage>