package api.example.java.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class GrowingSeasonsContentsResponse {
    @JsonProperty("results")
    private List<GrowingSeasonsContents> results;

    public List<GrowingSeasonsContents> getResults() {
        return results;
    }

    public void setResults(List<GrowingSeasonsContents> results) {
        this.results = results;
    }
}
