package api.example.java.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class HarvestReportsContentsResponse {
    @JsonProperty("results")
    private List<HarvestReportsContents> results;

    public List<HarvestReportsContents> getResults() {
        return results;
    }

    public void setResults(List<HarvestReportsContents> results) {
        this.results = results;
    }
}
