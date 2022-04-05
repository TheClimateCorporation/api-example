package api.example.java.model;

public class HarvestReportsContents {
    private String locationId;
    private String growingSeason;
    private String cropId;
    private Boolean phaPresent;
    private String latestPhaDate;
    private String initialDataReceivedOn;
    private String latestDataReceivedOn;
    private String latestHarvestDate;
    private Integer distinctSeedProducts;
    private Double totalMoistureMass;
    private Double totalMoistureMassPhaAdjusted;
    private Double totalWetMass;
    private Double totalWetMassPhaAdjusted;
    private Double totalHarvestedArea;
    private Double totalHarvestedAreaPhaAdjusted;
    private Double climateCalculatedAverageYield;
    private Double climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings;
    private Double climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings;
    private Double growerAdjustedNominalWeight;
    private Double growerAdjustedNominalMoisture;
    private Double growerAdjustedShrinkFactor;

    public String getLocationId() {
        return locationId;
    }

    public void setLocationId(String locationId) {
        this.locationId = locationId;
    }

    public String getGrowingSeason() {
        return growingSeason;
    }

    public void setGrowingSeason(String growingSeason) {
        this.growingSeason = growingSeason;
    }

    public String getCropId() {
        return cropId;
    }

    public void setCropId(String cropId) {
        this.cropId = cropId;
    }

    public Boolean getPhaPresent() {
        return phaPresent;
    }

    public void setPhaPresent(Boolean phaPresent) {
        this.phaPresent = phaPresent;
    }

    public String getLatestPhaDate() {
        return latestPhaDate;
    }

    public void setLatestPhaDate(String latestPhaDate) {
        this.latestPhaDate = latestPhaDate;
    }

    public String getInitialDataReceivedOn() {
        return initialDataReceivedOn;
    }

    public void setInitialDataReceivedOn(String initialDataReceivedOn) {
        this.initialDataReceivedOn = initialDataReceivedOn;
    }

    public String getLatestDataReceivedOn() {
        return latestDataReceivedOn;
    }

    public void setLatestDataReceivedOn(String latestDataReceivedOn) {
        this.latestDataReceivedOn = latestDataReceivedOn;
    }

    public String getLatestHarvestDate() {
        return latestHarvestDate;
    }

    public void setLatestHarvestDate(String latestHarvestDate) {
        this.latestHarvestDate = latestHarvestDate;
    }

    public Integer getDistinctSeedProducts() {
        return distinctSeedProducts;
    }

    public void setDistinctSeedProducts(Integer distinctSeedProducts) {
        this.distinctSeedProducts = distinctSeedProducts;
    }

    public Double getTotalMoistureMass() {
        return totalMoistureMass;
    }

    public void setTotalMoistureMass(Double totalMoistureMass) {
        this.totalMoistureMass = totalMoistureMass;
    }

    public Double getTotalMoistureMassPhaAdjusted() {
        return totalMoistureMassPhaAdjusted;
    }

    public void setTotalMoistureMassPhaAdjusted(Double totalMoistureMassPhaAdjusted) {
        this.totalMoistureMassPhaAdjusted = totalMoistureMassPhaAdjusted;
    }

    public Double getTotalWetMass() {
        return totalWetMass;
    }

    public void setTotalWetMass(Double totalWetMass) {
        this.totalWetMass = totalWetMass;
    }

    public Double getTotalWetMassPhaAdjusted() {
        return totalWetMassPhaAdjusted;
    }

    public void setTotalWetMassPhaAdjusted(Double totalWetMassPhaAdjusted) {
        this.totalWetMassPhaAdjusted = totalWetMassPhaAdjusted;
    }

    public Double getTotalHarvestedArea() {
        return totalHarvestedArea;
    }

    public void setTotalHarvestedArea(Double totalHarvestedArea) {
        this.totalHarvestedArea = totalHarvestedArea;
    }

    public Double getTotalHarvestedAreaPhaAdjusted() {
        return totalHarvestedAreaPhaAdjusted;
    }

    public void setTotalHarvestedAreaPhaAdjusted(Double totalHarvestedAreaPhaAdjusted) {
        this.totalHarvestedAreaPhaAdjusted = totalHarvestedAreaPhaAdjusted;
    }

    public Double getClimateCalculatedAverageYield() {
        return climateCalculatedAverageYield;
    }

    public void setClimateCalculatedAverageYield(Double climateCalculatedAverageYield) {
        this.climateCalculatedAverageYield = climateCalculatedAverageYield;
    }

    public Double getClimateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings() {
        return climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings;
    }

    public void setClimateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings(Double climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings) {
        this.climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings = climateCalculatedGrowerAdjustedAverageYieldDefaultCropSettings;
    }

    public Double getClimateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings() {
        return climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings;
    }

    public void setClimateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings(Double climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings) {
        this.climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings = climateCalculatedGrowerAdjustedAverageYieldGrowerCropSettings;
    }

    public Double getGrowerAdjustedNominalWeight() {
        return growerAdjustedNominalWeight;
    }

    public void setGrowerAdjustedNominalWeight(Double growerAdjustedNominalWeight) {
        this.growerAdjustedNominalWeight = growerAdjustedNominalWeight;
    }

    public Double getGrowerAdjustedNominalMoisture() {
        return growerAdjustedNominalMoisture;
    }

    public void setGrowerAdjustedNominalMoisture(Double growerAdjustedNominalMoisture) {
        this.growerAdjustedNominalMoisture = growerAdjustedNominalMoisture;
    }

    public Double getGrowerAdjustedShrinkFactor() {
        return growerAdjustedShrinkFactor;
    }

    public void setGrowerAdjustedShrinkFactor(Double growerAdjustedShrinkFactor) {
        this.growerAdjustedShrinkFactor = growerAdjustedShrinkFactor;
    }
}
