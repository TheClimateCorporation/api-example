<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
    <h1>Partner API Demo Site</h1>
    <h2>Welcome to the Climate Partner Demo App.</h2>
    <table>
        <tr>
            <td>Id</td>
            <td>name</td>
            <td>BoundaryId</td>
            <td>ResourceOwnerId</td>
            <td>ParentId</td>
            <td>ParentType</td>
        </tr>
        <#list fields as field>
        <tr>
            <td>
               ${field.id}
            </td>
            <td>${field.name}</td>
            <td>${field.boundaryId}</td>
            <td>${field.resourceOwnerId}</td>
            <td>${field.parent.id}</td>
            <td>${field.parent.type}</td> 
         </tr>	
         </#list>
    </table>
</@standardPage>