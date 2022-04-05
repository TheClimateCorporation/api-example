package api.example.java.api;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.codec.LoggingCodecSupport;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class RequestClient {

    public WebClient getWebClient(String uri, String accessToken, String apiKey) {
        return WebClient.builder()
                .baseUrl(uri).exchangeStrategies(exchangeStrategies())
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.ALL_VALUE)
                .defaultHeader("x-api-key", apiKey)
                .build();
    }

    public WebClient getWebClient(String uri, String auth) {
        return WebClient.builder()
                .baseUrl(uri)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_FORM_URLENCODED_VALUE)
                .defaultHeader(HttpHeaders.AUTHORIZATION, auth)
                .exchangeStrategies(exchangeStrategies())
                .build();
    }

    public WebClient getWebClientJSON(String uri, String accessToken, String apiKey) {
        return WebClient.builder()
                .baseUrl(uri).exchangeStrategies(exchangeStrategies())
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.ALL_VALUE)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .defaultHeader("x-api-key", apiKey)
                .build();
    }

    public WebClient getWebClientId(String uri, String id, String accessToken, String apiKey) {
        return WebClient.builder()
                .baseUrl(uri).exchangeStrategies(exchangeStrategies())
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
                .defaultHeader(HttpHeaders.ACCEPT, MediaType.ALL_VALUE)
                .defaultHeader("x-api-key", apiKey)
                .build();
    }

    private ExchangeStrategies exchangeStrategies() {
        ExchangeStrategies exchangeStrategies = ExchangeStrategies.withDefaults();
        exchangeStrategies
                .messageWriters()
                .stream()
                .filter(LoggingCodecSupport.class::isInstance)
                .forEach(writer -> ((LoggingCodecSupport) writer).setEnableLoggingRequestDetails(true));
        return exchangeStrategies;
    }
}
