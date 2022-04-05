<#include "standardPage.ftl" />

<@standardPage title="Api Java Example">
    <h1>Partner API Demo Site</h1>
    <h2>Welcome to the Climate Partner Demo App.</h2>
    <table>
        <tr>
            <td> locationId </td>
            <td> growingSeason </td>
            <td> cropId </td>
            <td> phaPresent </td>
            <td> latestPhaDate </td>
            <td> initialDataReceivedOn </td>
            <td> latestDataReceivedOn </td>
            <td> latestHarvestDate </td>
            <td> distinctSeedProducts </td>
            <td> totalMoistureMass </td>
            <td> totalMoistureMassPhaAdjusted </td>
            <td> totalWetMass </td>
            <td> totalWetMassPhaAdjusted </td>
            <td> totalHarvestedArea </td>
            <td> totalHarvestedAreaPhaAdjusted </td>
            <td> climateCalculatedAverageYield </td>
            <td> climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings </td>
            <td> climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings </td>
            <td> growerAdjustedNominalWeight </td>
            <td> growerAdjustedNominalMoisture </td>
            <td> growerAdjustedShrinkFactor </td>
        </tr>
        <#list harvestReportsContents.results as harvestReportsContent>
        <tr>
            <td>
                ${harvestReportsContent.locationId}
            </td>
            <td>
                ${harvestReportsContent.growingSeason}
            </td>
            <td>
                ${harvestReportsContent.cropId}
            </td>
            <td>
                ${harvestReportsContent.phaPresent?string}
            </td>
            <td>
                ${harvestReportsContent.latestPhaDate}
            </td>
            <td>
                ${harvestReportsContent.initialDataReceivedOn}
            </td>
            <td>
                ${harvestReportsContent.latestDataReceivedOn}
            </td>
            <td>
                ${harvestReportsContent.latestHarvestDate}
            </td>
            <td>
                ${harvestReportsContent.distinctSeedProducts}
            </td>
            <td>
                ${harvestReportsContent.totalMoistureMass}
            </td>
            <td>
                ${harvestReportsContent.totalMoistureMassPhaAdjusted}
            </td>
            <td>
                ${harvestReportsContent.totalWetMass}
            </td>
            <td>
                ${harvestReportsContent.totalWetMassPhaAdjusted}
            </td>
            <td>
                ${harvestReportsContent.totalHarvestedArea}
            </td>
            <td>
                ${harvestReportsContent.totalHarvestedAreaPhaAdjusted}
            </td>
            <td>
                ${harvestReportsContent.climateCalculatedAverageYield}
            </td>
            <td>
                ${harvestReportsContent.climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings}
            </td>
            <td>
                ${harvestReportsContent.climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings}
            </td>
            <td>
                ${harvestReportsContent.growerAdjustedNominalWeight}
            </td>
            <td>
                ${harvestReportsContent.growerAdjustedNominalMoisture}
            </td>
            <td>
                ${harvestReportsContent.growerAdjustedShrinkFactor}
            </td>
        </tr>
        </#list>
    </table>
</@standardPage>