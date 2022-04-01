package api.example.java.api;

import api.example.java.model.GrowingSeasonsContentsResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import api.example.java.Config;
import api.example.java.model.GrowingSeasons;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.BodyInserters;

import java.util.HashMap;
import java.util.Map;

@Component
public class ClimateAPIs {
    private static Logger logger = LoggerFactory.getLogger(ClimateAPIs.class);
    @Autowired
    protected RequestClient requestClient;
    @Autowired
    protected Config config;

    public GrowingSeasons createGrowingSeasons(String uri, String fieldId, String accessToken) {
        Map<String, String> body = new HashMap();
        body.put("fieldId", fieldId);

        GrowingSeasons growingSeasons = requestClient.getWebClientJSON(uri, accessToken, config.apiKey)
                .post()
                .body(BodyInserters.fromValue(body))
                .retrieve()
                .bodyToMono(GrowingSeasons.class)
                .block();

        return growingSeasons;
    }

    public GrowingSeasonsContentsResponse getGrowingSeasonsContents(String uri, String accessToken) {
        GrowingSeasonsContentsResponse growingSeasonsContentsResponse = requestClient.getWebClient(
                uri, accessToken, config.apiKey)
                .get()
//                .exchangeToMono(res -> res.bodyToMono(GrowingSeasonsContentsResponse.class))
                .retrieve()
                .bodyToMono(GrowingSeasonsContentsResponse.class)
                .block();
        return growingSeasonsContentsResponse;
    }
}
