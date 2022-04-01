<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
    <h1>Partner API Demo Site</h1>
    <h2>Welcome to the Climate Partner Demo App.</h2>
    <table>
        <tr>
            <td> Id </td>
            <td> Year </td>
        </tr>
        <#list growingSeasonsContents.results as growingSeasonsContent>
        <tr>
            <td>
                ${growingSeasonsContent.id}
            </td>
            <td>
                ${growingSeasonsContent.year}
            </td>
        </tr>
        </#list>
    </table>
</@standardPage>