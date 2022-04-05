package api.example.java.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class HarvestReportsRequest {
    @JsonProperty("fieldId")
    private String fieldId;

    @JsonProperty("growingSeasons")
    private String[] growingSeasons;

    public String getFieldId() {
        return fieldId;
    }

    public String[] getGrowingSeasons() {
        return growingSeasons;
    }

    public void setFieldId(String fieldId) {
        this.fieldId = fieldId;
    }

    public void setGrowingSeasons(String[] growingSeasons) {
        this.growingSeasons = growingSeasons;
    }
}
