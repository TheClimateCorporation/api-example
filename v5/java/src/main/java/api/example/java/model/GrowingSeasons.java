package api.example.java.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GrowingSeasons {
    @JsonProperty("contentId")
    private String contentId;

    public String getContentId() {
        return contentId;
    }

    public void setContentId(String contentId) {
        this.contentId = contentId;
    }
}
